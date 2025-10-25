from google.adk.agents.llm_agent import Agent
from .tools import get_google_search_tool
from google.adk.agents import SequentialAgent, LlmAgent
from dotenv import load_dotenv

load_dotenv()

search_tool = get_google_search_tool()

def google_search_action(query: str) -> dict:
    """Search Google for the latest information. Returns up to 10 search results with title, snippet, and URL."""
    result = search_tool.search(query)
    print(result)
    return result

root_agent = Agent(
    model='gemini-2.5-flash',
    name='web_intelligence_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions related to the latest news and information using google search.',
    tools=[google_search_action],
)
