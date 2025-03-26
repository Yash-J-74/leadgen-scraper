# LeadGen Scraper Tool

## Overview
The **LeadGen Scraper Tool** is a web scraping application that extracts business details (such as name, type, address, phone number, website, and rating) from Google Maps. Additionally, it identifies competitors and allows users to search for multiple businesses of the same type in a given area.

## Features
- Extracts business details from Google Maps
- Identifies competitors based on business type and location
- Searches for multiple businesses of the same type within a specified area

## Tech Stack Used
- **Python Playwright** - Web scraping
- **FastAPI** - Backend API
- **Streamlit** - Frontend UI

# Setup Instructions
- Clone the repository
```bash
git clone https://github.com/Yash-J-74/leadgen-scraper.git
cd leadgen-scraper
```
- Run the __init__.py file to set up the virtual environment, install dependencies, and create a .env file:
```bash
python __init__.py
```
The virtual environment must be running now
- Update the .env file with the API URL (usually http://127.0.0.1:8000).
- Run the application using the command:
```bash
python run_app.py
```

- To close the app, press Ctrl+C in the terminal.
