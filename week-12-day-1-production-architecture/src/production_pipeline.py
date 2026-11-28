
from pathlib import Path
import json
import logging
import sys

import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ==================================================
# 1. CONFIGURATION
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_DIR / "config" / "settings.json"


def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Configuration not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        config = json.load(file)

    required_settings = [
        "dataset",
        "output_directory",
        "chart_directory"
    ]

    for setting in required_settings:
        if setting not in config:
            raise ValueError(f"Missing configuration setting: {setting}")

    return config


CONFIG = load_config()

DATA_PATH = PROJECT_DIR / CONFIG["dataset"]
OUTPUT_DIR = PROJECT_DIR / CONFIG["output_directory"]
CHART_DIR = PROJECT_DIR / CONFIG["chart_directory"]
LOG_DIR = PROJECT_DIR / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

LOG_LEVEL = CONFIG.get("log_level", "INFO").upper()

REQUIRED_COLUMNS = [
    "listing_id", "city", "locality", "type", "area_sqft",
    "price_per_sqft", "total_price_lakh", "age_years",
    "floor", "parking", "furnished", "listed_date",
    "days_on_market", "transaction_type", "sold"
]


# ==================================================
# 2. LOGGING
# ==================================================

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

    return logging.getLogger("production_pipeline")


logger = setup_logging()


# ==================================================
# 3. DATA INGESTION
# ==================================================

def load_data():
    logger.info("Starting data ingestion")

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    if DATA_PATH.stat().st_size == 0:
        raise ValueError("Dataset file is empty")

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("Dataset contains no records")

    logger.info(
        "Dataset loaded successfully: %s rows, %s columns",
        df.shape[0],
        df.shape[1]
    )

    return df


# ==================================================
# 4. DATA VALIDATION
# ==================================================

def validate_data(df):
    logger.info("Starting data validation")

    validation = CONFIG.get("validation", {})

    if validation.get("check_missing_columns", True):
        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Required columns missing: {missing_columns}"
            )

    if validation.get("check_duplicate_ids", True):
        if df["listing_id"].isna().any():
            raise ValueError("Listing IDs contain missing values")

        if df["listing_id"].duplicated().any():
            raise ValueError("Duplicate listing IDs detected")

    critical_columns = [
        "listing_id", "city", "type", "area_sqft",
        "price_per_sqft", "total_price_lakh",
        "listed_date", "days_on_market"
    ]

    for column in critical_columns:
        if df[column].isna().any():
            raise ValueError(
                f"Missing values detected in critical column: {column}"
            )

    numeric_columns = [
        "area_sqft", "price_per_sqft", "total_price_lakh",
        "age_years", "floor", "parking", "days_on_market", "sold"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

        if df[column].isna().any():
            raise ValueError(
                f"Invalid numeric values detected in {column}"
            )

    df["listed_date"] = pd.to_datetime(
        df["listed_date"],
        errors="coerce"
    )

    if validation.get("check_invalid_dates", True):
        if df["listed_date"].isna().any():
            raise ValueError("Invalid listing dates detected")

    if validation.get("check_positive_prices", True):
        for column in [
            "area_sqft",
            "price_per_sqft",
            "total_price_lakh"
        ]:
            if (df[column] <= 0).any():
                raise ValueError(
                    f"Non-positive values detected in {column}"
                )

    if (df["days_on_market"] < 0).any():
        raise ValueError("Negative days_on_market values detected")

    logger.info("Data validation completed successfully")

    return df


# ==================================================
# 5. BUSINESS ANALYSIS
# ==================================================

def generate_summaries(df):
    logger.info("Generating business summaries")

    city_summary = (
        df.groupby("city")
        .agg(listings=("listing_id", "count"))
        .sort_values("listings", ascending=False)
    )

    city_summary["listing_share_pct"] = (
        city_summary["listings"] / len(df) * 100
    ).round(2)

    property_type_summary = (
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

    market_duration_summary = (
        df.groupby("type")
        .agg(
            listing_count=("listing_id", "count"),
            median_days_on_market=("days_on_market", "median"),
            average_days_on_market=("days_on_market", "mean")
        )
        .sort_values("median_days_on_market", ascending=False)
        .round(2)
    )

    sold_flag_summary = (
        df.groupby("sold")
        .agg(listing_count=("listing_id", "count"))
    )

    sold_flag_summary["share_pct"] = (
        sold_flag_summary["listing_count"] / len(df) * 100
    ).round(2)

    sold_flag_by_city = (
        df.groupby("city")
        .agg(
            listing_count=("listing_id", "count"),
            sold_flag_1_count=("sold", "sum"),
            sold_flag_1_share_pct=("sold", "mean")
        )
    )

    sold_flag_by_city["sold_flag_1_share_pct"] = (
        sold_flag_by_city["sold_flag_1_share_pct"] * 100
    ).round(2)

    monthly_listing_summary = (
        df.set_index("listed_date")
        .resample("ME")
        .size()
        .rename("listing_count")
        .reset_index()
    )

    return {
        "city_summary": city_summary,
        "property_type_summary": property_type_summary,
        "transaction_summary": transaction_summary,
        "market_duration_summary": market_duration_summary,
        "sold_flag_summary": sold_flag_summary,
        "sold_flag_by_city": sold_flag_by_city,
        "monthly_listing_summary": monthly_listing_summary
    }


# ==================================================
# 6. CHART GENERATION
# ==================================================

def generate_charts(summaries):
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Generating charts")

    chart_specs = [
        (
            summaries["city_summary"]["listings"],
            "bar",
            "Property Listings by City",
            "City",
            "Listings",
            "01_listings_by_city.png"
        ),
        (
            summaries["property_type_summary"][
                "median_price_lakh"
            ].sort_values(),
            "barh",
            "Median Property Price by Type",
            "Property Type",
            "Median Price (Lakh)",
            "02_median_price_by_type.png"
        ),
        (
            summaries["transaction_summary"]["listing_count"],
            "bar",
            "Sale versus Rent Listings",
            "Transaction Type",
            "Listings",
            "03_transaction_distribution.png"
        ),
        (
            summaries["market_duration_summary"][
                "median_days_on_market"
            ].sort_values(),
            "barh",
            "Median Days on Market by Type",
            "Property Type",
            "Median Days",
            "04_market_duration_by_type.png"
        ),
        (
            summaries["sold_flag_summary"]["listing_count"],
            "bar",
            "Listing Distribution by Sold Flag",
            "Sold Flag",
            "Listings",
            "05_sold_flag_distribution.png"
        )
    ]

    for series, kind, title, xlabel, ylabel, filename in chart_specs:
        ax = series.plot(
            kind=kind,
            figsize=(10, 6),
            title=title
        )

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        plt.tight_layout()
        plt.savefig(CHART_DIR / filename, dpi=150)
        plt.close()

    monthly = summaries["monthly_listing_summary"]

    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(
        monthly["listed_date"],
        monthly["listing_count"],
        marker="o"
    )

    ax.set_title("Monthly Property Listing Trend")
    ax.set_xlabel("Listed Month")
    ax.set_ylabel("Number of Listings")

    fig.autofmt_xdate()
    fig.tight_layout()

    fig.savefig(
        CHART_DIR / "06_monthly_listing_trend.png",
        dpi=150
    )

    plt.close(fig)

    logger.info("Chart generation completed")


# ==================================================
# 7. EXPORT RESULTS
# ==================================================

def export_outputs(df, summaries):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Exporting summary tables")

    for name, table in summaries.items():
        table.to_csv(OUTPUT_DIR / f"{name}.csv")

    summary = {
        "dataset_rows": int(len(df)),
        "dataset_columns": int(len(df.columns)),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_listing_ids": int(
            df["listing_id"].duplicated().sum()
        ),
        "date_range": {
            "start": str(df["listed_date"].min().date()),
            "end": str(df["listed_date"].max().date())
        },
        "sold_flag_counts": {
            str(key): int(value)
            for key, value in df["sold"].value_counts().items()
        },
        "top_city_by_listing_count": str(
            summaries["city_summary"].index[0]
        ),
        "highest_median_price_property_type": str(
            summaries["property_type_summary"].index[0]
        ),
        "longest_median_market_duration_type": str(
            summaries["market_duration_summary"].index[0]
        )
    }

    summary_path = OUTPUT_DIR / "analysis_summary.json"

    with open(summary_path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)

    logger.info("Summary exports completed")


# ==================================================
# 8. PIPELINE ORCHESTRATION
# ==================================================

def run_pipeline():
    logger.info("Production EDA pipeline started")

    try:
        df = load_data()
        df = validate_data(df)

        summaries = generate_summaries(df)

        export_outputs(df, summaries)
        generate_charts(summaries)

        logger.info(
            "Pipeline completed successfully. Outputs: %s",
            OUTPUT_DIR
        )

        return 0

    except Exception:
        logger.exception("Production EDA pipeline failed")
        return 1


# ==================================================
# 9. EXECUTION
# ==================================================

if __name__ == "__main__":
    sys.exit(run_pipeline())
