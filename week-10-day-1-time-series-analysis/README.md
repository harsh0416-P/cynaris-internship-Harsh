# Week 10 – Day 1: Time Series Analysis

## Objective
Analyze time-series sales data to understand trends, seasonality, moving averages, and future sales patterns using ARIMA forecasting.

## Dataset
- **Dataset:** Superstore Sales Dataset
- **Records:** 9,800
- **Date Column:** Order Date
- **Target Column:** Sales
- **Source:** Existing internship dataset

**Note:** This dataset contains US Superstore sales data. It is used here for learning time-series analysis.

## Tasks Completed
- Loaded and explored the sales dataset.
- Converted Order Date into datetime format.
- Sorted data chronologically.
- Aggregated sales by day and month.
- Visualized daily and monthly sales trends.
- Calculated a 30-day moving average.
- Performed seasonal decomposition.
- Applied ARIMA (1,1,1) for sales forecasting.
- Evaluated forecasting performance using MAE and RMSE.

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Statsmodels
- Jupyter Notebook

## Project Structure
```text
week-10-day-1-time-series-analysis/
│
├── data/
│   └── sales.csv
│
├── notebooks/
│   └── W10D1_Time_Series_Analysis.ipynb
│
├── outputs/
│
├── src/
│
└── README.md
```

## Key Concepts
1. Time-series data analysis
2. Trend analysis
3. Seasonality
4. Moving averages
5. Seasonal decomposition
6. ARIMA forecasting
7. Forecast evaluation using MAE and RMSE

## Conclusion
This task demonstrates how historical sales data can be analyzed to identify trends and seasonal patterns and how ARIMA can be used to forecast future sales.

The analysis provides practical experience with time-series data preparation, visualization, statistical modeling, and forecasting evaluation.

**Internship:** Cynaris  
**Week:** 10  
**Day:** 1