# W9D1 - MLflow Experiment Tracking

## Objective
Track exploratory data analysis and business performance experiments using MLflow.

## Dataset
Indian Business Sales Dataset

Columns:
- sale_id
- city
- category
- product
- quantity
- amount

## Experiments

### 1. Data Quality Analysis
Tracked metrics:
- Row count
- Column count
- Missing values
- Duplicate rows

Artifact:
- Summary statistics CSV

### 2. Business Performance Analysis
Tracked metrics:
- Total revenue
- Average order value
- Total quantity

Artifacts:
- Revenue by city CSV
- Revenue by city chart

## Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- MLflow

## Run
python mlflow_eda.py

## Start MLflow Dashboard
python -m mlflow ui --host 127.0.0.1 --port 5000 --workers 1
