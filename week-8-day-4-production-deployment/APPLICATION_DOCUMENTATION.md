# W8D4 – Application Interface Documentation

## 1. Application Overview
Business Intelligence Studio is a Streamlit-based customer analytics application.

## 2. Interface Entry Point
Application file: app.py

Run command:
python -m streamlit run app.py

## 3. Input Interface

Input type: CSV file

Required columns:
- Customer_ID
- City
- Age_Band
- Acquisition_Channel
- Total_Orders
- Total_Revenue
- Churned

## 4. Application Processing

1. User uploads a CSV file.
2. Application validates the dataset.
3. Pandas calculates customer and revenue metrics.
4. Streamlit displays KPIs and interactive charts.
5. Groq generates an executive summary and five recommendations when requested.
6. python-pptx generates a downloadable PowerPoint report.

## 5. Configuration

Environment variable:
GROQ_API_KEY

The key must be configured securely and must never be included in source control.

## 6. HTTP API Status

This application does not currently expose REST API endpoints.
Its interface is provided through Streamlit.
No undocumented HTTP endpoints are assumed.

## 7. Error Handling

- Invalid CSV: display dataset validation error.
- Missing API key: report configuration error.
- Groq failure: display AI generation error.
- PowerPoint failure: display export error.

## 8. Security

Do not expose API keys, confidential customer data or private project files.
External deployment requires appropriate authorization.
