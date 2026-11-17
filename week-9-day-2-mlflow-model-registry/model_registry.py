
# ============================================================
# W9D2 - MLflow Model Registry for Analyst Models
# Project: Business Sales Prediction
# ============================================================

import os
import warnings
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

warnings.filterwarnings("ignore")

# 1. Configuration
DATA_PATH = (
    r"D:\Cynaris-Internship\week-5-day-3-duckdb\data\sales.csv"
)

EXPERIMENT_NAME = "W9D2_Model_Registry"
MODEL_NAME = "CynarisSalesAmountModel"

os.makedirs("reports", exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

# 2. Load dataset
print("Loading sales dataset...")

df = pd.read_csv(DATA_PATH)

features = ["city", "category", "product", "quantity"]
target = "amount"

df = df[features + [target]].dropna()

X = df[features].copy()
y = df[target].astype(float)

print("Dataset shape:", df.shape)

# 3. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# 4. Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            ["city", "category", "product"]
        ),
        (
            "numerical",
            "passthrough",
            ["quantity"]
        )
    ]
)

# 5. Build Random Forest model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "regressor",
            RandomForestRegressor(
                n_estimators=100,
                random_state=42
            )
        )
    ]
)

# 6. Configure MLflow
mlflow.set_experiment(EXPERIMENT_NAME)

print("Training model...")

with mlflow.start_run(
    run_name="sales_amount_prediction"
) as run:

    # 7. Train
    model.fit(X_train, y_train)

    # 8. Predict
    predictions = model.predict(X_test)

    # 9. Evaluate
    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(
        mean_squared_error(y_test, predictions)
    )

    r2 = r2_score(y_test, predictions)

    # 10. Log parameters
    mlflow.log_param(
        "model_type",
        "RandomForestRegressor"
    )

    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("random_state", 42)

    # 11. Log metrics
    mlflow.log_metric("MAE", float(mae))
    mlflow.log_metric("RMSE", float(rmse))
    mlflow.log_metric("R2", float(r2))

    # 12. Save evaluation report
    report_path = "reports/model_evaluation.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("SALES AMOUNT PREDICTION MODEL\n")
        file.write("=" * 40 + "\n")
        file.write(f"Dataset rows: {len(df)}\n")
        file.write(f"Training rows: {len(X_train)}\n")
        file.write(f"Testing rows: {len(X_test)}\n")
        file.write(f"MAE: {mae:.4f}\n")
        file.write(f"RMSE: {rmse:.4f}\n")
        file.write(f"R2: {r2:.4f}\n")

    mlflow.log_artifact(report_path)

    # 13. Register model in MLflow
    print("Registering model...")

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        name="sales_amount_model",
        registered_model_name=MODEL_NAME,
        input_example=X_train.head(3),
        skops_trusted_types=[
            "sklearn.tree._tree.Tree"
        ]
    )

    # 14. Save run information
    with open(
        "reports/registration_details.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(f"Experiment: {EXPERIMENT_NAME}\n")
        file.write(f"Run ID: {run.info.run_id}\n")
        file.write(f"Model Name: {MODEL_NAME}\n")
        file.write(f"Model URI: {model_info.model_uri}\n")

    mlflow.log_artifact(
        "reports/registration_details.txt"
    )

# 15. Final output
print("\n" + "=" * 45)
print("MODEL TRAINING AND REGISTRATION COMPLETED")
print("=" * 45)

print("Model:", MODEL_NAME)
print("MAE:", round(mae, 4))
print("RMSE:", round(rmse, 4))
print("R2:", round(r2, 4))
print("Model URI:", model_info.model_uri)
print("Experiment:", EXPERIMENT_NAME)

print("\nCheck the MLflow Model Registry for the registered version.")
