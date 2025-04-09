import os
import logging
from datetime import datetime, timedelta
from functools import wraps
from urllib.parse import quote

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, Response, flash
from flask_caching import Cache
import pandas as pd
import io

from yahoo_scraper import scrape_yahoo_finance_history, get_period_timestamps
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure cache
cache_config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300  # 5 minutes
}
app.config.from_mapping(cache_config)
cache = Cache(app)

@app.route('/')
def index():
    """Render the main page with the form"""
    # Default date range (30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    return render_template('index.html', 
                           start_date=start_date.strftime('%Y-%m-%d'),
                           end_date=end_date.strftime('%Y-%m-%d'))

@app.route('/scrape', methods=['POST'])
def scrape():
    """Handle form submission and scrape data"""
    try:
        # Get form data
        ticker = request.form.get('ticker', '').strip().upper()
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        
        # Validate inputs
        if not ticker:
            flash("Please enter a ticker symbol", "danger")
            return redirect(url_for('index'))
        
        # Convert dates to timestamps for Yahoo Finance URL
        period1, period2 = get_period_timestamps(start_date, end_date)
        
        # Create Yahoo Finance URL
        url = f"https://finance.yahoo.com/quote/{ticker}/history/?period1={period1}&period2={period2}"
        
        # Check cache first
        cache_key = f"{ticker}_{period1}_{period2}"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            logger.debug(f"Using cached data for {ticker}")
            df = cached_data
            source = "cache"
        else:
            # Scrape data
            logger.debug(f"Scraping new data for {ticker}")
            df = scrape_yahoo_finance_history(url)
            
            if df is None or df.empty:
                flash(f"No data found for {ticker} in the selected date range", "warning")
                return redirect(url_for('index'))
            
            # Cache the result
            cache.set(cache_key, df)
            source = "scrape"
        
        # Store in session for download
        session['last_df'] = df.to_json(orient='split', date_format='iso')
        session['ticker'] = ticker
        
        # Format data for display
        data_for_template = {
            'ticker': ticker,
            'data': df.to_dict('records'),
            'start_date': start_date,
            'end_date': end_date,
            'source': source
        }
        
        return render_template('results.html', **data_for_template)
    
    except Exception as e:
        error_msg = f"Error scraping data: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        flash(error_msg, "danger")
        return redirect(url_for('index'))

@app.route('/download')
def download():
    """Download the last scraped data as Excel"""
    if 'last_df' not in session or 'ticker' not in session:
        flash("No data available for download", "warning")
        return redirect(url_for('index'))
    
    try:
        # Retrieve the data from the session
        df = pd.read_json(session['last_df'], orient='split')
        ticker = session['ticker']
        
        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name=f"{ticker} History", index=False)
            
            # Configure workbook
            workbook = writer.book
            worksheet = writer.sheets[f"{ticker} History"]
            
            # Format for dates
            date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
            worksheet.set_column('A:A', 12, date_format)
            
            # Format for numbers
            number_format = workbook.add_format({'num_format': '0.00'})
            worksheet.set_column('B:F', 12, number_format)
            
            # Format for volume
            volume_format = workbook.add_format({'num_format': '#,##0'})
            worksheet.set_column('G:G', 15, volume_format)
        
        # Set file for download
        output.seek(0)
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{ticker}_historical_data_{today}.xlsx"
        
        return Response(
            output.read(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    except Exception as e:
        error_msg = f"Error generating Excel file: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        flash(error_msg, "danger")
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500 error occurred: {str(e)}")
    logger.error(traceback.format_exc())
    return render_template('index.html', error="Internal server error"), 500
