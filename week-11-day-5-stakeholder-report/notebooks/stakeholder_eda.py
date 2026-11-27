from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Paths and setup
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_DIR / "data" / "indian_business_data.csv"
CHART_DIR = PROJECT_DIR / "outputs" / "charts"
REPORT_DIR = PROJECT_DIR / "reports"
OUTPUT_DIR = PROJECT_DIR / "outputs"

CHART_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

# --------------------------------------------------
# 2. Data validation and preparation
# --------------------------------------------------

required_columns = [
    "listing_id", "city", "locality", "type", "area_sqft",
    "price_per_sqft", "total_price_lakh", "age_years",
    "floor", "parking", "furnished", "listed_date",
    "days_on_market", "transaction_type", "sold"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

df["listed_date"] = pd.to_datetime(df["listed_date"], errors="coerce")

if df["listed_date"].isna().any():
    raise ValueError("Some listed_date values could not be converted to dates.")

if df["listing_id"].duplicated().any():
    raise ValueError("Duplicate listing IDs found.")

print("=" * 60)
print("STAKEHOLDER REPORT — EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDATASET OVERVIEW")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print(f"Missing values: {df.isna().sum().sum()}")
print(f"Duplicate listing IDs: {df['listing_id'].duplicated().sum()}")
print(f"Date range: {df['listed_date'].min().date()} to {df['listed_date'].max().date()}")

print("\nNUMERICAL SUMMARY")
print(df.describe().round(2))

# --------------------------------------------------
# 3. Calculate five business insight datasets
# --------------------------------------------------

# Insight 1: City-wise listing distribution
city_summary = (
    df.groupby("city")
    .agg(listings=("listing_id", "count"))
    .sort_values("listings", ascending=False)
)
city_summary["listing_share_pct"] = (
    city_summary["listings"] / len(df) * 100
).round(2)

# Insight 2: Property type pricing
type_summary = (
    df.groupby("type")
    .agg(
        listing_count=("listing_id", "count"),
        average_price_lakh=("total_price_lakh", "mean"),
        median_price_lakh=("total_price_lakh", "median"),
        median_price_per_sqft=("price_per_sqft", "median")
    )
    .sort_values("median_price_lakh", ascending=False)
    .round(2)
)

# Insight 3: Sale versus Rent
transaction_summary = (
    df.groupby("transaction_type")
    .agg(
        listing_count=("listing_id", "count"),
        median_days_on_market=("days_on_market", "median"),
        average_days_on_market=("days_on_market", "mean"),
        median_price_per_sqft=("price_per_sqft", "median")
    )
    .round(2)
)

# Insight 4: Market duration by property type
duration_summary = (
    df.groupby("type")
    .agg(
        listing_count=("listing_id", "count"),
        median_days_on_market=("days_on_market", "median"),
        average_days_on_market=("days_on_market", "mean")
    )
    .sort_values("median_days_on_market", ascending=False)
    .round(2)
)

# Insight 5: Sold flag distribution
sold_summary = (
    df.groupby("sold")
    .agg(listing_count=("listing_id", "count"))
)

sold_summary["share_pct"] = (
    sold_summary["listing_count"] / len(df) * 100
).round(2)

sold_by_city = (
    df.groupby("city")
    .agg(
        listing_count=("listing_id", "count"),
        sold_flag_1_count=("sold", "sum"),
        sold_flag_1_share_pct=("sold", "mean")
    )
)

sold_by_city["sold_flag_1_share_pct"] = (
    sold_by_city["sold_flag_1_share_pct"] * 100
).round(2)

# --------------------------------------------------
# 4. Monthly listing trend
# --------------------------------------------------

monthly_summary = (
    df.set_index("listed_date")
    .resample("ME")
    .size()
    .rename("listing_count")
    .reset_index()
)

# --------------------------------------------------
# 5. Export analysis tables
# --------------------------------------------------

summaries = {
    "city_summary": city_summary,
    "property_type_summary": type_summary,
    "transaction_summary": transaction_summary,
    "market_duration_summary": duration_summary,
    "sold_flag_summary": sold_summary,
    "sold_flag_by_city": sold_by_city,
    "monthly_listing_summary": monthly_summary
}

for name, table in summaries.items():
    table.to_csv(OUTPUT_DIR / f"{name}.csv")

# --------------------------------------------------
# 6. Generate charts
# --------------------------------------------------

plt.style.use("default")

# Chart 1: Listings by city
ax = city_summary["listings"].plot(
    kind="bar", figsize=(10, 6), title="Property Listings by City"
)
ax.set_xlabel("City")
ax.set_ylabel("Number of Listings")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(CHART_DIR / "01_listings_by_city.png", dpi=150)
plt.close()

# Chart 2: Median price by property type
ax = type_summary["median_price_lakh"].sort_values().plot(
    kind="barh", figsize=(10, 6),
    title="Median Property Price by Property Type"
)
ax.set_xlabel("Median Price (Lakh)")
ax.set_ylabel("Property Type")
plt.tight_layout()
plt.savefig(CHART_DIR / "02_median_price_by_type.png", dpi=150)
plt.close()

# Chart 3: Sale versus Rent distribution
ax = transaction_summary["listing_count"].plot(
    kind="bar", figsize=(8, 5),
    title="Sale versus Rent Listings"
)
ax.set_xlabel("Transaction Type")
ax.set_ylabel("Number of Listings")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR / "03_transaction_distribution.png", dpi=150)
plt.close()

# Chart 4: Median days on market by property type
ax = duration_summary["median_days_on_market"].sort_values().plot(
    kind="barh", figsize=(10, 6),
    title="Median Days on Market by Property Type"
)
ax.set_xlabel("Median Days on Market")
ax.set_ylabel("Property Type")
plt.tight_layout()
plt.savefig(CHART_DIR / "04_market_duration_by_type.png", dpi=150)
plt.close()

# Chart 5: Sold flag distribution
ax = sold_summary["listing_count"].plot(
    kind="bar", figsize=(8, 5),
    title="Listing Distribution by Sold Flag"
)
ax.set_xlabel("Sold Flag (Dataset Value)")
ax.set_ylabel("Number of Listings")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHART_DIR / "05_sold_flag_distribution.png", dpi=150)
plt.close()

# Chart 6: Monthly listing trend
plt.figure(figsize=(11, 5))
plt.plot(
    monthly_summary["listed_date"],
    monthly_summary["listing_count"],
    marker="o"
)
plt.title("Monthly Property Listing Trend")
plt.xlabel("Listed Month")
plt.ylabel("Number of Listings")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(CHART_DIR / "06_monthly_listing_trend.png", dpi=150)
plt.close()

# --------------------------------------------------
# 7. Save machine-readable analysis summary
# --------------------------------------------------

summary = {
    "dataset_rows": int(len(df)),
    "dataset_columns": int(len(df.columns)),
    "missing_values": int(df.isna().sum().sum()),
    "duplicate_listing_ids": int(df["listing_id"].duplicated().sum()),
    "date_range": {
        "start": str(df["listed_date"].min().date()),
        "end": str(df["listed_date"].max().date())
    },
    "sold_flag_counts": {
        str(key): int(value)
        for key, value in df["sold"].value_counts().items()
    },
    "top_city_by_listing_count": str(city_summary.index[0]),
    "highest_median_price_property_type": str(type_summary.index[0]),
    "longest_median_market_duration_type": str(duration_summary.index[0])
}

with open(OUTPUT_DIR / "analysis_summary.json", "w") as file:
    json.dump(summary, file, indent=4)

# --------------------------------------------------
# 8. Print results for stakeholder report writing
# --------------------------------------------------

for name, table in summaries.items():
    print(f"\n{name.upper().replace('_', ' ')}")
    print(table.to_string())

print("\nANALYSIS COMPLETE")
print(f"Charts saved to: {CHART_DIR}")
print(f"Analysis tables saved to: {OUTPUT_DIR}")