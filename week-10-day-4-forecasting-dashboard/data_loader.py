from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "week-10-day-2-prophet-forecasting" / "data" / "da_realestate_listings.csv"
FORECAST_PATH = ROOT / "week-10-day-2-prophet-forecasting" / "outputs" / "prophet_forecast.csv"
EVALUATION_PATH = ROOT / "week-10-day-2-prophet-forecasting" / "outputs" / "forecast_evaluation.csv"


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")
    return pd.read_csv(path)


def load_data():
    listings = load_csv(DATA_PATH)
    forecast = load_csv(FORECAST_PATH)
    evaluation = load_csv(EVALUATION_PATH)

    required_listing = {"listed_date", "total_price_lakh", "city", "type"}
    required_forecast = {"ds", "yhat", "yhat_lower", "yhat_upper"}
    required_evaluation = {
        "ds", "Actual Price (Lakh)", "Predicted Price (Lakh)"
    }

    for name, frame, required in [
        ("Listings", listings, required_listing),
        ("Forecast", forecast, required_forecast),
        ("Evaluation", evaluation, required_evaluation),
    ]:
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f"{name} file is missing columns: {sorted(missing)}")

    listings["listed_date"] = pd.to_datetime(
        listings["listed_date"], errors="coerce"
    )
    forecast["ds"] = pd.to_datetime(forecast["ds"], errors="coerce")
    evaluation["ds"] = pd.to_datetime(evaluation["ds"], errors="coerce")

    for name, frame, date_col in [
        ("Listings", listings, "listed_date"),
        ("Forecast", forecast, "ds"),
        ("Evaluation", evaluation, "ds"),
    ]:
        if frame[date_col].isna().any():
            raise ValueError(f"{name} contains invalid dates in {date_col}")

    listings["total_price_lakh"] = pd.to_numeric(
        listings["total_price_lakh"], errors="coerce"
    )
    if listings["total_price_lakh"].isna().any():
        raise ValueError("Listings contain invalid property prices")

    monthly = (
        listings.assign(month=listings["listed_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month", as_index=False)
        .agg(
            actual_price=("total_price_lakh", "mean"),
            listing_count=("total_price_lakh", "size"),
        )
        .sort_values("month")
    )

    return listings, monthly, forecast, evaluation
