
"""
Cynaris Internship - Week 8 Day 3
PPT Report Export using python-pptx
Project: Superstore Sales Analysis
"""

import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# -----------------------------------------
# 1. LOAD DATASET
# -----------------------------------------

DATA_PATH = (
    r"D:\Cynaris-Internship\week-7-day-2-auto-eda"
    r"\data\sales.csv"
)

df = pd.read_csv(DATA_PATH)

# Convert order date
df["Order Date"] = pd.to_datetime(
    df["Order Date"], dayfirst=True, errors="coerce"
)

print("=" * 55)
print("SUPERSTORE SALES - BUSINESS DATA ANALYSIS")
print("=" * 55)

# -----------------------------------------
# 2. DATASET OVERVIEW
# -----------------------------------------

total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()

print("\n1. DATASET OVERVIEW")
print("Total Records:", len(df))
print("Total Columns:", len(df.columns))
print("Missing Values:", df.isnull().sum().sum())
print("Unique Orders:", total_orders)
print("Unique Customers:", total_customers)

# -----------------------------------------
# 3. TOTAL SALES
# -----------------------------------------

print("\n2. TOTAL SALES")
print(f"Total Sales: ${total_sales:,.2f}")

# -----------------------------------------
# 4. SALES BY CATEGORY
# -----------------------------------------

category_sales = df.groupby("Category")["Sales"].sum()

print("\n3. SALES BY CATEGORY")
print(category_sales.sort_values(ascending=False))

# -----------------------------------------
# 5. SALES BY REGION
# -----------------------------------------

region_sales = df.groupby("Region")["Sales"].sum()

print("\n4. SALES BY REGION")
print(region_sales.sort_values(ascending=False))

# -----------------------------------------
# 6. SALES BY CUSTOMER SEGMENT
# -----------------------------------------

segment_sales = df.groupby("Segment")["Sales"].sum()

print("\n5. SALES BY CUSTOMER SEGMENT")
print(segment_sales.sort_values(ascending=False))

# -----------------------------------------
# 7. SALES BY SHIPPING MODE
# -----------------------------------------

shipping_sales = df.groupby("Ship Mode")["Sales"].sum()

print("\n6. SALES BY SHIPPING MODE")
print(shipping_sales.sort_values(ascending=False))

# -----------------------------------------
# 8. YEARLY SALES
# -----------------------------------------

df["Year"] = df["Order Date"].dt.year

yearly_sales = df.groupby("Year")["Sales"].sum()

print("\n7. SALES BY YEAR")
print(yearly_sales.sort_index())
-
# -----------------------------------------
# 9. GENERATE FIVE KEY INSIGHTS
# -----------------------------------------

print("\n" + "=" * 55)
print("FIVE KEY BUSINESS INSIGHTS")
print("=" * 55)

insights = [
    ("Product Category", category_sales.idxmax(), category_sales.max()),
    ("Region", region_sales.idxmax(), region_sales.max()),
    ("Customer Segment", segment_sales.idxmax(), segment_sales.max()),
    ("Shipping Mode", shipping_sales.idxmax(), shipping_sales.max()),
    ("Year", str(yearly_sales.idxmax()), yearly_sales.max()),
]

for name, leader, value in insights:
    percentage = (value / total_sales) * 100

    print(
        f"{name}: {leader} generated "
        f"${value:,.2f} "
        f"({percentage:.2f}% of total sales)."
    )

# -----------------------------------------
# 10. DATA QUALITY CHECK
# -----------------------------------------

print("\n" + "=" * 55)
print("DATA QUALITY CHECK")
print("=" * 55)

print("Duplicate Rows:", df.duplicated().sum())
print("Missing Sales Values:", df["Sales"].isnull().sum())
print("Invalid Order Dates:", df["Order Date"].isnull().sum())

print("\nAnalysis completed successfully!")
