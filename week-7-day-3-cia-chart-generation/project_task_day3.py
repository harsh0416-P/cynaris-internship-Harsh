# W7D3: CIA Chart Generation — Plotly
# Project: EDA on Indian Business Dataset

import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px

# Load sales data from the verified SQLite database
DB_PATH = Path("../week-6-day-5-nl-sql-dashboard/data/sales.db")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM sales", conn)
conn.close()

# Basic data inspection
print("DATASET OVERVIEW")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())

# Create output directory
output_dir = Path("charts")
output_dir.mkdir(exist_ok=True)

# 1. Sales by city
city_sales = df.groupby("city", as_index=False)["amount"].sum()

fig1 = px.bar(
    city_sales,
    x="city",
    y="amount",
    title="Total Sales by City",
    labels={"city": "City", "amount": "Sales Amount"},
    color="city"
)
fig1.write_html(output_dir / "sales_by_city.html")

# 2. Sales by product category
category_sales = df.groupby("category", as_index=False)["amount"].sum()

fig2 = px.pie(
    category_sales,
    names="category",
    values="amount",
    title="Sales Distribution by Category",
    hole=0.4
)
fig2.write_html(output_dir / "sales_by_category.html")

# 3. Quantity versus sales amount
fig3 = px.scatter(
    df,
    x="quantity",
    y="amount",
    color="category",
    hover_name="product",
    title="Quantity vs Sales Amount"
)
fig3.write_html(output_dir / "quantity_vs_sales.html")

print("\nSUCCESS: All three interactive Plotly charts generated.")
print("Charts saved in:", output_dir.resolve())