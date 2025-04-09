# Yahoo Finance Scraper

A Flask web application for scraping and visualizing Yahoo Finance historical stock data with downloadable reports.

![Yahoo Finance Scraper](static/img/screenshot.svg)

## Static Demo

A static demonstration of the UI is available on GitHub Pages:
- [View Static Demo](https://YOUR_USERNAME.github.io/yahoo-finance-scraper/)

The static demo showcases the UI and interactions using demo data for AAPL, MSFT, and GOOG stocks.

## Features

- Retrieve historical stock data from Yahoo Finance
- Interactive data visualizations with Chart.js
- Tabular data display with DataTables
- Excel file download functionality
- Responsive Bootstrap-based UI

## Installation

1. Clone this repository
   ```
   git clone https://github.com/YOUR_USERNAME/yahoo-finance-scraper.git
   cd yahoo-finance-scraper
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python main.py
   ```
   
4. Open your browser to http://localhost:5000

## Usage

1. Enter a stock ticker symbol (e.g., AAPL for Apple)
2. Select a date range
3. Click "Get Stock Data" to retrieve and visualize the data
4. Toggle between chart and table views
5. Download the data as an Excel file

## Repository Structure

- `/` - Main Python application (Flask backend)
- `/docs` - Static HTML version for GitHub Pages
- `/static` - CSS, JavaScript, and images
- `/templates` - HTML templates for Flask

## Dependencies

- Flask: Web framework
- BeautifulSoup4: HTML parsing
- Pandas: Data manipulation
- Chart.js: Data visualization
- DataTables: Interactive tables
- XlsxWriter: Excel file generation

## License

This project is available under the MIT License. See the [LICENSE](LICENSE) file for more info.

## Disclaimer

This project is for educational purposes only. Not affiliated with Yahoo Finance.