# Business Intelligence Studio — W8D2

## 1. Project Overview

Business Intelligence Studio is an interactive customer analytics dashboard developed as part of the Cynaris Data Analyst Internship (Week 8, Day 2).

The application analyses customer data, identifies business performance patterns, generates AI-powered business recommendations and exports an executive PowerPoint presentation.

## 2. Key Features

- Customer dataset upload and validation.
- Interactive city, acquisition channel and age-group filters.
- KPI tracking: total customers, revenue, orders and churn rate.
- City-wise revenue and churn analysis.
- Acquisition channel performance analysis.
- Age-group performance analysis.
- AI-generated executive summaries and five business recommendations.
- Downloadable 11-slide PowerPoint presentation.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Pandas | Data analysis |
| NumPy | Numerical operations |
| Streamlit | Interactive dashboard |
| Plotly | Interactive visualizations |
| Groq API | AI-generated recommendations |
| python-pptx | PowerPoint generation |
| python-dotenv | Environment variable management |

## 4. Dataset Information

Dataset: `da_customer_profiles.csv`

The dataset contains 200 customer records and includes:

- Customer ID
- City
- Age band
- Gender
- Acquisition channel
- First purchase date
- Total orders
- Total revenue
- Last purchase date
- Churn status

## 5. Installation

Activate the project virtual environment and install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 6. Environment Configuration

Create or configure the `.env` file with your Groq API key.

```env
GROQ_API_KEY=your_api_key_here
```

Never commit your actual API key to GitHub.

## 7. Run the Application

Start the dashboard:

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal.

Upload `da_customer_profiles.csv` to begin analysing customer performance.

## 8. AI Recommendations

The application uses the Groq API to generate:

- An executive summary.
- Five data-driven business recommendations.
- Findings, recommended actions and potential benefits.

AI-generated conclusions should be reviewed against the underlying dataset before business decisions are made.

## 9. PowerPoint Export

The dashboard generates an executive presentation containing 11 slides:

1. Business Intelligence Report
2. Executive Summary
3. City Performance
4. Acquisition Channel Performance
5. Age Group Performance
6. Customer Churn
7. Targeted Retention Recommendation
8. Website Acquisition Recommendation
9. App Channel Recommendation
10. Age-Focused Recommendation
11. Offline Channel Recommendation

## 10. Project Structure

```text
week-8-day-2-business-recommendations/
│
├── app.py
├── data_analysis.py
├── ai_recommendations.py
├── generate_presentation.py
├── main.py
├── requirements.txt
├── README.md
├── business_recommendations.txt
└── TESTING_REPORT.md
```

## 11. Known Limitations

- AI recommendations depend on API availability.
- Recommendations are suggestions and require business validation.
- Revenue analysis does not establish profitability.
- The dataset contains only 200 customer records.
- Observed churn patterns do not establish causal relationships.

## 12. Project Outcome

Developed an interactive analytics dashboard combining customer data analysis, visualization, AI-generated business recommendations and executive PowerPoint reporting.