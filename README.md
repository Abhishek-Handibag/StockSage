# StockSage

## Project Overview
A StockSage is a professional-grade AI-powered multi-agent system built with Google's Agent Development Kit (ADK) and FastAPI. This system intelligently orchestrates specialized agents for comprehensive stock market analysis and web intelligence gathering. Using LLM-driven delegation, it automatically routes user queries to the appropriate specialist agent, providing accurate, data-driven insights through a REST API.

## Features
- **🚀 FastAPI REST API**: Production-ready backend with comprehensive documentation
- **🤖 LLM-Driven Agent Routing**: Automatic query analysis and delegation using Gemini 2.5 Flash
- **📊 Financial Data Analysis**: Deep integration with Alpha Vantage MCP for real-time stock data, technical indicators, and fundamental analysis
- **🌐 Web Intelligence**: Google Custom Search integration for current news, market sentiment, and web research
- **🏗️ Multi-Agent Architecture**: Coordinator pattern with specialized sub-agents
- **📈 Comprehensive Market Coverage**: Stocks, forex, cryptocurrencies, commodities, and economic indicators
- **🔍 Technical & Fundamental Analysis**: RSI, MACD, SMA, EMA, earnings, balance sheets, and more
- **📝 Interactive API Docs**: Swagger UI and ReDoc for easy testing and integration
- **💪 Health Monitoring**: Built-in health check endpoints and logging

## Installation

### Prerequisites
- Python 3.11 or higher
- Git

### Setup Steps

1. **Clone the repository:**
    ```sh
    git clone https://github.com/Abhishek-Handibag/StockSage.git
    cd StockSage
    ```

2. **Create and activate a Python virtual environment:**
    ```bash
    # Windows (PowerShell)
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
    Or install core packages manually:
    ```bash
    pip install google-adk google-generativeai fastapi uvicorn python-dotenv pydantic
    ```

4. **Configure environment variables:**
   
   Create a `.env` file in the project root:
    ```env
    # Gemini API Configuration
    GOOGLE_GENAI_USE_VERTEXAI=0
    GOOGLE_API_KEY=your_gemini_api_key_here
    
    # Alpha Vantage MCP Server
    STOCK_MARKET_API=your_alphavantage_api_key_here
    
    # Google Custom Search (Optional - for web intelligence)
    GOOGLE_SEARCH_API_KEY=your_google_search_api_key_here
    GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here
    GOOGLE_CUSTOM_SEARCH_URL=https://www.googleapis.com/customsearch/v1
    ```
   
   **Get Your API Keys:**
   - **Gemini API**: [Google AI Studio](https://aistudio.google.com/apikey)
   - **Alpha Vantage API**: [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - **Google Custom Search**: [Google Cloud Console](https://console.cloud.google.com/) → Enable Custom Search API

## Usage

### Starting the FastAPI Server

```bash
python main.py
```

The server will start at `http://127.0.0.1:8000`

**Access the API:**
- 🏠 **Root**: http://127.0.0.1:8000/
- 💬 **Chat Endpoint**: http://127.0.0.1:8000/chat (POST)
- 🏥 **Health Check**: http://127.0.0.1:8000/health
- 📚 **API Documentation**: http://127.0.0.1:8000/docs
- 📖 **Alternative Docs**: http://127.0.0.1:8000/redoc

### Making API Requests

#### Using cURL:
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the current price of Tesla stock?",
    "user_id": "user123"
  }'
```

#### Using Python:
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/chat",
    json={
        "query": "What is Apple's RSI indicator?",
        "user_id": "user123"
    }
)

print(response.json())
```

#### Using the Interactive Docs:
Navigate to http://127.0.0.1:8000/docs and use the built-in "Try it out" feature

## Architecture

### Multi-Agent System Design

This project implements the **Coordinator/Dispatcher Pattern** using ADK's LLM-driven delegation:

```
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│         (main.py)                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Chat Orchestrator Agent              │
│    (LLM-Driven Delegation)              │
│                                         │
│  • Analyzes user queries                │
│  • Routes to appropriate specialist     │
│  • Uses transfer_to_agent()             │
└──────┬──────────────────────┬───────────┘
       │                      │
       ▼                      ▼
┌──────────────────┐   ┌──────────────────┐
│ Data Researcher  │   │ Web Intelligence │
│ Agent            │   │ Agent            │
│                  │   │                  │
│ • Alpha Vantage  │   │ • Google Search  │
│ • MCP Tools      │   │ • Web Scraping   │
│ • Financial Data │   │ • News & Events  │
└──────────────────┘   └──────────────────┘
```

### Agent Components

#### 1. **Chat Orchestrator** (`chat_orchestrator/agent.py`)
- **Pattern**: Coordinator/Dispatcher with LLM-driven delegation
- **Model**: Gemini 2.5 Flash
- **Function**: Analyzes queries and transfers to appropriate specialist
- **Routing Strategy**:
  - Financial queries → `data_researcher_agent`
  - Web/news queries → `web_intelligence_agent`
  - Automatic via `transfer_to_agent()` function call

#### 2. **Data Researcher Agent** (`data_researcher_agent/agent.py`)
- **Specialization**: Financial market data and analysis
- **Data Source**: Alpha Vantage MCP Server (via MCPToolset)
- **Model**: Gemini 2.5 Flash
- **Capabilities**:
  - ✅ Real-time stock quotes and historical data
  - ✅ Technical indicators (RSI, MACD, SMA, EMA, Bollinger Bands, ATR, STOCH)
  - ✅ Fundamental analysis (earnings, balance sheets, income statements, cash flow)
  - ✅ Options data and insider transactions
  - ✅ Economic indicators (CPI, GDP, inflation, unemployment)
  - ✅ Forex, cryptocurrencies, and commodities (WTI, Brent, Gold, etc.)
  - ✅ Market news sentiment and earnings calendars

#### 3. **Web Intelligence Agent** (`web_intelligence_agent/agent.py`)
- **Specialization**: Web research and information gathering
- **Architecture**: Multi-agent loop (optimizer + data gatherer)
- **Model**: Gemini 2.5 Flash
- **Data Sources**: 
  - Google Custom Search API
  - Web scraping (BeautifulSoup4)
- **Capabilities**:
  - ✅ Real-time web search for current events
  - ✅ News articles and market sentiment
  - ✅ Company announcements and press releases
  - ✅ General market intelligence and context

## API Endpoints

### POST /chat
Main chat endpoint for querying the multi-agent system.

**Request Body:**
```json
{
  "query": "What is the current price of Tesla stock?",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "response": "Based on Alpha Vantage data from GLOBAL_QUOTE, TSLA...",
  "session_id": "session_abc-123-def",
  "timestamp": "2025-11-02T10:30:00Z"
}
```

### GET /health
Health check endpoint for monitoring service status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-02T10:30:00Z",
  "version": "1.0.0",
  "agent_status": "initialized"
}
```

### GET /
Root endpoint with API information.

## Example Queries

### Financial Data Queries (→ data_researcher_agent)
```
✅ "What is the current price of AAPL?"
✅ "Show me Tesla's RSI indicator"
✅ "What are Apple's latest quarterly earnings?"
✅ "Give me the top gainers today"
✅ "What is the MACD for Microsoft?"
✅ "Show me Bitcoin's current price"
```

### Web Intelligence Queries (→ web_intelligence_agent)
```
✅ "What's the latest news about Tesla?"
✅ "Current tech industry trends"
✅ "Recent announcements from Microsoft"
✅ "Latest AI developments"
```

### Query Routing Logic
The orchestrator automatically analyzes each query and routes it to the appropriate agent:
- Keywords like "price", "stock", "RSI", "earnings" → Financial agent
- Keywords like "news", "latest", "trends", "announcements" → Web agent
- The LLM makes intelligent routing decisions based on context

## Project Structure
```
StockSage/
├── main.py                     # 🚀 FastAPI backend entry point
├── requirements.txt            # 📦 Python dependencies
├── .env                        # 🔐 Environment variables (create from .env.example)
├── .env.example                # 📝 Example environment configuration
├── .gitignore
├── LICENSE
├── README.md
│
├── chat_orchestrator/          # 🎯 Main coordinator agent
│   ├── __init__.py
│   └── agent.py               # LLM-driven delegation logic
│
├── data_researcher_agent/      # 📊 Financial data specialist
│   ├── __init__.py
│   ├── agent.py               # Alpha Vantage MCP integration
│   └── .env                   # Agent-specific config
│
└── web_intelligence_agent/     # 🌐 Web research specialist
    ├── __init__.py
    ├── agent.py               # Multi-agent search workflow
    ├── google_search_tool.py  # Google Custom Search wrapper
    ├── web_scraper_tool.py    # Web scraping utilities
    ├── tools.py               # Tool exports
    └── .env                   # Agent-specific config
```

## Development

### Running Tests
Test the orchestrator with sample queries:
```bash
python test_orchestrator.py
```

### Testing Individual Agents
```bash
# Test with ADK CLI
adk run ./chat_orchestrator/
adk run ./data_researcher_agent/
adk run ./web_intelligence_agent/
```

### Freezing Dependencies
```bash
pip freeze > requirements.txt
```

## Contributing
We welcome contributions!
1. Fork the repository: [StockSage GitHub](https://github.com/Abhishek-Handibag/StockSage)
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes with clear messages
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

**Contribution Guidelines:**
- Follow existing code style and structure
- Add docstrings to all functions and classes
- Update README.md if adding new features
- Test your changes before submitting

## Technical Stack

### Backend
- **API Framework**: FastAPI 0.119+
- **Server**: Uvicorn (ASGI)
- **Agent Framework**: Google ADK (Agent Development Kit) 1.16+
- **LLM**: Gemini 2.5 Flash (via Google GenAI)
- **Python**: 3.11+

### Data Sources
- **Financial Data**: Alpha Vantage MCP Server (Model Context Protocol)
- **Web Search**: Google Custom Search API
- **Web Scraping**: BeautifulSoup4 + lxml

### Key Libraries
- `google-adk` - Agent Development Kit framework
- `google-genai` - Gemini API client
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-dotenv` - Environment management

## Architecture Highlights

### Design Patterns
- ✅ **Coordinator/Dispatcher Pattern**: LLM-driven agent delegation
- ✅ **Multi-Agent System**: Hierarchical agent composition
- ✅ **MCP Integration**: Streaming financial data via Model Context Protocol
- ✅ **Async/Await**: Non-blocking agent execution in FastAPI
- ✅ **RESTful API**: Clean, documented HTTP endpoints

### Key Features
- 🎯 **Automatic Routing**: LLM analyzes queries and calls `transfer_to_agent()`
- 🔄 **Async Agent Execution**: Uses `runner.run_async()` for proper FastAPI integration
- 📊 **Session Management**: In-memory session service for conversation state
- 🛡️ **Error Handling**: Comprehensive exception handling and logging
- 📝 **API Documentation**: Auto-generated Swagger UI and ReDoc
- 🏥 **Health Monitoring**: Built-in health check endpoints
- 🔐 **Environment Security**: API keys managed via .env files

### Agent Communication
- **Shared State**: Agents communicate via session state
- **LLM Transfer**: Coordinator uses `transfer_to_agent()` function calls
- **Tool Invocation**: Specialized agents use FunctionTool and MCPToolset
- **Event Streaming**: Async event streams for real-time responses

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Issue: `httpcore.ConnectError: [Errno 11001] getaddrinfo failed`**
- **Cause**: Using sync `runner.run()` in FastAPI causes event loop conflicts
- **Solution**: Use `runner.run_async()` instead (already implemented in main.py)

**Issue: Agent returns only agent name instead of response**
- **Cause**: Using SequentialAgent instead of LLM-driven delegation
- **Solution**: Use single LlmAgent with sub_agents (already implemented)

**Issue: MCP connection errors**
- **Cause**: Invalid or missing Alpha Vantage API key
- **Solution**: Verify `STOCK_MARKET_API` in .env file

**Issue: Import errors**
- **Cause**: Virtual environment not activated or dependencies not installed
- **Solution**: Activate venv and run `pip install -r requirements.txt`

## Performance Considerations

- **Session Management**: Currently uses in-memory sessions (data lost on restart)
- **Rate Limits**: Alpha Vantage free tier has API call limits
- **Response Time**: First query may be slower due to MCP initialization
- **Concurrent Requests**: FastAPI handles multiple requests asynchronously

## Future Enhancements

- [ ] Persistent session storage (Redis/PostgreSQL)
- [ ] Caching layer for frequently requested data
- [ ] WebSocket support for streaming responses
- [ ] User authentication and rate limiting
- [ ] Conversation history and context management
- [ ] Deployment guides (Docker, Cloud Run, etc.)
- [ ] Monitoring and observability (Prometheus, Grafana)

## Contact

For questions, suggestions, or collaboration:
- **GitHub Repository**: [https://github.com/Abhishek-Handibag/StockSage](https://github.com/Abhishek-Handibag/StockSage)
- **Issues**: [Open an issue](https://github.com/Abhishek-Handibag/StockSage/issues)
- **Author**: Abhishek Handibag

---

## Acknowledgments

This project leverages:
- **Google ADK** - Agent Development Kit framework
- **Google Gemini** - Advanced LLM capabilities  
- **Alpha Vantage** - Financial market data
- **FastAPI** - Modern Python web framework

---

**Multi-Agent Chat Orchestrator**: Professional AI-driven financial intelligence and web research, powered by Google ADK and FastAPI.

---

**Note:** This project demonstrates advanced multi-agent architecture using Google's ADK framework with the Coordinator/Dispatcher pattern, LLM-driven delegation, and production-ready REST API design.