# GitHub Pages Setup Instructions

This document provides instructions for setting up this project with GitHub Pages.

## Setting Up GitHub Pages

1. **Push to GitHub**: Push this repository to GitHub under your account.

2. **Enable GitHub Pages**: 
   - Go to your repository on GitHub
   - Click on "Settings"
   - Scroll down to the "GitHub Pages" section
   - Under "Source", select the branch "gh-pages" (this will be created by the GitHub Action)
   - Click "Save"

3. **GitHub Action**: 
   - The repository includes a GitHub Action workflow file (`.github/workflows/github-pages.yml`)
   - This action automatically publishes the contents of the `docs` folder to the `gh-pages` branch
   - The first time you push to the repository, the action will run and create the `gh-pages` branch

4. **Custom Domain** (Optional):
   - If you have a custom domain you want to use:
     - Replace the contents of `docs/CNAME` with your custom domain
     - In your GitHub Pages settings, add your custom domain
     - Configure your DNS provider with the appropriate GitHub Pages records

5. **Wait for Deployment**:
   - After enabling GitHub Pages, it may take a few minutes for your site to be published
   - You can check the status in the "GitHub Pages" section of your repository settings
   - Once published, the site will be available at `https://[your-username].github.io/yahoo-finance-scraper/`

## Local Testing

To test the static site locally before pushing to GitHub:

1. Open the `docs/index.html` file directly in your browser
2. The static demo should work with the included demo data

## Making Changes

When making changes to the static demo:

1. Edit files in the `docs` folder
2. Test locally by opening `docs/index.html` in your browser
3. Push changes to GitHub
4. The GitHub Action will automatically update the deployed site

## Demo Data vs. Real Application

Remember that the GitHub Pages version uses demo data and does not have the backend scraping functionality. To use the full application:

1. Clone the repository
2. Follow the installation instructions in the main README.md
3. Run the application locally or deploy to a server that supports Python