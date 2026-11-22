# W10D4 — Real Estate Forecasting Dashboard

## Overview
Interactive Streamlit dashboard using Plotly to visualize historical monthly average property listing prices and existing Prophet forecasts.

## Technology
- Python
- Pandas
- Plotly
- Streamlit
- Prophet forecast outputs generated in W10D2

## Data Sources
- Original real estate listings dataset
- Existing Prophet forecast CSV
- Existing forecast evaluation CSV

## Features
- Historical monthly average price visualization
- Prophet forecast with uncertainty interval
- City and property-type filters for historical listings
- Forecast horizon selector
- Model evaluation table
- KPI summary

## Run Locally
Install dependencies:

```bash
pip install -r requirements.txt
```

Launch:

```bash
python -m streamlit run app.py
```

## Model Limitations
The evaluation file contains three test observations (October–December 2024). Performance metrics should be interpreted cautiously. The future forecast is based on the original overall dataset model and is not recalculated for individual city or property filters.
