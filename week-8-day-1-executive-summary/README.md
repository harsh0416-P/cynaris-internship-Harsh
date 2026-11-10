# W8D1 – Executive Summary Generation

## Project Overview

This project automates customer data analysis and executive report generation using Python, Pandas, the Groq API, and python-pptx.

## Workflow

1. Load a customer CSV dataset.
2. Validate required columns and data quality.
3. Calculate five business insights.
4. Generate an executive summary using the Groq API.
5. Export a seven-slide PowerPoint presentation.

## Dataset

- Records: 200 customers
- Columns: 10
- Missing values: 0
- Duplicate customer IDs: 0

## Business Insights

- Revenue by city
- Revenue by acquisition channel
- Revenue by age group
- Customer churn
- Customer value and order metrics

## Technologies

- Python
- Pandas
- Groq API
- python-pptx
- python-dotenv

## Project Files

- `run_pipeline.py` – Integrated application
- `executive_summary.py` – Executive summary implementation
- `generate_presentation.py` – PowerPoint generation
- `executive_summary.txt` – Generated summary
- `executive_summary.pptx` – Seven-slide presentation

## Execution

Activate the virtual environment and run:

```powershell
python run_pipeline.py "..\project 1 Stakeholder brief + data inventory\data\da_customer_profiles.csv"
```

The `.env` file must contain a valid `GROQ_API_KEY`. Never commit API credentials.

## Validation

The customer dataset passed the required-column validation and the integrated pipeline successfully generated the executive summary and seven-slide PowerPoint presentation.

## Limitations

The dataset contains customer revenue and a churn flag, but does not provide acquisition costs, profit margins, churn reasons, or churn periods. Recommendations should be interpreted as suggestions for further investigation.
