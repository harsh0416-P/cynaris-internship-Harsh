
import pandas as pd
import numpy as np
import mlflow
from scipy.stats import chi2_contingency

# 1. Load the business dataset
DATA_PATH = "../week-5-day-3-duckdb/data/sales.csv"
df = pd.read_csv(DATA_PATH)

# 2. Create a reproducible A/B experiment
np.random.seed(42)

df["experiment_group"] = np.random.choice(
    ["A", "B"], size=len(df)
)

# 3. Simulate purchase conversion outcomes
# This is a demonstration, not actual customer behaviour.
df["converted"] = np.where(
    df["experiment_group"] == "A",
    np.random.binomial(1, 0.10, len(df)),
    np.random.binomial(1, 0.13, len(df))
)

# 4. Calculate metrics
summary = df.groupby("experiment_group").agg(
    visitors=("converted", "count"),
    conversions=("converted", "sum"),
    revenue=("amount", "sum")
)

summary["conversion_rate"] = (
    summary["conversions"] / summary["visitors"]
)

print("\nA/B Test Results:")
print(summary)

# 5. Statistical significance test
contingency = [
    summary.loc["A", ["conversions"]].iloc[0],
    summary.loc["B", ["conversions"]].iloc[0]
]

non_conversions = [
    summary.loc["A", "visitors"] - summary.loc["A", "conversions"],
    summary.loc["B", "visitors"] - summary.loc["B", "conversions"]
]

table = [
    [contingency[0], non_conversions[0]],
    [contingency[1], non_conversions[1]]
]

chi2, p_value, _, _ = chi2_contingency(table)

# 6. Track experiment using MLflow
mlflow.set_experiment("W9D3_AB_Test_Tracking")

with mlflow.start_run(run_name="checkout_ab_test"):
    mlflow.log_param("control_group", "A")
    mlflow.log_param("variant_group", "B")
    mlflow.log_param("test_type", "chi_square")

    mlflow.log_metric(
        "conversion_rate_A",
        summary.loc["A", "conversion_rate"]
    )

    mlflow.log_metric(
        "conversion_rate_B",
        summary.loc["B", "conversion_rate"]
    )

    mlflow.log_metric("p_value", p_value)
    mlflow.log_metric("chi_square", chi2)

    mlflow.log_text(
        summary.to_string(),
        "ab_test_results.txt"
    )

print("\nP-value:", p_value)
print("MLflow experiment tracking completed!")
