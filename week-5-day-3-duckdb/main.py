
from pathlib import Path
from time import perf_counter

import duckdb
import pandas as pd
import polars as pl

# ==========================================
# 1. SETUP AND DATASET
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "sales.csv"
ROWS = 100_000

print("\n=== 1. GENERATING DATASET ===")

if not CSV_PATH.exists():
    df = pd.DataFrame({
        "sale_id": range(1, ROWS + 1),
        "city": [
            ["Bengaluru", "Mumbai", "Delhi", "Ahmedabad"][i % 4]
            for i in range(ROWS)
        ],
        "category": [
            ["Electronics", "Clothing", "Food", "Books"][i % 4]
            for i in range(ROWS)
        ],
        "product": [
            ["Laptop", "Phone", "Shirt", "Book"][i % 4]
            for i in range(ROWS)
        ],
        "quantity": [(i % 10) + 1 for i in range(ROWS)],
        "amount": [((i % 500) + 1) * 100 for i in range(ROWS)]
    })
    df.to_csv(CSV_PATH, index=False)

# Always verify the actual CSV row count
row_count = sum(1 for _ in open(CSV_PATH, encoding="utf-8")) - 1
print(f"Dataset ready: {row_count:,} rows")
print(f"File: {CSV_PATH}")

# ==========================================
# 2. FIVE SQL QUERIES
# ==========================================

queries = {
    "Total Sales": """
        SELECT SUM(amount) AS total_sales
        FROM sales
    """,
    "Sales by City": """
        SELECT city, SUM(amount) AS revenue
        FROM sales
        GROUP BY city
        ORDER BY revenue DESC, city
    """,
    "Sales by Category": """
        SELECT category, SUM(amount) AS revenue
        FROM sales
        GROUP BY category
        ORDER BY revenue DESC, category
    """,
    "High Value Sales": """
        SELECT COUNT(*) AS sale_count
        FROM sales
        WHERE amount >= 30000
    """,
    "Top Products": """
        SELECT product, SUM(quantity) AS units_sold
        FROM sales
        GROUP BY product
        ORDER BY units_sold DESC, product
    """
}

# ==========================================
# 3. DUCKDB
# ==========================================

print("\n=== 2. DUCKDB ANALYTICS ===")

con = duckdb.connect()

# read_csv_auto detects the header and column types
safe_path = str(CSV_PATH.resolve()).replace("\\", "/").replace("'", "''")

con.execute(
    f"CREATE VIEW sales AS "
    f"SELECT * FROM read_csv_auto('{safe_path}', header=true)"
)

duck_results = {}
duck_times = {}

for name, query in queries.items():
    start = perf_counter()
    result = con.execute(query).fetchdf()
    duck_times[name] = perf_counter() - start
    duck_results[name] = result

    print(f"\n{name}")
    print(result.to_string(index=False))

# ==========================================
# 4. PANDAS
# ==========================================

print("\n=== 3. PANDAS ANALYTICS ===")

start = perf_counter()
pdf = pd.read_csv(CSV_PATH)
pandas_load_time = perf_counter() - start

pandas_operations = {
    "Total Sales": lambda: pd.DataFrame({
        "total_sales": [pdf["amount"].sum()]
    }),
    "Sales by City": lambda: (
        pdf.groupby("city", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "revenue"})
        .sort_values(
            ["revenue", "city"],
            ascending=[False, True]
        )
        .reset_index(drop=True)
    ),
    "Sales by Category": lambda: (
        pdf.groupby("category", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "revenue"})
        .sort_values(
            ["revenue", "category"],
            ascending=[False, True]
        )
        .reset_index(drop=True)
    ),
    "High Value Sales": lambda: pd.DataFrame({
        "sale_count": [(pdf["amount"] >= 30000).sum()]
    }),
    "Top Products": lambda: (
        pdf.groupby("product", as_index=False)["quantity"]
        .sum()
        .rename(columns={"quantity": "units_sold"})
        .sort_values(
            ["units_sold", "product"],
            ascending=[False, True]
        )
        .reset_index(drop=True)
    )
}

pandas_results = {}
pandas_times = {}

for name, operation in pandas_operations.items():
    start = perf_counter()
    pandas_results[name] = operation()
    pandas_times[name] = perf_counter() - start

    print(f"\n{name}")
    print(pandas_results[name].to_string(index=False))

# ==========================================
# 5. POLARS
# ==========================================

print("\n=== 4. POLARS ANALYTICS ===")

start = perf_counter()
pldf = pl.read_csv(CSV_PATH)
polars_load_time = perf_counter() - start

polars_operations = {
    "Total Sales": lambda: pldf.select(
        pl.col("amount").sum().alias("total_sales")
    ),
    "Sales by City": lambda: (
        pldf.group_by("city")
        .agg(pl.col("amount").sum().alias("revenue"))
        .sort(["revenue", "city"], descending=[True, False])
    ),
    "Sales by Category": lambda: (
        pldf.group_by("category")
        .agg(pl.col("amount").sum().alias("revenue"))
        .sort(["revenue", "category"], descending=[True, False])
    ),
    "High Value Sales": lambda: pldf.select(
        (pl.col("amount") >= 30000).sum().alias("sale_count")
    ),
    "Top Products": lambda: (
        pldf.group_by("product")
        .agg(pl.col("quantity").sum().alias("units_sold"))
        .sort(["units_sold", "product"], descending=[True, False])
    )
}

polars_results = {}
polars_times = {}

for name, operation in polars_operations.items():
    start = perf_counter()
    polars_results[name] = operation()
    polars_times[name] = perf_counter() - start

    print(f"\n{name}")
    print(polars_results[name])

# ==========================================
# 6. VALIDATION
# ==========================================

print("\n=== 5. VALIDATION ===")

for name in queries:
    duck = duck_results[name].reset_index(drop=True)
    pandas_result = pandas_results[name].reset_index(drop=True)
    polars_result = polars_results[name].to_pandas().reset_index(drop=True)

    pd.testing.assert_frame_equal(
        duck, pandas_result, check_dtype=False
    )
    pd.testing.assert_frame_equal(
        duck, polars_result, check_dtype=False
    )

    print(f"PASS: {name}")

print("All five operations match!")

# ==========================================
# 7. BENCHMARK
# ==========================================

print("\n=== 6. BENCHMARK RESULTS ===")

print(f"Pandas CSV loading: {pandas_load_time:.6f} sec")
print(f"Polars CSV loading: {polars_load_time:.6f} sec")

benchmark = pd.DataFrame([
    {
        "operation": name,
        "duckdb_seconds": duck_times[name],
        "pandas_seconds": pandas_times[name],
        "polars_seconds": polars_times[name]
    }
    for name in queries
])

print(benchmark.to_string(index=False))

benchmark.to_csv(BASE_DIR / "benchmark_results.csv", index=False)

# Save the SQL queries for submission
with open(BASE_DIR / "queries.sql", "w", encoding="utf-8") as file:
    for name, query in queries.items():
        file.write(f"-- {name}\n{query.strip()};\n\n")

con.close()

print("\nSUCCESS: All five queries passed validation.")
print("Created: benchmark_results.csv")
print("Created: queries.sql")
print("Completed: DuckDB, Pandas and Polars comparison")
