import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams
# from stock_analyzer.stock import get_share_price

load_dotenv()
api_key = os.getenv("STOCK_MARKET_API")

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[
        MCPToolset(connection_params=StreamableHTTPConnectionParams(
            url=f"https://mcp.alphavantage.co/mcp?apikey={api_key}"
        ))
    ],
)
