import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("STOCK_MARKET_API")
base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&interval=5min&apikey={api_key}'

def get_share_price(ticker_symbol: str) -> str:
    """Fetches the latest share price for the given ticker symbol using Alpha Vantage API. Returns price as string or error message."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker_symbol}&interval=5min&apikey={api_key}'
    try:
        response = requests.get(url)
        data = response.json()
        if "Time Series (5min)" in data:
            time_series = data["Time Series (5min)"]
            latest_timestamp = sorted(time_series.keys())[-1]
            latest_close = time_series[latest_timestamp]["4. close"]
            return f"The latest share price for {ticker_symbol.upper()} is ${float(latest_close):.2f}."
        # Handle various API error messages explicitly
        if "Note" in data:
            return f"API notice: {data['Note']} Please try again later."
        if "Error Message" in data:
            return f"Error: {data['Error Message']} Check if the symbol is correct or try again later."
        return f"Unexpected API response or data format for {ticker_symbol}. ({data})"
    except Exception as e:
        return f"An error occurred while retrieving the price for {ticker_symbol}: {str(e)}"