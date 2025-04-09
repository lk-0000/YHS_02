import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import datetime
import time
import logging
import random  # For random user agent selection

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
        # List of user agents to rotate through (helps prevent blocking by Yahoo)
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        ]
        
        # Choose a random user agent - this helps avoid detection on Render.com
        user_agent = random.choice(user_agents)
        
        # Enhanced headers to look more like a real browser
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://finance.yahoo.com/',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',  # Do Not Track
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate', 
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1'
        }
        
        logger.info(f"Requesting data from: {url}")
        
        # Add retry mechanism
        max_retries = 3
        retry_delay = 2  # seconds
        response = None
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    break
                
                logger.warning(f"Attempt {attempt+1}/{max_retries} failed with status code {response.status_code}.")
                
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request exception on attempt {attempt+1}/{max_retries}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
        
        # Check if we got a valid response
        if response is None:
            logger.error("All request attempts failed.")
            return None
            
        if response.status_code != 200:
            logger.error(f"Failed to retrieve page after {max_retries} attempts: Status code {response.status_code}")
            return None
        
        # Debug response content
        logger.debug(f"Response content length: {len(response.text)}")
        logger.debug(f"Response content preview: {response.text[:200]}...")
        
        # Check for anti-scraping messages
        if "Please try again later" in response.text or "Access Denied" in response.text:
            logger.error("Detected anti-scraping message in response")
            logger.error("The server may be blocking requests from Render.com's IP addresses")
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table - it comes after the marker in the HTML
        table_body = soup.find('tbody')
        
        if not table_body:
            logger.error("Could not find the table body in the HTML")
            
            # Check for alternative structures
            # Sometimes the data might be embedded in JSON/JavaScript
            for script in soup.find_all('script'):
                if script.string and "HistoricalPriceStore" in script.string:
                    logger.info("Found data in JavaScript. Attempting to extract...")
                    # This would require parsing JavaScript, which is more complex
                    # but flagging that we found the data in a different format
            
            # Output more of the HTML for deeper investigation
            logger.debug(f"HTML title: {soup.title.string if soup.title else 'No title found'}")
            logger.debug(f"HTML body preview: {soup.body.get_text()[:500] if soup.body else 'No body found'}...")
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
