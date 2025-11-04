"""
FastAPI Backend for Multi-Agent Chat Orchestrator.

This module implements a RESTful API for interacting with an intelligent 
multi-agent system powered by Google's Agent Development Kit (ADK). 
The orchestrator dynamically routes user queries to specialized agents, 
such as financial data researchers or web intelligence agents, 
based on the content and context of the query.

Architecture:
    - chat_orchestrator: Acts as the central coordinator using an 
      LLM-driven delegation pattern to route user queries.
    - data_researcher_agent: Specialized in financial market data 
      collection, analysis, and research.
    - web_intelligence_agent: Focused on web-based intelligence, 
      search, and real-time event insights.

API Endpoints:
    - GET  /           : Returns API information and metadata.
    - GET  /health     : Performs a system health check.
    - POST /chat       : Handles user queries and coordinates 
      agent responses.

Author:
    Abhishek Handibag
    
Version:
    1.0.0
"""


import uvicorn
import sys
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Setup Project Path ---
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# --- ADK and Gemini Imports ---
try:
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types as genai_types
except ImportError as e:
    logger.error("ADK libraries not found: %s", e)
    print("Error: ADK libraries not found.")
    print("Please ensure 'google-adk' and 'google-generativeai' are installed.")
    print("Run: pip install google-adk google-generativeai")
    sys.exit(1)

try:
    from chat_orchestrator.agent import root_agent
except ImportError as e:
    logger.error("Failed to import root_agent: %s", e)
    print("Error: Could not import 'root_agent'.")
    print("Please ensure 'main.py' is in your project's root directory,")
    print("and your agent is located at 'chat_orchestrator/agent.py'.")
    sys.exit(1)


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Attributes:
        query: The user's question or request
        user_id: Optional identifier for the user (default: "default-user")
    """
    query: str = Field(..., description="User's question or query", min_length=1, max_length=5000)
    user_id: str = Field(default="default-user", description="User identifier for session management")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the current price of Tesla stock?",
                "user_id": "user123"
            }
        }


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Attributes:
        response: The agent's response to the user's query
        session_id: Unique identifier for this conversation session
        timestamp: ISO format timestamp of the response
    """
    response: str = Field(..., description="Agent's response to the user query")
    session_id: Optional[str] = Field(None, description="Session identifier")
    timestamp: Optional[str] = Field(None, description="Response timestamp in ISO format")


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    Attributes:
        status: Service health status
        timestamp: Current server timestamp
        version: API version
        agent_status: Status of the ADK agent
    """
    status: str = Field(..., description="Service health status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version")
    agent_status: str = Field(..., description="ADK agent initialization status")


class RootResponse(BaseModel):
    """
    Response model for root endpoint.
    
    Attributes:
        message: Welcome message
        version: API version
        documentation: URL to API documentation
        endpoints: Available API endpoints
    """
    message: str
    version: str
    documentation: str
    endpoints: Dict[str, str]


# --- Initialize FastAPI App ---
app = FastAPI(
    title="StockSage : Multi-Agent Chat Orchestrator API",
    description="""
    Intelligent multi-agent system for financial research and web intelligence
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Abhishek Handibag",
        "url": "https://github.com/Abhishek-Handibag/StockSage",
    },
    license_info={
        "name": "MIT",
    },
)

# --- Initialize ADK Components ---
APP_NAME = "chat_orchestrator_app"
APP_VERSION = "1.0.0"

try:
    session_service = InMemorySessionService()
    logger.info("Session service initialized successfully")
    
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    logger.info("ADK Runner initialized successfully with agent: %s", root_agent.name)
    AGENT_STATUS = "initialized"
except Exception as e:
    logger.error("Failed to initialize ADK components: %s", e)
    AGENT_STATUS = f"error: {str(e)}"
    raise


# --- API Endpoints ---

@app.get("/", response_model=RootResponse, tags=["Info"])
async def root():
    """
    Root endpoint providing API information and available endpoints.
    
    Returns:
        RootResponse: API information including version and available endpoints
    """
    return RootResponse(
        message="Welcome to the Multi-Agent Chat Orchestrator API",
        version=APP_VERSION,
        documentation="/docs",
        endpoints={
            "root": "/",
            "health": "/health",
            "chat": "POST /chat",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    )


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify service availability and agent status.
    
    Returns:
        HealthResponse: Current health status of the service and agents
        
    Status Codes:
        200: Service is healthy and operational
        503: Service is unavailable or agents are not initialized
    """
    try:
        health_status = {
            "status": "healthy" if AGENT_STATUS == "initialized" else "degraded",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": APP_VERSION,
            "agent_status": AGENT_STATUS
        }
        
        status_code = status.HTTP_200_OK if AGENT_STATUS == "initialized" else status.HTTP_503_SERVICE_UNAVAILABLE
        
        return JSONResponse(
            status_code=status_code,
            content=health_status
        )
    except Exception as e:
        logger.error("Health check failed: %s", e)
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "version": APP_VERSION,
                "agent_status": f"error: {str(e)}"
            }
        )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_with_agent(request: ChatRequest):
    """
    Main chat endpoint for interacting with the multi-agent orchestrator.
    
    This endpoint receives user queries and routes them to specialized agents:
    - Financial queries → data_researcher_agent
    - General/web queries → web_intelligence_agent
    
    The coordinator uses LLM-driven delegation to automatically determine
    the appropriate specialist agent based on query content.
    
    Args:
        request: ChatRequest containing the user's query and optional user_id
        
    Returns:
        ChatResponse: Agent's response with session information
        
    Raises:
        HTTPException: 
            - 400: Invalid request or empty query
            - 500: Internal server error during agent execution
            - 503: Service unavailable (agents not initialized)
            
    Example:
        Request:
            {
                "query": "What is the current price of AAPL?",
                "user_id": "user123"
            }
            
        Response:
            {
                "response": "Based on Alpha Vantage data...",
                "session_id": "session_abc123",
                "timestamp": "2025-11-02T10:30:00Z"
            }
    """
    if AGENT_STATUS != "initialized":
        logger.error("Chat request received but agent not initialized")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Service unavailable: Agent status is '{AGENT_STATUS}'"
        )
    
    # Validate request
    if not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )
    
    session_id = f"session_{uuid.uuid4()}"
    logger.info("Processing chat request - User: %s, Session: %s", request.user_id, session_id)
    
    try:
        # Create new session
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id
        )
        logger.debug("Session created successfully: %s", session_id)
        
        # Format user message for ADK
        user_message = genai_types.Content(
            role='user',
            parts=[genai_types.Part(text=request.query)]
        )
        
        # Execute agent asynchronously
        final_response = "Agent did not provide a final response."
        
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                    logger.info("Agent response generated successfully for session: %s", session_id)
                break
        
        return ChatResponse(
            response=final_response,
            session_id=session_id,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
        
    except Exception as e:
        logger.error("Error processing chat request: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


# --- Exception Handlers ---

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request: The request that caused the exception
        exc: The exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    )


# --- Startup and Shutdown Events ---

@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Logs initialization information.
    """
    logger.info("=" * 70)
    logger.info("Multi-Agent Chat Orchestrator API Starting")
    logger.info("=" * 70)
    logger.info("Version: %s", APP_VERSION)
    logger.info("Agent: %s", root_agent.name)
    logger.info("Agent Status: %s", AGENT_STATUS)
    logger.info("Documentation: http://127.0.0.1:8000/docs")
    logger.info("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event handler.
    Logs shutdown information and performs cleanup.
    """
    logger.info("Multi-Agent Chat Orchestrator API shutting down...")


# --- Server Entry Point ---

if __name__ == "__main__":
    print("=" * 70)
    print("Multi-Agent Chat Orchestrator API")
    print("=" * 70)
    print(f"Version: {APP_VERSION}")
    print(f"Agent: {root_agent.name}")
    print(f"Status: {AGENT_STATUS}")
    print("=" * 70)
    print("Starting FastAPI server at http://127.0.0.1:8000")
    print("Documentation available at http://127.0.0.1:8000/docs")
    print("=" * 70)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )
