
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mlflow
import os

DATA_PATH = r"D:\Cynaris-Internship\week-5-day-3-duckdb\data\sales.csv"

df = pd.read_csv(DATA_PATH)

os.makedirs("reports", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

mlflow.set_experiment("W9D1_Business_EDA")

# Run 1: Data Quality Analysis
with mlflow.start_run(run_name="data_quality_analysis"):

    mlflow.log_param("dataset", "sales.csv")
    mlflow.log_param("analysis_type", "Data Quality")

    mlflow.log_metric("row_count", len(df))
    mlflow.log_metric("column_count", len(df.columns))
    mlflow.log_metric("missing_values", int(df.isnull().sum().sum()))
    mlflow.log_metric("duplicate_rows", int(df.duplicated().sum()))

    df.describe(include="all").to_csv(
        "reports/summary_statistics.csv"
    )

    mlflow.log_artifact("reports/summary_statistics.csv")

# Run 2: Business Performance Analysis
with mlflow.start_run(run_name="business_performance_analysis"):

    total_revenue = float(df["amount"].sum())
    average_order_value = float(df["amount"].mean())
    total_quantity = int(df["quantity"].sum())

    revenue_by_city = df.groupby("city")["amount"].sum()

    mlflow.log_param("analysis_type", "Business Performance")
    mlflow.log_param("revenue_grouping", "city")

    mlflow.log_metric("total_revenue", total_revenue)
    mlflow.log_metric("average_order_value", average_order_value)
    mlflow.log_metric("total_quantity", total_quantity)

    revenue_by_city.to_csv("reports/revenue_by_city.csv")
    mlflow.log_artifact("reports/revenue_by_city.csv")

    revenue_by_city.plot(kind="bar", title="Revenue by City")
    plt.ylabel("Revenue")
    plt.tight_layout()

    plt.savefig("artifacts/revenue_by_city.png")
    plt.close()

    mlflow.log_artifact("artifacts/revenue_by_city.png")

print("Both MLflow experiments completed successfully!")
