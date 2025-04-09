# Contributing to Yahoo Finance Scraper

Thank you for considering contributing to the Yahoo Finance Scraper project!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/yahoo-finance-scraper.git`
3. Create a branch for your feature: `git checkout -b feature-name`
4. Install dependencies: `pip install -r requirements.txt`

## Structure

The project consists of two main parts:
1. **Python Backend**: A Flask application that handles web scraping and data processing.
2. **Static Demo**: A pure HTML/CSS/JS demo in the `/docs` folder for GitHub Pages.

## Contributing to the Backend

The backend is built with Flask and uses Beautiful Soup for web scraping. Files of interest:
- `yahoo_scraper.py`: Contains the scraping logic
- `app.py`: Flask routes and application logic
- `templates/`: HTML templates
- `static/`: CSS, JavaScript, and images

## Contributing to the Static Demo

The static demo in the `/docs` folder is for GitHub Pages. When making changes to the backend application, consider if the changes should also be reflected in the static demo:
- `docs/index.html`: Main HTML file
- `docs/js/script.js`: JavaScript for the demo
- `docs/js/demo-data.js`: Mock data for demonstration

## Testing

Before submitting a pull request:
1. Test the application locally
2. Ensure code is properly formatted
3. Update documentation if necessary

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Increase version numbers in any example files and the README.md to the new version
3. Submit your pull request with a clear description of the changes

## Code of Conduct

Please note that this project has a Code of Conduct. By participating, you are expected to uphold this code.

## Questions?

Feel free to open an issue if you have any questions about contributing.