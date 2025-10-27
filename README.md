# StockSage

## Project Overview
StockSage is a professional-grade AI-powered multi-agent system for comprehensive stock analysis and market intelligence. It combines specialized agents for financial data analysis, web intelligence gathering, and intelligent query routing to provide accurate, data-driven insights for investors and analysts.

## Features
- **Intelligent Query Routing**: Chat orchestrator automatically routes queries to the appropriate specialized agent
- **Financial Data Analysis**: Deep integration with Alpha Vantage API for real-time stock data, technical indicators, and fundamental analysis
- **Web Intelligence**: Google Custom Search integration for current news, market sentiment, and web research
- **Multi-Agent Architecture**: Three specialized agents working together seamlessly
- **Comprehensive Market Coverage**: Stocks, forex, cryptocurrencies, commodities, and economic indicators
- **Technical & Fundamental Analysis**: RSI, MACD, SMA, EMA, earnings, balance sheets, and more

## Installation
1. **Clone the repository:**
    ```sh
    git clone https://github.com/Abhishek-Handibag/StockSage.git
    cd StockSage
    ```
2. **Create and activate a Python virtual environment:**
    ```sh
    python -m venv venv
    # Activate (Windows)
    venv\Scripts\Activate.ps1
    # Or (Linux/macOS)
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```sh
    pip install google-adk python-dotenv requests beautifulsoup4 lxml
    ```
4. **Configure environment variables:**
   
   Create a `.env` file in the project root with the following keys:
    ```env
    GOOGLE_API_KEY="Your Gemini API Key"
    STOCK_MARKET_API="Your Alpha Vantage API Key"
    GOOGLE_SEARCH_API_KEY="Your Google Search API Key"
    GOOGLE_SEARCH_ENGINE_ID="Your Google Search Engine ID"
    GOOGLE_CUSTOM_SEARCH_URL="https://www.googleapis.com/customsearch/v1"
    ```
   
   **API Key Sources:**
   - **Gemini API**: [Google AI Studio](https://aistudio.google.com/apikey)
   - **Alpha Vantage API**: [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
   - **Google Custom Search**: [Google Cloud Console](https://console.cloud.google.com/)

## Usage

### Running the Multi-Agent System
The chat orchestrator automatically routes queries to the appropriate specialized agents:

```sh
adk run .\chat_orchestrator\
```

### Agent Architecture

#### 1. **Chat Orchestrator Agent** (`chat_orchestrator/`)
- **Role**: Intelligent query router and response synthesizer
- **Function**: Analyzes user queries and delegates to appropriate specialized agents
- **Routing Logic**:
  - Financial queries → Data Researcher Agent
  - Web/news queries → Web Intelligence Agent
  - Combined queries → Both agents sequentially

#### 2. **Data Researcher Agent** (`data_researcher_agent/`)
- **Role**: Financial data specialist
- **Data Source**: Alpha Vantage MCP Server
- **Capabilities**:
  - Real-time stock quotes and historical data
  - Technical indicators (RSI, MACD, SMA, EMA, Bollinger Bands, ATR, etc.)
  - Fundamental analysis (earnings, balance sheets, income statements, cash flow)
  - Options data and insider transactions
  - Economic indicators (CPI, GDP, inflation, unemployment)
  - Forex, cryptocurrencies, and commodities
  - Market news sentiment and earnings calendars

#### 3. **Web Intelligence Agent** (`web_intelligence_agent/`)
- **Role**: Web research and information gathering
- **Data Source**: Google Custom Search API
- **Capabilities**:
  - Real-time web search for current events
  - News articles and market sentiment
  - Company announcements and press releases
  - General market intelligence

### Example Queries

**Financial Data Queries:**
```
- "What is the current price of AAPL?"
- "Show me Tesla's RSI indicator"
- "What are Apple's latest quarterly earnings?"
- "Give me the top gainers today"
```

**Web Intelligence Queries:**
```
- "What's the latest news about Tesla?"
- "Current tech industry trends"
- "Recent announcements from Microsoft"
```

**Combined Queries (Uses Both Agents):**
```
- "What's Tesla's stock price and recent news?"
- "How did the market react to today's Federal Reserve announcement?"
- "Apple's current stock performance and latest product news"
```

## Project Structure
```
StockSage/
├── chat_orchestrator/          # Main orchestrator agent
│   ├── __init__.py
│   └── agent.py               # Router & synthesizer logic
├── data_researcher_agent/      # Financial data specialist
│   ├── __init__.py
│   ├── agent.py               # Alpha Vantage MCP integration
│   └── .env.example
├── web_intelligence_agent/     # Web research specialist
│   ├── __init__.py
│   ├── agent.py               # Multi-agent web search flow
│   ├── google_search_tool.py  # Google Custom Search wrapper
│   ├── web_scraper_tool.py    # Web scraping utilities
│   ├── tools.py               # Tool exports
│   └── .env.example
├── search.py                   # Standalone search test script
├── .env                        # Environment variables (create this)
├── .gitignore
├── LICENSE
└── README.md
```

## Contributing
We welcome contributions!
1. Fork the repository: [StockSage GitHub](https://github.com/Abhishek-Handibag/StockSage)
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request on [https://github.com/Abhishek-Handibag/StockSage/pulls](https://github.com/Abhishek-Handibag/StockSage/pulls)

## Technical Stack
- **Framework**: Google ADK (Agent Development Kit)
- **LLM**: Gemini 2.5 Flash
- **Financial Data**: Alpha Vantage MCP Server
- **Web Search**: Google Custom Search API
- **Web Scraping**: BeautifulSoup4 + Requests
- **Environment**: Python 3.8+

## Architecture Highlights
- **Multi-Agent Orchestration**: Sequential and loop-based agent flows
- **Intelligent Routing**: Context-aware query analysis and delegation
- **Modular Design**: Each agent is independently deployable and testable
- **MCP Integration**: Model Context Protocol for financial data streaming
- **Tool-Based Actions**: Function tools for search and scraping operations

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions, suggestions, or collaboration:
- **GitHub Repository:** [https://github.com/Abhishek-Handibag/StockSage](https://github.com/Abhishek-Handibag/StockSage)
- **GitHub Issues:** [Open an issue](https://github.com/Abhishek-Handibag/StockSage/issues)

---
**StockSage**: Professional, AI-driven multi-agent stock analysis made simple.

---

**Note:** This project uses cutting-edge multi-agent architecture with Google's ADK framework. The system intelligently combines financial data analysis with web intelligence to provide comprehensive market insights.