import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import Agent
from google.adk.tools import FunctionTool
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

load_dotenv()
api_key = os.getenv("STOCK_MARKET_API")

root_agent = Agent(
    model='gemini-2.5-flash',
    name='data_researcher_agent',
    description='An expert financial assistant specialized in analyzing stock market data and answering investment-related questions accurately.',
    instruction="""
    "You are an AI financial expert with deep knowledge of the global stock market, "
    "equities, indices, technical indicators, and market analysis principles. "
    "Your responses must be strictly based on verified data obtained through the "
    "MCPToolset connection to the stock market data MCP Server. "
    "Only answer a question if the proper and relevant data is successfully retrieved "
    "via this connection. "
    "If sufficient or valid data cannot be obtained, politely decline to answer and "
    "inform the user that reliable data is not available at the moment. "

    "When you do respond, analyze the retrieved data deeply and explain your reasoning "
    "step-by-step. Use appropriate financial terminology, clear structure, and "
    "educational explanations. Include metrics such as price trends, volume, volatility, "
    "moving averages, RSI, or other relevant indicators when applicable. "
    "Provide factual, data-driven insights — never speculate or provide personal financial advice. "
    "Maintain a professional, objective, and informative tone at all times."
    """,
    tools=[
        MCPToolset(connection_params=StreamableHTTPConnectionParams(
            url=f"https://mcp.alphavantage.co/mcp?apikey={api_key}"
        ))
    ],
)