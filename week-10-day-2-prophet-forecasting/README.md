# W10D2 — Prophet Forecasting on Indian Real Estate Data

## Objective
Apply Facebook Prophet to historical Indian real estate listing data and generate a monthly property-price forecast.

## Dataset
- Source file: `data/da_realestate_listings.csv`
- Records: 600
- Historical period: January 2023 – December 2024
- Target variable: Monthly average `total_price_lakh`

## Methodology
1. Loaded and inspected the real estate dataset.
2. Converted `listed_date` into datetime format.
3. Aggregated property prices into monthly averages.
4. Prepared Prophet's required `ds` and `y` columns.
5. Split the data chronologically:
   - Training: 21 months
   - Testing: 3 months
6. Trained a Prophet forecasting model.
7. Generated a six-month forecast.
8. Evaluated predictions against the three-month test period.

## Evaluation Results

| Metric | Result |
|---|---:|
| MAE | ₹20.28 lakh |
| RMSE | ₹26.32 lakh |

## Outputs
- `outputs/prophet_forecast.csv`
- `outputs/forecast_evaluation.csv`
- `outputs/prophet_forecast.png`
- `outputs/forecast_components.png`

## Limitations
- Only 24 monthly observations are available.
- Evaluation uses only three test observations.
- The dataset combines listings from different cities and property types.
- Results are exploratory and should not be treated as reliable investment predictions.

## Tools
Python, Pandas, NumPy, Matplotlib, Scikit-learn, Prophet, Jupyter Notebook.
