# -- tools.py (entry point for web agent tools) --
"""
Tool entry point for web intelligence agent. Imports Google and web scraping tools.
"""

from .google_search_tool import GoogleSearchTool, get_google_search_tool
from .web_scraper_tool import WebScraper, get_web_scraper_tool, scrape_links