# W8D4 – Production Deployment and Application Documentation

## Project
Business Intelligence Studio – Customer Analytics Dashboard

## Overview
An interactive Streamlit application for customer analytics, business performance monitoring, AI-generated recommendations and PowerPoint reporting.

## Features
- CSV upload and validation
- Customer, revenue and order KPIs
- City-wise revenue and churn analysis
- Acquisition channel analysis
- Age-group analysis
- Interactive Plotly charts
- Groq AI executive summary and recommendations
- PowerPoint report export

## Technology Stack
- Python
- Streamlit
- Pandas and NumPy
- Plotly
- Groq API
- python-pptx
- python-dotenv

## Installation

1. Clone or copy the project.
2. Install dependencies:

   `python -m pip install -r requirements.txt`

3. Configure the environment variable:

   `GROQ_API_KEY=your_api_key`

4. Never commit `.env` or API credentials.

## Run Locally

`python -m streamlit run app.py`

Open the local URL displayed by Streamlit.

## Configuration
The application reads GROQ_API_KEY from environment variables or a local .env file.

## Deployment Status
Local deployment tested successfully.

External production deployment is pending authorization because the internship project is subject to confidentiality restrictions.

## API Documentation
This project currently exposes a Streamlit user interface, not a REST API. No HTTP API endpoints are claimed.

## Testing
- Python syntax validation
- Local Streamlit application startup
- Dashboard loading
- CSV upload and analytics functionality

## Known Limitations
- AI recommendations require Groq API access.
- Input CSV must contain the required customer columns.
- AI-generated recommendations require human review.
- Revenue does not establish profitability.
- Public hosting requires written authorization.

## Security
- Keep API keys in environment variables or deployment secrets.
- Never commit credentials.
- Do not publish confidential datasets or project files.

## Project Context
Cynaris Data Analyst Internship – Week 8 Day 4.
