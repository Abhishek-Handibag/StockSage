"""WebScraper module for web intelligence agent.

Provides page scraping and link scraping utilities.
"""
import logging
import requests
from bs4 import BeautifulSoup

default_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class WebScraper:
    """
    Tool for scraping web pages. Returns HTML content from a URL.
    """
    def __init__(self, logger=None):
        self.logger = logger or default_logger

    def scrape(self, url):
        """
        Scrapes a web page and returns the HTML content.

        Args:
            url (str): URL of the page.

        Returns:
            dict: 'ok', 'html_content', and 'error' fields as applicable.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            self.logger.info("Scraped OK: %s", url)
            return {
                'ok': True,
                'html_content': soup.prettify(),
            }
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to scrape %s: %s", url, str(e))
            return {
                'ok': False,
                'error': str(e),
                'html_content': None,
            }

def get_web_scraper_tool():
    """
    Initializes and returns a WebScraper instance.
    """
    return WebScraper()

def scrape_links(results):
    """
    Scrapes all links from the given search results dict.
    For each result, returns a dict: {title, snippet, html_content, url, error}

    Args:
        results (dict): Dictionary as from GoogleSearchTool.search().

    Returns:
        dict: Dict with 'ok' and 'results' key. Each item is a dict containing 'title', 'snippet', 'html_content', 'url', and 'error' (if applicable).
    """
    scraper = get_web_scraper_tool()
    scraped_results = []
    for result in results.get('results', []):
        scraped = scraper.scrape(result['link'])
        scraped_entry = {
            'title': result.get('title'),
            'snippet': result.get('snippet'),
            'url': result.get('link'),
            'html_content': scraped.get('html_content'),
            'error': scraped.get('error') if not scraped.get('ok') else None
        }
        scraped_results.append(scraped_entry)
    return {
        'ok': True,
        'results': scraped_results,
    }
