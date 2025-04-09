"""
Alternative API for Yahoo Finance data when web scraping is blocked.
This file provides a fallback method for retrieving stock data.
"""

import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def get_stock_data_from_api(ticker, start_date, end_date):
    """
    Get stock data from yfinance API as a fallback method
    
    Args:
        ticker (str): Stock ticker symbol (e.g., AAPL)
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
    Returns:
        DataFrame: Historical stock data or None if error
    """
    try:
        logger.info(f"Fetching data for {ticker} from yfinance API")
        
        # Get data from yfinance
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            logger.error(f"No data returned from yfinance for {ticker}")
            return None
            
        # Reset index to make Date a column
        data = data.reset_index()
        
        # Make column names match our expected format
        data.columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        
        return data
        
    except Exception as e:
        logger.error(f"Error fetching data from yfinance: {str(e)}")
        return None