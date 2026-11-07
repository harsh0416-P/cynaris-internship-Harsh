
import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.model_selection import KFold, cross_val_predict
from sklearn.dummy import DummyRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "da_realestate_listings.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 1. LOAD DATA
# ==========================================

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully:", df.shape)


# ==========================================
# 2. DATA QUALITY CHECKS
# ==========================================

quality = pd.DataFrame({
    "column": df.columns,
    "missing_values": df.isnull().sum().values,
    "unique_values": df.nunique().values
})

quality.to_csv(
    OUTPUT_DIR / "data_quality_report.csv",
    index=False
)

duplicate_rows = int(df.duplicated().sum())
duplicate_listing_ids = int(df["listing_id"].duplicated().sum())

quality_summary = pd.DataFrame({
    "metric": [
        "total_rows",
        "total_columns",
        "duplicate_rows",
        "duplicate_listing_ids"
    ],
    "value": [
        len(df),
        len(df.columns),
        duplicate_rows,
        duplicate_listing_ids
    ]
})

quality_summary.to_csv(
    OUTPUT_DIR / "data_quality_summary.csv",
    index=False
)

print("Data quality checks completed.")


# ==========================================
# 3. DATA CLEANING
# ==========================================

df = df.drop_duplicates().copy()

df["listed_date"] = pd.to_datetime(
    df["listed_date"],
    errors="coerce"
)

numeric_columns = [
    "area_sqft",
    "price_per_sqft",
    "total_price_lakh",
    "age_years",
    "floor",
    "parking",
    "days_on_market"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

df = df.dropna(subset=[
    "city",
    "locality",
    "area_sqft",
    "price_per_sqft",
    "total_price_lakh",
    "transaction_type"
])

df = df[
    (df["area_sqft"] > 0) &
    (df["price_per_sqft"] > 0) &
    (df["total_price_lakh"] > 0)
].copy()

print("Cleaned dataset:", df.shape)


# ==========================================
# 4. PRICE CONSISTENCY CHECK
# ==========================================

df["calculated_price_lakh"] = (
    df["area_sqft"] *
    df["price_per_sqft"] / 100000
)

df["price_difference_lakh"] = (
    df["total_price_lakh"] -
    df["calculated_price_lakh"]
).abs()

df["price_consistent"] = (
    df["price_difference_lakh"] <= 0.01
)

price_consistency = pd.DataFrame({
    "metric": [
        "total_records",
        "consistent_records",
        "inconsistent_records"
    ],
    "value": [
        len(df),
        int(df["price_consistent"].sum()),
        int((~df["price_consistent"]).sum())
    ]
})

price_consistency.to_csv(
    OUTPUT_DIR / "price_consistency_report.csv",
    index=False
)


# ==========================================
# 5. FILTER BENGALURU SALE LISTINGS
# ==========================================

blr = df[
    (df["city"].astype(str).str.strip().str.lower() == "bengaluru") &
    (df["transaction_type"].astype(str).str.strip().str.lower() == "sale")
].copy()

if blr.empty:
    raise ValueError(
        "No Bengaluru sale listings found in the dataset."
    )

print("Bengaluru sale listings:", len(blr))


# ==========================================
# 6. SELECT TOP 3 MICRO-MARKETS
# ==========================================

top_markets = (
    blr["locality"]
    .value_counts()
    .head(3)
    .index
)

market_data = blr[
    blr["locality"].isin(top_markets)
].copy()


# ==========================================
# 7. MICRO-MARKET ANALYSIS
# ==========================================

summary = market_data.groupby("locality").agg(
    listing_count=("listing_id", "count"),
    average_price_sqft=("price_per_sqft", "mean"),
    median_price_sqft=("price_per_sqft", "median"),
    average_area=("area_sqft", "mean"),
    average_days_on_market=("days_on_market", "mean")
).reset_index()

summary.to_csv(
    OUTPUT_DIR / "micromarket_summary.csv",
    index=False
)


# ==========================================
# 8. BASELINE REGRESSION - 5 FOLD CV
# ==========================================

features = [
    "area_sqft",
    "age_years",
    "floor",
    "parking"
]

X = blr[features].copy().fillna(0)
y = blr["price_per_sqft"]

metrics = []

if len(blr) >= 10:

    cv = KFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    model = DummyRegressor(
        strategy="median"
    )

    predictions = cross_val_predict(
        model,
        X,
        y,
        cv=cv
    )

    metrics.append({
        "model": "Median Dummy Baseline - 5 Fold CV",
        "samples": len(y),
        "MAE": mean_absolute_error(
            y, predictions
        ),
        "RMSE": np.sqrt(
            mean_squared_error(y, predictions)
        ),
        "MAPE_percent": mean_absolute_percentage_error(
            y, predictions
        ) * 100
    })

else:
    print("Not enough records for 5-fold cross-validation.")

pd.DataFrame(metrics).to_csv(
    OUTPUT_DIR / "baseline_metrics.csv",
    index=False
)


# ==========================================
# 9. EXPORT CLEANED DATA
# ==========================================

blr.to_csv(
    OUTPUT_DIR / "cleaned_bengaluru_listings.csv",
    index=False
)

market_data.to_csv(
    OUTPUT_DIR / "top3_micromarket_listings.csv",
    index=False
)


# ==========================================
# 10. PIPELINE SUMMARY
# ==========================================

print("\n" + "=" * 45)
print("DATA PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 45)

print("Original dataset rows:", len(pd.read_csv(INPUT_FILE)))
print("Cleaned dataset rows:", len(df))
print("Bengaluru sale listings:", len(blr))
print("Selected micro-markets:", list(top_markets))
print("Selected micro-market listings:", len(market_data))

print("\nMicro-market summary:")
print(summary.to_string(index=False))

if metrics:
    print("\nBaseline metrics:")
    print(pd.DataFrame(metrics).to_string(index=False))

print("\nGenerated reports:")
for file in sorted(OUTPUT_DIR.glob("*.csv")):
    print("-", file.name)

print("\nOutput directory:", OUTPUT_DIR)
print("=" * 45)