# Sales Forecasting Dashboard

## Project Overview
The Sales Forecasting Dashboard analyzes historical sales transactions and predicts future sales using time-series forecasting. It provides business insights through interactive visualizations and forecast reports.

## Objectives
- Analyze historical sales performance.
- Identify monthly, yearly, category-wise, and regional sales trends.
- Build a sales forecasting model using Prophet.
- Evaluate forecasting accuracy.
- Visualize future sales predictions through a Streamlit dashboard.

## Technology Stack
- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Plotly
- Streamlit
- Facebook Prophet
- Scikit-learn
- Jupyter Notebook

## Dataset
**File:** `sales.csv`

The dataset contains sales transaction information, including:
- Order Date
- Ship Date
- Customer Details
- Product Category
- Sub-Category
- Region
- Sales

## Project Workflow
1. Import Python libraries.
2. Load and inspect the dataset.
3. Clean missing values and duplicate records.
4. Convert date columns into datetime format.
5. Perform exploratory data analysis.
6. Aggregate transaction sales into monthly sales.
7. Split data into training and testing datasets.
8. Train and evaluate the Prophet forecasting model.
9. Generate a 12-month sales forecast.
10. Build an interactive Streamlit dashboard.

## Model Evaluation
The forecasting model is evaluated using:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- Mean Absolute Percentage Error (MAPE)

The Prophet model is compared against a baseline forecasting model.

## Dashboard Features
- Total Sales KPI
- Total Orders KPI
- Total Customers KPI
- Historical Monthly Sales
- Category-wise Sales Distribution
- Future Sales Forecast
- Forecast Confidence Intervals
- Model Performance Metrics
- Forecast Data Table

## Project Structure
```text
week-10-day-5-sales-forecasting/
│
├── sales.csv
├── Sales_Forecasting.ipynb
├── app.py
├── README.md
├── outputs/
└── evidence/
```

## Installation

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit prophet scikit-learn
```

## Run the Notebook

Open `Sales_Forecasting.ipynb` in Jupyter Notebook and execute the cells sequentially.

## Run the Dashboard

```bash
streamlit run app.py
```

## Outputs
Generated forecasting results and analysis files are stored in the `outputs/` directory.

Screenshots and project evidence are stored in the `evidence/` directory.

## Limitations
- Forecasts are based on historical sales patterns.
- Forecast accuracy depends on the amount and quality of historical data.
- Predictions should be interpreted as estimates, not guaranteed future sales.
- The model should be monitored and retrained when new sales data becomes available.

## Conclusion
This project demonstrates an end-to-end sales analytics and forecasting workflow, combining data preprocessing, exploratory analysis, time-series modeling, model evaluation, and interactive dashboard development.
