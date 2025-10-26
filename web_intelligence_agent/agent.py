"""Agent orchestration module for web intelligence.

Defines agent assembly for query optimization, Google search, and web scraping using sequential and looping constructs.
"""

from google.adk.agents import SequentialAgent, LlmAgent, LoopAgent
from .tools import get_google_search_tool, scrape_links
# from .tools import scrape_links  # Commented out for now - web scraper functionality
from dotenv import load_dotenv
import json

load_dotenv()

search_tool = get_google_search_tool()

def google_search_action(query: str) -> dict:
    """
    Search Google for the latest information.
    Returns up to 10 search results with title, snippet, and URL.

    Args:
        query (str): The search query string.

    Returns:
        dict: Search results with metadata.
    """
    result = search_tool.search(query)
    print('google_search_response:', result)
    return result

# def scrape_links_action(results: dict) -> dict:
#     """
#     Scrape the links from the search results.
# 
#     Args:
#         results (dict): Google search result dictionary.
# 
#     Returns:
#         dict: Same results format, but with HTML content for each link.
#     """
#     response = scrape_links(results)
#     print('web_scraper_response:', json.dumps(response, indent=2))
#     return response

optimizer_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='optimizer_agent',
    description='An agent that synthesizes gathered information into a comprehensive answer for the user. You receive data from the data_gatherer_agent and provide optimized answers.',
    instruction=(
        "You are an answer synthesizer. Your job is to take the information gathered by the data_gatherer_agent and provide a clear, comprehensive, and optimized answer to the user's original question. "
        "Review the gathered data, extract the most relevant information, and present it in a well-structured and easy-to-understand format. "
        "You may be called multiple times in a loop if more information is needed. In such cases, refine your answer based on new data."
    ),
)

data_gatherer_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='data_gatherer_agent',
    description='An agent that gathers data from Google search based on user questions. You search for information and provide comprehensive data to the optimizer_agent.',
    instruction=(
        "You are a data gatherer. Your job is to take the user's question and search Google for relevant information. "
        "Search Google using the user's question (or an optimized version of it) and gather comprehensive information. "
        "Provide detailed search results including titles, snippets, and URLs in a structured format. "
        "You may be called multiple times if the optimizer_agent needs more specific information. "
        "Focus on gathering accurate and relevant data from reliable sources."
    ),
    tools=[google_search_action],
)

search_and_scrape_sequence = SequentialAgent(
    sub_agents=[
        data_gatherer_agent,
        optimizer_agent,
    ],
    name='search_and_scrape_sequence',
    description='A sequence where data_gatherer_agent first searches for information, then optimizer_agent synthesizes an optimized answer. This sequence may run iteratively in a loop, gathering additional data and refining answers across multiple passes.',
)

root_agent = LoopAgent(
    name='root_agent',
    sub_agents=[search_and_scrape_sequence],
    description='A looping agent that runs the search and scrape sequence iteratively, allowing agents to refine and update results across multiple iterations.',
    max_iterations=3,
)