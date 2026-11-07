
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from sklearn.model_selection import KFold, cross_val_predict
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "da_realestate_listings.csv"

OUTPUT_DIR = BASE_DIR / "output"
CHART_DIR = BASE_DIR / "charts"

OUTPUT_DIR.mkdir(exist_ok=True)
CHART_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")


# ==========================================
# 2. LOAD AND CLEAN DATA
# ==========================================

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print("Original dataset shape:", df.shape)

df = df.drop_duplicates().copy()

numeric_columns = [
    "area_sqft", "price_per_sqft",
    "total_price_lakh", "age_years",
    "floor", "parking", "days_on_market"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["listed_date"] = pd.to_datetime(
    df["listed_date"], errors="coerce"
)

df = df.dropna(subset=[
    "city", "locality", "transaction_type",
    "area_sqft", "price_per_sqft"
])

df = df[
    (df["area_sqft"] > 0) &
    (df["price_per_sqft"] > 0)
].copy()

# Bengaluru sale listings
blr = df[
    (df["city"].astype(str).str.strip().str.lower() == "bengaluru") &
    (df["transaction_type"].astype(str).str.strip().str.lower() == "sale")
].copy()

if len(blr) < 10:
    raise ValueError("Insufficient Bengaluru sale records.")

print("Bengaluru sale records:", len(blr))


# ==========================================
# 3. MICRO-MARKET SEGMENTATION
# ==========================================

market_summary = blr.groupby("locality").agg(
    listing_count=("listing_id", "count"),
    average_price_sqft=("price_per_sqft", "mean"),
    median_price_sqft=("price_per_sqft", "median"),
    average_area=("area_sqft", "mean"),
    average_property_age=("age_years", "mean"),
    average_days_on_market=("days_on_market", "mean")
).reset_index()

market_summary = market_summary.sort_values(
    "average_price_sqft", ascending=False
)

market_summary.to_csv(
    OUTPUT_DIR / "micromarket_analysis.csv",
    index=False
)

top_markets = (
    blr["locality"].value_counts().head(3).index
)

top_market_data = blr[
    blr["locality"].isin(top_markets)
].copy()


# ==========================================
# 4. EXPLORATORY DATA ANALYSIS
# ==========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=market_summary.head(10),
    x="average_price_sqft",
    y="locality"
)

plt.title("Average Property Price per Sq Ft by Locality")
plt.xlabel("Average Price per Sq Ft")
plt.ylabel("Locality")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "locality_price_comparison.png",
    dpi=300
)
plt.close()


plt.figure(figsize=(9, 6))

sns.histplot(
    data=blr,
    x="price_per_sqft",
    bins=15,
    kde=True
)

plt.title("Distribution of Bengaluru Property Prices")
plt.xlabel("Price per Sq Ft")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "price_distribution.png",
    dpi=300
)
plt.close()


plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=blr,
    x="area_sqft",
    y="price_per_sqft",
    hue="type"
)

plt.title("Property Area vs Price per Sq Ft")
plt.xlabel("Property Area (Sq Ft)")
plt.ylabel("Price per Sq Ft")
plt.tight_layout()

plt.savefig(
    CHART_DIR / "area_vs_price.png",
    dpi=300
)
plt.close()


# ==========================================
# 5. PREDICTIVE MODELLING
# ==========================================

features = [
    "area_sqft",
    "age_years",
    "floor",
    "parking",
    "locality"
]

X = blr[features].copy()
y = blr["price_per_sqft"].copy()

numeric_features = [
    "area_sqft", "age_years", "floor", "parking"
]

categorical_features = ["locality"]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            SimpleImputer(strategy="median"),
            numeric_features
        ),
        (
            "categorical",
            Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ]),
            categorical_features
        )
    ]
)

models = {
    "Median Dummy Baseline": DummyRegressor(strategy="median"),
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        max_depth=4,
        min_samples_leaf=2,
        random_state=42
    )
}

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

results = []
prediction_output = pd.DataFrame({
    "actual_price_sqft": y
})

for name, model in models.items():

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    predictions = cross_val_predict(
        pipeline,
        X,
        y,
        cv=cv
    )

    mae = mean_absolute_error(y, predictions)
    rmse = np.sqrt(mean_squared_error(y, predictions))
    mape = mean_absolute_percentage_error(
        y, predictions
    ) * 100

    results.append({
        "model": name,
        "samples": len(y),
        "MAE": mae,
        "RMSE": rmse,
        "MAPE_percent": mape
    })

    prediction_output[
        name.replace(" ", "_").lower() + "_prediction"
    ] = predictions

    print(
        f"{name}: MAE={mae:.2f}, "
        f"RMSE={rmse:.2f}, MAPE={mape:.2f}%"
    )


# ==========================================
# 6. SAVE MODEL COMPARISON
# ==========================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    "MAPE_percent"
)

results_df.to_csv(
    OUTPUT_DIR / "model_comparison.csv",
    index=False
)

prediction_output.to_csv(
    OUTPUT_DIR / "prediction_results.csv",
    index=False
)


# ==========================================
# 7. MODEL COMPARISON CHART
# ==========================================

plt.figure(figsize=(10, 6))

sns.barplot(
    data=results_df,
    x="MAPE_percent",
    y="model"
)

plt.axvline(
    x=18,
    linestyle="--",
    label="Project target: 18%"
)

plt.title("Regression Model MAPE Comparison")
plt.xlabel("MAPE (%)")
plt.ylabel("Model")
plt.legend()
plt.tight_layout()

plt.savefig(
    CHART_DIR / "model_comparison.png",
    dpi=300
)
plt.close()


# ==========================================
# 8. SAVE METHODOLOGY
# ==========================================

methodology = """
# Week 6 - Deep-Dive Analysis Methodology

## Objective
Analyze Bengaluru property sale listings, compare micro-markets,
and evaluate regression models for predicting price per square foot.

## Dataset
Source: Cynaris PropTech real estate listings dataset.
The analysis uses valid Bengaluru sale listings.

## Segmentation
Properties are grouped by locality.
Average and median price per square foot, listing count,
average area, property age, and days on market are calculated.

## Prediction Target
price_per_sqft

## Features
- area_sqft
- age_years
- floor
- parking
- locality

## Models
- Median Dummy Regressor
- Linear Regression
- Ridge Regression
- Random Forest Regressor

## Validation
Five-fold cross-validation with shuffled folds and random_state=42.

## Evaluation Metrics
- MAE
- RMSE
- MAPE

## Assumptions and Limitations
- Only Bengaluru sale listings are included.
- Price per square foot is used as the prediction target.
- Missing numeric feature values are imputed using the median.
- Missing locality values are imputed using the most frequent category.
- The dataset contains a limited number of Bengaluru sale listings.
- Cross-validation results are preliminary and may vary with new data.
- The 18% MAPE target is an acceptance criterion, not an assumed result.
- Locality codes are used as supplied; no geographic coordinates are inferred.
"""

with open(
    OUTPUT_DIR / "methodology.md",
    "w",
    encoding="utf-8"
) as file:
    file.write(methodology)


# ==========================================
# 9. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 50)
print("WEEK 6 DEEP-DIVE ANALYSIS COMPLETED")
print("=" * 50)

print("Bengaluru sale records:", len(blr))
print("Unique localities:", blr["locality"].nunique())
print("Top 3 micro-markets:", list(top_markets))

print("\nModel comparison:")
print(results_df.to_string(index=False))

print("\nBest model by MAPE:")
print(results_df.iloc[0]["model"])

print("\nGenerated output files:")
for file in sorted(OUTPUT_DIR.iterdir()):
    print("-", file.name)

print("\nGenerated charts:")
for file in sorted(CHART_DIR.iterdir()):
    print("-", file.name)
