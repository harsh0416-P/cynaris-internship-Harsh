
import pandas as pd
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)

df = pd.read_csv("data/sales.csv")
df["Order Date"] = pd.to_datetime(
    df["Order Date"], dayfirst=True, errors="coerce"
)

results = {
    "1. Total Sales": df["Sales"].sum(),

    "2. Top 5 Cities": (
        df.groupby("City")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    ),

    "3. Highest Sales Category": (
        df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    ),

    "4. Average Sales": df["Sales"].mean(),

    "5. Sales by Region": (
        df.groupby("Region")["Sales"].sum()
    ),

    "6. Highest Sales Segment": (
        df.groupby("Segment")["Sales"]
        .sum()
        .idxmax()
    ),

    "7. Top 10 Products": (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    ),

    "8. Unique Order IDs": df["Order ID"].nunique(),

    "9. Highest Sales Month": (
        df.groupby(df["Order Date"].dt.month)["Sales"]
        .sum()
        .idxmax()
    ),

    "10. Sales by Category": (
        df.groupby("Category")["Sales"].sum()
    )
}

with open("outputs/manual_baseline.txt", "w", encoding="utf-8") as f:
    for question, result in results.items():
        print(f"\n{'=' * 55}")
        print(question)
        print(result)
        f.write(f"\n{question}\n{result}\n")

print("\nManual baseline saved to outputs/manual_baseline.txt")
