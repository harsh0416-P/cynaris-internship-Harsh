
from pathlib import Path
import pandas as pd

DATA_PATH = Path(
    "../week-5-day-3-duckdb/data/sales.csv"
).resolve()

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_csv(DATA_PATH)

required = {"city", "category", "product", "quantity", "amount"}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Calculate business metrics from the dataset
total_revenue = df["amount"].sum()
average_sale = df["amount"].mean()
median_sale = df["amount"].median()
high_value_count = int((df["amount"] >= 30000).sum())

city_revenue = df.groupby("city")["amount"].sum().sort_values(
    ascending=False
)
category_revenue = df.groupby("category")["amount"].sum().sort_values(
    ascending=False
)
product_quantity = df.groupby("product")["quantity"].sum().sort_values(
    ascending=False
)

# Generate transparent, data-driven business insights
insights = [
    "# AI-Ready Business Insights Report",
    "",
    "> Generated using Python and Pandas rules; this is not an LLM response.",
    "",
    "## Business Overview",
    f"- Total revenue: {total_revenue:,.2f}",
    f"- Average transaction amount: {average_sale:,.2f}",
    f"- Median transaction amount: {median_sale:,.2f}",
    f"- High-value transactions (amount >= 30000): {high_value_count:,}",
    "",
    "## Key Findings",
    f"- Highest-revenue city: **{city_revenue.index[0]}** "
    f"({city_revenue.iloc[0]:,.2f})",
    f"- Highest-revenue category: **{category_revenue.index[0]}** "
    f"({category_revenue.iloc[0]:,.2f})",
    f"- Highest-quantity product: **{product_quantity.index[0]}** "
    f"({product_quantity.iloc[0]:,.0f} units)",
    "",
    "## Revenue by City",
]

for city, revenue in city_revenue.items():
    insights.append(f"- {city}: {revenue:,.2f}")

insights.extend(["", "## Revenue by Category"])

for category, revenue in category_revenue.items():
    insights.append(f"- {category}: {revenue:,.2f}")

insights.extend([
    "",
    "## Suggested Questions for Further Analysis",
    "- Which city has the largest opportunity for revenue growth?",
    "- Which categories have high revenue but low sales quantities?",
    "- How do average transaction amounts differ between cities?",
    "- Are there missing values, duplicates, or unusual sale amounts?",
    "",
    "## Limitations",
    "These are descriptive findings, not causal explanations or forecasts. "
    "The report does not use a generative AI model.",
])

report_path = OUTPUT_DIR / "ai_analysis_results.md"
report_path.write_text("\n".join(insights), encoding="utf-8")

print("Business insights generated successfully.")
print(f"Rows analyzed: {len(df):,}")
print(f"Total revenue: {total_revenue:,.2f}")
print(f"Highest-revenue city: {city_revenue.index[0]}")
print(f"Highest-revenue category: {category_revenue.index[0]}")
print(f"Highest-quantity product: {product_quantity.index[0]}")
print(f"Report saved to: {report_path.resolve()}")
