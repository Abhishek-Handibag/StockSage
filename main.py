import uvicorn
import sys
import uuid
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel

# --- Setup Project Path ---
# This ensures that your agent's imports (like 'data_researcher_agent')
# can be found by Python when this script is run.
root_dir = Path(__file__).parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
# --------------------------


# --- ADK and Gemini Imports ---
# These are the necessary components to run an ADK agent
try:
    from google.adk.sessions import InMemorySessionService
    from google.adk.runners import Runner
    from google.genai import types as genai_types
except ImportError:
    print("Error: ADK libraries not found.")
    print("Please ensure 'google-adk' and 'google-generativeai' are installed.")
    sys.exit(1)
# --------------------------


# --- Import Your Agent ---
try:
    from chat_orchestrator.agent import root_agent
except ImportError:
    print("Error: Could not import 'root_agent'.")
    print("Please ensure 'main.py' is in your project's root directory,")
    print("and your agent is located at 'chat_orchestrator_agent/agent.py'.")
    sys.exit(1)
# -------------------------


# --- Define Request and Response Models ---
class ChatRequest(BaseModel):
    query: str
    user_id: str = "default-user" # Optional: allow user_id from client

class ChatResponse(BaseModel):
    response: str
# -------------------------


# --- Initialize FastAPI App ---
app = FastAPI(
    title="Chat Orchestrator API",
    description="An API to interact with the multi-agent ADK orchestrator.",
    version="1.0.0",
)
# ----------------------------


# --- Initialize ADK Runner and Session ---
# These are the core components for running your agent.
APP_NAME = "chat_orchestrator_app"

# The SessionService stores conversation state.
# InMemorySessionService is the simplest, non-persistent option.
session_service = InMemorySessionService()

# The Runner is the engine that executes the agent.
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
# ---------------------------------------


# --- Define the /chat Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest):
    """
    Receives a user query, processes it with the ADK agent,
    and returns the agent's final response.
    """
    try:
        # 1. Create a unique session for each request.
        session_id = f"session_{uuid.uuid4()}"
        
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id
        )

        # 2. Format the user's query into the ADK's 'Content' format.
        user_message = genai_types.Content(
            role='user',
            parts=[genai_types.Part(text=request.query)]
        )

        # 3. Use the ASYNC runner method instead of sync in threadpool.
        # This is the proper way to run ADK agents in FastAPI.
        final_response = "Agent did not provide a final response."
        
        async for event in runner.run_async(
            user_id=request.user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            if event.is_final_response():
                # The final response is in the 'parts' of the event content
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                break
        
        return ChatResponse(response=final_response)
        
    except Exception as e:
        # Handle any errors during agent execution
        return ChatResponse(response=f"An error occurred: {repr(e)}")
# -------------------------------


# --- Run the Server ---
if __name__ == "__main__":
    print("Starting FastAPI server at http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
# ----------------------