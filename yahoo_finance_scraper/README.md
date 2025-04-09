# Yahoo Finance Scraper

A Flask web application for scraping and visualizing Yahoo Finance historical stock data with downloadable reports.

## Features

- Retrieve historical stock data from Yahoo Finance
- Interactive data visualizations with Chart.js
- Tabular data display with DataTables
- Excel file download functionality
- Responsive Bootstrap-based UI

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
   
## Usage

1. Enter a stock ticker symbol (e.g., AAPL for Apple)
2. Select a date range
3. Click "Get Stock Data" to retrieve and visualize the data
4. Toggle between chart and table views
5. Download the data as an Excel file

## Dependencies

- Flask: Web framework
- BeautifulSoup4: HTML parsing
- Pandas: Data manipulation
- Chart.js: Data visualization
- DataTables: Interactive tables
- XlsxWriter: Excel file generation

## License

This project is for educational purposes only. Not affiliated with Yahoo Finance.