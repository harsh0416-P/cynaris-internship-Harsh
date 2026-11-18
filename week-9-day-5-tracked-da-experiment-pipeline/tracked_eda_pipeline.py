
import os
import mlflow
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent

DATA_PATH = Path(
    r"D:\Cynaris-Internship\week-5-day-3-duckdb\data\sales.csv"
)

ARTIFACT_DIR = PROJECT_DIR / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

TRACKING_DB = (
    "sqlite:///D:/Cynaris-Internship/"
    "week-9-day-2-mlflow-model-registry/mlflow.db"
)

mlflow.set_tracking_uri(TRACKING_DB)
mlflow.set_experiment("W9D5_Tracked_DA_Experiment_Pipeline")

# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

print("Loading Indian Business Dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("\nFirst five records:")
print(df.head())

# --------------------------------------------------
# 3. DATA QUALITY ANALYSIS
# --------------------------------------------------

missing_values = int(df.isnull().sum().sum())
duplicate_rows = int(df.duplicated().sum())

numeric_columns = df.select_dtypes(include=np.number).columns

print("\nData Quality Summary")
print("Missing values:", missing_values)
print("Duplicate rows:", duplicate_rows)

# --------------------------------------------------
# 4. EDA AND BUSINESS METRICS
# --------------------------------------------------

total_revenue = float(df["amount"].sum())
average_order_value = float(df["amount"].mean())
total_quantity = int(df["quantity"].sum())
unique_cities = int(df["city"].nunique())
unique_categories = int(df["category"].nunique())

top_city = (
    df.groupby("city")["amount"]
    .sum()
    .idxmax()
)

print("\nBusiness Analysis")
print("Total Revenue:", total_revenue)
print("Average Order Value:", average_order_value)
print("Total Quantity:", total_quantity)
print("Unique Cities:", unique_cities)
print("Unique Categories:", unique_categories)
print("Top Revenue City:", top_city)

# --------------------------------------------------
# 5. VISUALIZATION
# --------------------------------------------------

revenue_by_city = (
    df.groupby("city")["amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
revenue_by_city.plot(kind="bar")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.tight_layout()

city_chart = ARTIFACT_DIR / "revenue_by_city.png"
plt.savefig(city_chart)
plt.close()

# --------------------------------------------------
# 6. SAVE EDA REPORT
# --------------------------------------------------

report_path = ARTIFACT_DIR / "eda_summary.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("W9D5 TRACKED EDA REPORT\n")
    file.write("======================\n")
    file.write(f"Total records: {len(df)}\n")
    file.write(f"Total columns: {len(df.columns)}\n")
    file.write(f"Missing values: {missing_values}\n")
    file.write(f"Duplicate rows: {duplicate_rows}\n")
    file.write(f"Total revenue: {total_revenue:.2f}\n")
    file.write(f"Average order value: {average_order_value:.2f}\n")
    file.write(f"Total quantity: {total_quantity}\n")
    file.write(f"Top revenue city: {top_city}\n")

# --------------------------------------------------
# 7. MLFLOW EXPERIMENT TRACKING
# --------------------------------------------------

with mlflow.start_run(run_name="Indian_Business_Tracked_EDA"):

    # Parameters
    mlflow.log_param("dataset", "Indian Business Dataset")
    mlflow.log_param("analysis_type", "Exploratory Data Analysis")
    mlflow.log_param("records", len(df))
    mlflow.log_param("columns", len(df.columns))

    # Metrics
    mlflow.log_metric("missing_values", missing_values)
    mlflow.log_metric("duplicate_rows", duplicate_rows)
    mlflow.log_metric("total_revenue", total_revenue)
    mlflow.log_metric("average_order_value", average_order_value)
    mlflow.log_metric("total_quantity", total_quantity)
    mlflow.log_metric("unique_cities", unique_cities)
    mlflow.log_metric("unique_categories", unique_categories)

    # Artifacts
    mlflow.log_artifact(str(city_chart))
    mlflow.log_artifact(str(report_path))

    print("\nMLflow tracking completed successfully!")

print("\nW9D5 PIPELINE COMPLETED!")
print("Artifacts saved in:", ARTIFACT_DIR)
