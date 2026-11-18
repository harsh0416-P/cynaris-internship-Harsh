# W9D5 — Tracked Data Analyst Experiment Pipeline

## Project Overview
This project implements an automated Exploratory Data Analysis (EDA) pipeline on the Indian Business Sales Dataset using Python and MLflow.

The pipeline analyzes business data, calculates data quality and business metrics, generates visualizations, and tracks experiment results using MLflow.

## Dataset
- Dataset: Indian Business Sales Dataset
- Records: 100,000
- Columns: 6
- Missing values: 0
- Duplicate rows: 0

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- MLflow
- SQLite
- Git and GitHub

## Pipeline Workflow
1. Load the sales dataset.
2. Inspect dataset structure.
3. Calculate missing values and duplicate records.
4. Calculate business performance metrics.
5. Analyze revenue by city.
6. Generate a revenue visualization.
7. Save an EDA summary report.
8. Log parameters, metrics, and artifacts in MLflow.

## Business Analysis Results

| Metric | Result |
|---|---:|
| Total Revenue | 2,505,000,000 |
| Average Order Value | 25,050 |
| Total Quantity | 550,000 |
| Unique Cities | 4 |
| Unique Categories | 4 |
| Top Revenue City | Ahmedabad |

## MLflow Tracking
Experiment name: `W9D5_Tracked_DA_Experiment_Pipeline`

Run name: `Indian_Business_Tracked_EDA`

Tracked parameters:
- Dataset name
- Analysis type
- Number of records
- Number of columns

Tracked metrics:
- Missing values
- Duplicate rows
- Total revenue
- Average order value
- Total quantity
- Unique cities
- Unique categories

## Project Structure
```text
week-9-day-5-tracked-da-experiment-pipeline/
├── tracked_eda_pipeline.py
├── README.md
├── artifacts/
│   ├── revenue_by_city.png
│   └── eda_summary.txt
└── evidence/
    ├── 01_mlflow_experiment.png
    ├── 02_mlflow_metrics.png
    └── 03_mlflow_artifacts.png
```

## Key Findings
- The dataset contains 100,000 records.
- No missing values or duplicate rows were detected.
- Ahmedabad recorded the highest total revenue.
- MLflow successfully tracked the EDA experiment and its artifacts.

## Limitations
The quality checks cover missing values and duplicate rows only. Further validation is needed to assess business-data accuracy and realism.

## How to Run
```bash
python tracked_eda_pipeline.py
```

## Conclusion
Successfully developed and executed a tracked EDA pipeline that combines business analysis, data visualization, and MLflow experiment tracking.