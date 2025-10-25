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

query_optimizer_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='query_optimizer_agent',
    description='An agent that refines user queries for Google search and synthesizes the final answer. You may be called multiple times in a loop, receiving updated queries or results.',
    instruction=(
        "You are a query optimizer. Your job is to iteratively refine the user's query for a better Google search experience. "
        "You may receive updated queries or search results in a loop, and should synthesize a final answer to the user's original query, "
        "taking into account new information from each iteration. Avoid redundant actions and build on previous results."
    ),
)

data_gatherer_agent = LlmAgent(
    model='gemini-2.5-flash',
    name='data_gatherer_agent',
    description='An agent that gathers data from Google search and scrapes the content of the links. You may be called repeatedly in a loop, receiving updated queries or instructions.',
    instruction=(
        "You are a data gatherer. Your job is to use the provided query to search Google and provide comprehensive information based on the search results. "
        "Summarize and include in your response a structured list of the links with their title, snippet, and url. "
        "You may be called multiple times in a loop, and should update your data gathering based on new queries or instructions. "
        "Avoid repeating work unnecessarily and build on previous iterations."
    ),
    tools=[google_search_action],  # scrape_links_action commented out for now
)

search_and_scrape_sequence = SequentialAgent(
    sub_agents=[
        query_optimizer_agent,
        data_gatherer_agent,
    ],
    name='search_and_scrape_sequence',
    description='A sequence of agents that searches Google and scrapes the results. This sequence may run iteratively in a loop, refining queries and gathering data across multiple passes.',
)

root_agent = LoopAgent(
    name='root_agent',
    sub_agents=[search_and_scrape_sequence],
    description='A looping agent that runs the search and scrape sequence iteratively, allowing agents to refine and update results across multiple iterations.',
    max_iterations=3,
)