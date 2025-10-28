"""GoogleSearchTool module for web intelligence agent.

Provides GoogleSearchTool and initializer for custom web search.
"""
import os
import logging
import requests
from pathlib import Path
from dotenv import load_dotenv

root_dir = Path(__file__).parent.parent
load_dotenv(dotenv_path=root_dir / '.env')
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class GoogleSearchTool:
    """
    A tool for performing Google searches using the Custom Search API.
    """
    def __init__(self, api_key, engine_id, search_url="https://www.googleapis.com/customsearch/v1"):
        """
        Initialize GoogleSearchTool.

        Args:
            api_key (str): Google API key.
            engine_id (str): Custom Search Engine ID.
            search_url (str): API URL (optional override).
        """
        self.api_key = api_key
        self.engine_id = engine_id
        self.search_url = search_url

    def search(self, query):
        """
        Performs a Google search and returns the results.

        Args:
            query (str): Search query.

        Returns:
            dict: Search results or error info.
        """
        params = {
            'key': self.api_key,
            'cx': self.engine_id,
            'q': query
        }
        try:
            response = requests.get(self.search_url, params=params)
            response.raise_for_status()
            search_results = response.json()
            items = search_results.get('items', [])
            results = []
            for item in items:
                results.append({
                    'title': item.get('title'),
                    'snippet': item.get('snippet'),
                    'link': item.get('link'),
                })
            response_to_return = {
                'ok': True,
                'results': results,
            }
            logger.info("Google search succeeded: %s results", len(results))
            return response_to_return
        except requests.exceptions.RequestException as e:
            logger.error("Google search failed: %s", str(e))
            error_response = {
                'ok': False,
                'error': str(e),
                'results': []
            }
            return error_response

def get_google_search_tool():
    """
    Initializes and returns GoogleSearchTool from environment variables.
    Raises ValueError if vars unset.
    """
    api_key = os.environ.get('GOOGLE_SEARCH_API_KEY')
    engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
    search_url = os.environ.get('GOOGLE_CUSTOM_SEARCH_URL')
    if not api_key:
        logger.critical('GOOGLE_SEARCH_API_KEY not set')
        raise ValueError("GOOGLE_SEARCH_API_KEY environment variable not set.")
    if not engine_id:
        logger.critical('GOOGLE_SEARCH_ENGINE_ID not set')
        raise ValueError("GOOGLE_SEARCH_ENGINE_ID environment variable not set.")
    return GoogleSearchTool(api_key, engine_id, search_url) if search_url else GoogleSearchTool(api_key, engine_id)
