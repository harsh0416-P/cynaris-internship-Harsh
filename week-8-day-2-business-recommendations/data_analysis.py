from pathlib import Path
import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR.parent
    / "project 1 Stakeholder brief + data inventory"
    / "data"
    / "da_customer_profiles.csv"
)


def load_dataset():
    """Load and validate the customer dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_columns = [
        "Customer_ID",
        "City",
        "Age_Band",
        "Acquisition_Channel",
        "Total_Orders",
        "Total_Revenue",
        "Churned"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if df["Customer_ID"].duplicated().any():
        raise ValueError("Duplicate customer IDs detected.")

    if df[required_columns].isnull().any().any():
        raise ValueError("Missing values detected.")

    if not df["Churned"].isin([0, 1]).all():
        raise ValueError("Churned must contain only 0 or 1.")

    print("Dataset loaded successfully!")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    return df

def calculate_insights(df):
    """Calculate five evidence-based business insights."""

    # 1. Overall business performance
    total_customers = len(df)
    total_revenue = float(df["Total_Revenue"].sum())
    total_orders = int(df["Total_Orders"].sum())

    average_revenue = float(df["Total_Revenue"].mean())
    average_orders = float(df["Total_Orders"].mean())

    # 2. Revenue and customer performance by city
    city_performance = (
        df.groupby("City")
        .agg(
            customers=("Customer_ID", "count"),
            revenue=("Total_Revenue", "sum"),
            average_revenue=("Total_Revenue", "mean"),
            churned=("Churned", "sum")
        )
        .sort_values("revenue", ascending=False)
    )

    city_performance["churn_rate"] = (
        city_performance["churned"]
        / city_performance["customers"] * 100
    )

    # 3. Performance by acquisition channel
    channel_performance = (
        df.groupby("Acquisition_Channel")
        .agg(
            customers=("Customer_ID", "count"),
            revenue=("Total_Revenue", "sum"),
            average_revenue=("Total_Revenue", "mean"),
            churned=("Churned", "sum")
        )
        .sort_values("revenue", ascending=False)
    )

    channel_performance["churn_rate"] = (
        channel_performance["churned"]
        / channel_performance["customers"] * 100
    )

    # 4. Performance by age group
    age_performance = (
        df.groupby("Age_Band")
        .agg(
            customers=("Customer_ID", "count"),
            revenue=("Total_Revenue", "sum"),
            average_revenue=("Total_Revenue", "mean")
        )
        .sort_values("revenue", ascending=False)
    )

    # 5. Customer churn
    churned_customers = int(df["Churned"].sum())

    churn_rate = (
        churned_customers / total_customers
    ) * 100

    insights = {
        "total_customers": total_customers,
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_revenue": average_revenue,
        "average_orders": average_orders,
        "churned_customers": churned_customers,
        "churn_rate": churn_rate,
        "city_performance": city_performance,
        "channel_performance": channel_performance,
        "age_performance": age_performance
    }

    return insights
if __name__ == "__main__":
    df = load_dataset()

    insights = calculate_insights(df)

    print("\nTOTAL REVENUE:", insights["total_revenue"])
    print("AVERAGE REVENUE:", insights["average_revenue"])
    print("CHURN RATE:", insights["churn_rate"])

    print("\nCITY PERFORMANCE:")
    print(insights["city_performance"])

    print("\nCHANNEL PERFORMANCE:")
    print(insights["channel_performance"])

    print("\nAGE PERFORMANCE:")
    print(insights["age_performance"])