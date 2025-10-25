import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleSearchTool:
    """A tool for performing Google searches."""
    def __init__(self, api_key, engine_id, search_url="https://www.googleapis.com/customsearch/v1"):
        self.api_key = api_key
        self.engine_id = engine_id
        self.search_url = search_url

    def search(self, query):
        """Performs a Google search and returns the results."""
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
            print(response_to_return)
            return response_to_return
        except requests.exceptions.RequestException as e:
            error_response = {
                'ok': False,
                'error': str(e),
                'results': []
            }
            print(error_response)
            return error_response

def get_google_search_tool():
    """Initializes the GoogleSearchTool with API key and engine ID from environment variables."""
    api_key = os.environ.get('GOOGLE_SEARCH_API_KEY')
    engine_id = os.environ.get('GOOGLE_SEARCH_ENGINE_ID')
    search_url = os.environ.get('GOOGLE_CUSTOM_SEARCH_URL')
    
    if not api_key:
        raise ValueError("GOOGLE_SEARCH_API_KEY environment variable not set.")
    if not engine_id:
        raise ValueError("GOOGLE_SEARCH_ENGINE_ID environment variable not set.")
    
    return GoogleSearchTool(api_key, engine_id, search_url) if search_url else GoogleSearchTool(api_key, engine_id)