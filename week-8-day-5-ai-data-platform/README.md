# W8D5 — AI Data Platform: Full Demo and Documentation

## Project Overview

This project extends the Week 8 EDA work with data quality validation, business insights, reusable summary exports, and visual reporting.

## Dataset

- Dataset: Indian Real Estate Listings
- Records: 600
- Columns: 15
- Missing values: 0
- Duplicate rows: 0

**Note:** The dataset is an Indian real-estate listings dataset. Its equivalence to the portal's assigned Indian Business Dataset has not been confirmed.

## Technology Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook

## Analysis Performed

1. Dataset overview and structure
2. Missing-value validation
3. Duplicate-record validation
4. City-wise average property price
5. Property-type price comparison
6. Transaction distribution
7. Sales-status analysis
8. Market-duration analysis

## Key Findings

- Bengaluru has the highest average property price among the listed cities.
- Ahmedabad has the lowest average property price.
- Villas have the highest average price among property types.
- Plots have the lowest average price among property types.
- Average property price: ₹229.10 lakh.
- Average days on market: 183.70 days.

## Generated Outputs

- `eda_outputs/w8d5_business_summary.csv`
- `charts/city_average_prices.png`
- `charts/property_type_prices.png`
- `charts/market_duration.png`

## Data Limitations

- Price consistency issues were identified in the earlier EDA.
- Some rental listings have a sold status, requiring clarification.
- Average listing price does not establish profitability.
- Findings describe this dataset and should not be generalized to the entire Indian property market.
- Dataset equivalence to the assigned Indian Business Dataset remains unconfirmed.

## Run Locally

Install the required packages:

```bash
pip install pandas numpy matplotlib jupyter
```

Open the notebook:

```bash
jupyter notebook
```

Run all cells from top to bottom.

## Deployment and Confidentiality

This project is maintained as a local internship deliverable. External deployment and publication require written authorization under the project confidentiality policy.

## Internship

Cynaris Data Analyst Internship — Week 8 Day 5.
## Key Business Insights

| Metric | Value |
|---|---:|
| Total Properties | 600 |
| Average Property Price | ₹229.1 lakh |
| Average Market Duration | 183.7 days |
| Highest Average Price City | Bengaluru |
| Highest Average Price | ₹267.77 lakh |
| Most Expensive Property Type | Villa |
| Highest Property Type Average | ₹502.21 lakh |
| Missing Values | 0 |
| Duplicate Rows | 0 |