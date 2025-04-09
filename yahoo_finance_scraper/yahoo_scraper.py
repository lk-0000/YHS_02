import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def get_period_timestamps(start_date, end_date):
    """
    Convert date strings to timestamps for Yahoo Finance URL
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        
    Returns:
        tuple: (period1, period2) timestamps for Yahoo Finance URL
    """
    try:
        # Convert to datetime objects
        start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        
        # Add a day to end_date to make it inclusive
        end_dt = end_dt + datetime.timedelta(days=1)
        
        # Convert to timestamps (seconds since epoch)
        period1 = int(start_dt.timestamp())
        period2 = int(end_dt.timestamp())
        
        return period1, period2
    except Exception as e:
        logger.error(f"Error converting dates to timestamps: {str(e)}")
        # Default to last 30 days if there's an error
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - (30 * 24 * 60 * 60)
        return start_timestamp, end_timestamp

def scrape_yahoo_finance_history(url):
    """
    Scrape historical data from Yahoo Finance and return as DataFrame
    
    Args:
        url (str): Yahoo Finance historical data URL
        
    Returns:
        DataFrame: Historical stock data
    """
    try:
        # Send request to get the page content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        logger.info(f"Requesting data from: {url}")
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logger.error(f"Failed to retrieve page: Status code {response.status_code}")
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table - it comes after the marker in the HTML
        table_body = soup.find('tbody')
        
        if not table_body:
            logger.error("Could not find the table body in the HTML")
            logger.debug(f"HTML content: {soup.prettify()[:500]}...")  # Log a sample of the HTML for debugging
            return None
        
        # Extract data from table rows
        data = []
        rows = table_body.find_all('tr') if table_body else []
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 7:  # Ensure we have enough columns
                row_data = [cell.text.strip() for cell in cells]
                data.append(row_data)
        
        if not data:
            logger.error("No data found in the table")
            return None
        
        # Create DataFrame
        columns = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        df = pd.DataFrame(data, columns=columns)
        
        # Clean data and convert types
        for col in ["Open", "High", "Low", "Close", "Adj Close"]:
            # Replace any non-numeric chars except decimal point and try to convert
            df[col] = df[col].replace('[^0-9.-]', '', regex=True)
            # Handle any remaining conversion errors
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert Volume to numeric (remove commas and convert)
        df["Volume"] = df["Volume"].replace('[^0-9]', '', regex=True)
        df["Volume"] = pd.to_numeric(df["Volume"], errors='coerce')
        
        # Convert Date to datetime
        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        
        # Drop any rows with NaN values
        df = df.dropna()
        
        if df.empty:
            logger.error("DataFrame is empty after cleaning")
            return None
            
        return df
    except Exception as e:
        logger.error(f"Error in scrape_yahoo_finance_history: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None
