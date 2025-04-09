# Deploying to Render.com

This document guides you through the process of deploying the Yahoo Finance Scraper to Render.com.

## Option 1: One-Click Deploy (Recommended)

1. Make sure you have a Render account and are logged in
2. Click this button: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
3. Select the repository with your Yahoo Finance Scraper code
4. Render will automatically use the settings from `render.yaml`

## Option 2: Manual Deployment

1. Log in to [Render.com](https://render.com)
2. From your dashboard, click "New" and select "Web Service"
3. Connect your repository or upload files directly
4. Fill in the following configuration:

   - **Name**: yahoo-finance-scraper (or any name you prefer)
   - **Environment**: Python
   - **Region**: Choose one closest to your location
   - **Branch**: main (or your preferred branch)
   - **Build Command**: `pip install -r render-requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --reuse-port main:app`

5. Add the following environment variables:
   - `SESSION_SECRET`: [Generate a random string]
   - `FLASK_ENV`: production
   - `CACHE_TYPE`: SimpleCache
   - `CACHE_DEFAULT_TIMEOUT`: 1800
   - `LOG_LEVEL`: INFO

6. Click "Create Web Service"

## Special Considerations for Render.com

1. **Free Tier Limitations**: Free instances will spin down after 15 minutes of inactivity. This means the first request after inactivity will be slower.

2. **Anti-Scraping Measures**: Yahoo Finance may block Render.com IP addresses. The application is configured to automatically fall back to the yfinance API when scraping fails.

3. **Scaling**: If you need more performance, consider upgrading to a paid plan on Render.com.

4. **Logs**: You can view application logs by clicking on your service in the Render dashboard and selecting the "Logs" tab.

5. **Custom Domains**: In the paid plan, you can add a custom domain to your application.

## Troubleshooting

- **Application Error**: Check the logs for specific error messages
- **Slow Initial Load**: This is normal for free tier as the app spins up
- **No Data Returned**: Ensure you're using correct ticker symbols (e.g., "AAPL" for Apple)
- **Deployment Failures**: Ensure all dependencies are properly listed in render-requirements.txt