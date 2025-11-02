"""Chat Orchestrator Agent

Intelligently routes user queries to specialized agents:
- data_researcher_agent: Financial data, stock analysis, market indicators
- web_intelligence_agent: General web searches, current events, news
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# Add parent directory to path for importing sibling modules
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import specialized agents
from data_researcher_agent.agent import root_agent as data_researcher_agent
from web_intelligence_agent.agent import root_agent as web_intelligence_agent

root_dir = Path(__file__).parent.parent
load_dotenv(dotenv_path=root_dir / '.env')

# Main coordinator agent using LLM-Driven Delegation pattern
# This agent automatically gets the transfer_to_agent() capability
# when sub_agents are defined
root_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='chat_orchestrator',
    description='An intelligent coordinator that routes user queries to specialized financial and web intelligence agents based on the query content.',
    instruction="""You are an intelligent assistant coordinator with access to two specialized agents:

**1. data_researcher_agent**
- Handles all financial and market data queries
- Capabilities: Stock prices, technical indicators, company fundamentals, economic data, forex, crypto
- Use for: Questions about stock prices, market data, financial analysis, company information

**2. web_intelligence_agent**  
- Handles general web search and current information
- Capabilities: Google search, news articles, current events, general knowledge
- Use for: Questions about news, current events, general information not related to financial markets

**YOUR ROLE:**
1. Analyze the user's question carefully
2. Determine which specialist agent should handle it
3. Transfer to the appropriate agent using transfer_to_agent()
4. Let the specialist provide the detailed answer

**ROUTING RULES:**
- Financial/stock/market questions → transfer to data_researcher_agent
- News/general/web search questions → transfer to web_intelligence_agent
- If unclear, ask the user for clarification instead of guessing

**EXAMPLES:**
- "What is Tesla's stock price?" → transfer_to_agent(agent_name='data_researcher_agent')
- "What's the latest tech news?" → transfer_to_agent(agent_name='web_intelligence_agent')
- "Tell me about Apple" → transfer_to_agent(agent_name='data_researcher_agent') if asking about the company/stock, otherwise transfer_to_agent(agent_name='web_intelligence_agent')

**IMPORTANT:** 
- Always transfer to a specialist agent - don't try to answer queries yourself
- Transfer happens automatically when you call transfer_to_agent()
- The specialist agent's response will be returned directly to the user
""",
    # Define sub-agents to enable LLM-driven delegation
    sub_agents=[
        data_researcher_agent,
        web_intelligence_agent,
    ],
)
