
from pathlib import Path
import os

import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==================================================
# 1. CONFIGURATION
# ==================================================

ROOT = Path(r"D:\Cynaris-Internship")

DB_PATH = (
    ROOT / "week-9-day-2-mlflow-model-registry" / "mlflow.db"
)

DATA_PATH = (
    ROOT / "week-5-day-3-duckdb" / "data" / "sales.csv"
)

REPORT_DIR = Path("reports")
REPORT_DIR.mkdir(exist_ok=True)

MODEL_NAME = "CynarisSalesAmountModel"
EXPERIMENT_NAME = "W9D4_Model_Version_Comparison"

if not DB_PATH.exists():
    raise FileNotFoundError(f"MLflow database not found: {DB_PATH}")

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

# Connect to the existing W9D2 MLflow database
tracking_uri = f"sqlite:///{DB_PATH.as_posix()}"

mlflow.set_tracking_uri(tracking_uri)
mlflow.set_registry_uri(tracking_uri)

# ==================================================
# 2. LOAD DATASET
# ==================================================

df = pd.read_csv(DATA_PATH)

features = ["city", "category", "product", "quantity"]
target = "amount"

X = df[features].copy()
y = df[target].copy()

# Same train/test split for both models
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Dataset loaded successfully!")
print("Total records:", len(df))
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# ==================================================
# 3. LOAD REGISTERED MODEL VERSION 1
# ==================================================

print("\nLoading Model Version 1...")

model_v1 = mlflow.pyfunc.load_model(
    f"models:/{MODEL_NAME}/1"
)

predictions_v1 = model_v1.predict(X_test)

# ==================================================
# 4. TRAIN MODEL VERSION 2
# ==================================================

print("\nTraining Model Version 2...")

categorical_features = [
    "city",
    "category",
    "product"
]

numeric_features = ["quantity"]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numeric",
            "passthrough",
            numeric_features
        )
    ]
)

pipeline_v2 = Pipeline([
    ("preprocessor", preprocessor),
    (
        "regressor",
        RandomForestRegressor(
            n_estimators=200,
            max_depth=None,
            min_samples_leaf=2,
            random_state=42
        )
    )
])

pipeline_v2.fit(X_train, y_train)

predictions_v2 = pipeline_v2.predict(X_test)

print("Model Version 2 trained successfully!")

# ==================================================
# 5. EVALUATE BOTH MODELS
# ==================================================

def calculate_metrics(actual, predicted):
    return {
        "MAE": mean_absolute_error(actual, predicted),
        "RMSE": np.sqrt(
            mean_squared_error(actual, predicted)
        ),
        "R2": r2_score(actual, predicted)
    }


metrics_v1 = calculate_metrics(
    y_test,
    predictions_v1
)

metrics_v2 = calculate_metrics(
    y_test,
    predictions_v2
)

comparison = pd.DataFrame(
    [metrics_v1, metrics_v2],
    index=["Version 1", "Version 2"]
)

print("\nMODEL VERSION COMPARISON")
print(comparison)

# Save comparison report
comparison_path = REPORT_DIR / "model_comparison.csv"
comparison.to_csv(comparison_path)

# ==================================================
# 6. TRACK EXPERIMENT IN MLFLOW
# ==================================================

mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(
    run_name="compare_model_versions"
):

    mlflow.log_param(
        "dataset",
        "Indian Business Sales"
    )

    mlflow.log_param(
        "model_name",
        MODEL_NAME
    )

    mlflow.log_param(
        "version_1",
        "Existing Random Forest"
    )

    mlflow.log_param(
        "version_2_estimators",
        200
    )

    mlflow.log_param(
        "test_size",
        0.2
    )

    mlflow.log_param(
        "random_state",
        42
    )

    # Log Version 1 metrics
    for metric, value in metrics_v1.items():
        mlflow.log_metric(
            f"version_1_{metric.lower()}",
            float(value)
        )

    # Log Version 2 metrics
    for metric, value in metrics_v2.items():
        mlflow.log_metric(
            f"version_2_{metric.lower()}",
            float(value)
        )

    mlflow.log_artifact(str(comparison_path))

    # Register Version 2
    print("\nRegistering Model Version 2...")

    mlflow.sklearn.log_model(
        sk_model=pipeline_v2,
        name="model",
        registered_model_name=MODEL_NAME,
        skops_trusted_types=[
            "sklearn.tree._tree.Tree"
        ]
    )

# ==================================================
# 7. DISPLAY FINAL RESULTS
# ==================================================

print("\n" + "=" * 50)
print("W9D4 MODEL COMPARISON COMPLETED")
print("=" * 50)

print("Registered model:", MODEL_NAME)
print("Model Version 1: Existing model")
print("Model Version 2: Newly trained model")
print("Comparison report:", comparison_path)

print("\nFinal comparison:")
print(comparison)

print("\nMLflow experiment:", EXPERIMENT_NAME)
print("Experiment tracking completed successfully!")
