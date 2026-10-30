
from pathlib import Path
import json
import time

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import duckdb

# --------------------------------------------------
# Configuration
# --------------------------------------------------
DATA_PATH = Path(
    "../week-5-day-3-duckdb/data/sales.csv"
).resolve()

OUTPUT_DIR = Path("outputs")
CHART_DIR = OUTPUT_DIR / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

print("=" * 65)
print("W5D5: AI-POWERED EDA ON AN INDIAN BUSINESS DATASET")
print("=" * 65)

# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------
start = time.perf_counter()
df = pd.read_csv(DATA_PATH)
load_time = time.perf_counter() - start

print(f"\nDataset: {DATA_PATH}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(f"Load time: {load_time:.4f} seconds")

# --------------------------------------------------
# 2. Data quality checks
# --------------------------------------------------
missing_values = df.isnull().sum()
duplicate_rows = int(df.duplicated().sum())

quality_report = {
    "row_count": int(len(df)),
    "column_count": int(len(df.columns)),
    "duplicate_rows": duplicate_rows,
    "missing_values": {
        column: int(count)
        for column, count in missing_values.items()
    },
    "data_types": {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    },
}

with open(OUTPUT_DIR / "data_quality_report.json", "w", encoding="utf-8") as f:
    json.dump(quality_report, f, indent=2)

print("\nDATA QUALITY")
print("Duplicate rows:", duplicate_rows)
print("Missing values by column:")
print(missing_values.to_string())

# --------------------------------------------------
# 3. Summary statistics
# --------------------------------------------------
df.describe(include="all").transpose().to_csv(
    OUTPUT_DIR / "summary_statistics.csv"
)

# Validate required business columns
required_columns = {
    "amount", "city", "category", "product", "quantity"
}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise ValueError(f"Required columns are missing: {missing_columns}")

# --------------------------------------------------
# 4. Business analysis with Pandas
# --------------------------------------------------
total_revenue = float(df["amount"].sum())
average_sale = float(df["amount"].mean())
high_value_count = int((df["amount"] >= 30000).sum())

city_revenue = (
    df.groupby("city", as_index=False)["amount"]
    .sum()
    .rename(columns={"amount": "revenue"})
    .sort_values("revenue", ascending=False)
)

category_revenue = (
    df.groupby("category", as_index=False)["amount"]
    .sum()
    .rename(columns={"amount": "revenue"})
    .sort_values("revenue", ascending=False)
)

product_quantity = (
    df.groupby("product", as_index=False)["quantity"]
    .sum()
    .sort_values("quantity", ascending=False)
)

city_revenue.to_csv(OUTPUT_DIR / "revenue_by_city.csv", index=False)
category_revenue.to_csv(
    OUTPUT_DIR / "revenue_by_category.csv", index=False
)
product_quantity.to_csv(
    OUTPUT_DIR / "quantity_by_product.csv", index=False
)

# --------------------------------------------------
# 5. Visualizations
# --------------------------------------------------
def save_bar_chart(data, x, y, title, filename, x_label, y_label):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data[x].astype(str), data[y])
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=150)
    plt.close(fig)

save_bar_chart(
    city_revenue, "city", "revenue",
    "Revenue by City",
    "revenue_by_city.png", "City", "Revenue"
)

save_bar_chart(
    category_revenue, "category", "revenue",
    "Revenue by Category",
    "revenue_by_category.png", "Category", "Revenue"
)

save_bar_chart(
    product_quantity, "product", "quantity",
    "Quantity Sold by Product",
    "quantity_by_product.png", "Product", "Quantity"
)

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df["amount"].dropna(), bins=30)
ax.set_title("Distribution of Sale Amounts")
ax.set_xlabel("Sale Amount")
ax.set_ylabel("Number of Transactions")
fig.tight_layout()
fig.savefig(CHART_DIR / "sales_amount_distribution.png", dpi=150)
plt.close(fig)

# --------------------------------------------------
# 6. Cross-check business metrics using DuckDB SQL
# --------------------------------------------------
con = duckdb.connect()
escaped_path = DATA_PATH.as_posix().replace("'", "''")

con.execute(
    f"CREATE VIEW sales AS SELECT * FROM read_csv_auto('{escaped_path}')"
)

duck_metrics = con.execute("""
    SELECT
        SUM(amount) AS total_revenue,
        AVG(amount) AS average_sale,
        COUNT(*) FILTER (WHERE amount >= 30000) AS high_value_count
    FROM sales
""").fetchone()

assert abs(float(duck_metrics[0]) - total_revenue) < 0.01
assert abs(float(duck_metrics[1]) - average_sale) < 0.01
assert int(duck_metrics[2]) == high_value_count

con.close()

# --------------------------------------------------
# 7. Create a business findings report
# --------------------------------------------------
top_city = city_revenue.iloc[0]
top_category = category_revenue.iloc[0]
top_product = product_quantity.iloc[0]

findings = f"""# Indian Business Dataset — EDA Findings

## Dataset
- Rows: {len(df):,}
- Columns: {len(df.columns)}
- CSV loading time: {load_time:.4f} seconds

## Business Metrics
- Total revenue: {total_revenue:,.2f}
- Average sale amount: {average_sale:,.2f}
- High-value transactions (amount >= 30000): {high_value_count:,}
- Duplicate rows: {duplicate_rows:,}

## Key Findings
- Highest-revenue city: {top_city['city']} ({top_city['revenue']:,.2f})
- Highest-revenue category: {top_category['category']} ({top_category['revenue']:,.2f})
- Highest-quantity product: {top_product['product']} ({top_product['quantity']:,.0f} units)

## Data Quality
Missing values are recorded in `data_quality_report.json`.
Summary statistics are saved in `summary_statistics.csv`.

## Validation
Pandas revenue, average sale, and high-value transaction count
were cross-checked against DuckDB SQL results successfully.

## Limitations
This is descriptive analysis of the supplied dataset. It does not
establish causal relationships or guarantee future business performance.
"""

(OUTPUT_DIR / "eda_findings.md").write_text(findings, encoding="utf-8")

print("\nBUSINESS SUMMARY")
print(f"Total revenue: {total_revenue:,.2f}")
print(f"Average sale: {average_sale:,.2f}")
print(f"High-value transactions: {high_value_count:,}")
print(f"Top city: {top_city['city']}")
print(f"Top category: {top_category['category']}")
print(f"Top product by quantity: {top_product['product']}")

print("\nVALIDATION")
print("Pandas vs DuckDB metrics: PASS")

print("\nOUTPUT FILES")
for path in sorted(OUTPUT_DIR.rglob("*")):
    if path.is_file():
        print(path)

print("\nEDA completed successfully.")
print("Note: This script produces automated EDA, charts, and findings.")
print("An LLM-powered PandasAI analysis can be added after configuring its model.")


