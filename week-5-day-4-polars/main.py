
from pathlib import Path
import time

import duckdb
import pandas as pd
import polars as pl


# --------------------------------------------------
# 1. Dataset configuration
# --------------------------------------------------

DATA = Path("../week-5-day-3-duckdb/data/sales.csv").resolve()

if not DATA.exists():
    raise FileNotFoundError(
        f"Sales dataset not found: {DATA}\n"
        "Make sure the W5D3 sales.csv file exists."
    )

print("=" * 60)
print("W5D4: POLARS HIGH-PERFORMANCE DATAFRAME OPERATIONS")
print("=" * 60)
print(f"Dataset: {DATA}")


# --------------------------------------------------
# 2. Load the same CSV into Pandas and Polars
# --------------------------------------------------

start = time.perf_counter()
pdf = pd.read_csv(DATA)
pandas_load_time = time.perf_counter() - start

start = time.perf_counter()
pldf = pl.read_csv(DATA)
polars_load_time = time.perf_counter() - start

print(f"\nDataset rows: {len(pdf):,}")
print(f"Pandas loading time: {pandas_load_time:.6f} seconds")
print(f"Polars loading time: {polars_load_time:.6f} seconds")


# --------------------------------------------------
# 3. Create a DuckDB view over the CSV
# --------------------------------------------------

con = duckdb.connect()

csv_path = DATA.as_posix().replace("'", "''")

con.execute(
    f"""
    CREATE VIEW sales AS
    SELECT * FROM read_csv_auto('{csv_path}')
    """
)


# --------------------------------------------------
# 4. Five equivalent analytical operations
# --------------------------------------------------

queries = {
    "Total Sales": """
        SELECT SUM(amount) AS total_sales
        FROM sales
    """,
    "Sales by City": """
        SELECT city, SUM(amount) AS revenue
        FROM sales
        GROUP BY city
        ORDER BY city
    """,
    "Sales by Category": """
        SELECT category, SUM(amount) AS revenue
        FROM sales
        GROUP BY category
        ORDER BY category
    """,
    "High Value Sales": """
        SELECT COUNT(*) AS transaction_count
        FROM sales
        WHERE amount >= 30000
    """,
    "Top Products": """
        SELECT product, SUM(quantity) AS total_quantity
        FROM sales
        GROUP BY product
        ORDER BY product
    """,
}


# --------------------------------------------------
# 5. Pandas implementations
# --------------------------------------------------

def run_pandas(operation):
    if operation == "Total Sales":
        return pdf["amount"].sum()

    if operation == "Sales by City":
        return (
            pdf.groupby("city")["amount"]
            .sum()
            .sort_index()
        )

    if operation == "Sales by Category":
        return (
            pdf.groupby("category")["amount"]
            .sum()
            .sort_index()
        )

    if operation == "High Value Sales":
        return int((pdf["amount"] >= 30000).sum())

    if operation == "Top Products":
        return (
            pdf.groupby("product")["quantity"]
            .sum()
            .sort_index()
        )

    raise ValueError(f"Unknown operation: {operation}")


# --------------------------------------------------
# 6. Polars implementations
# --------------------------------------------------

def run_polars(operation):
    if operation == "Total Sales":
        return pldf.select(
            pl.col("amount").sum()
        ).item()

    if operation == "Sales by City":
        return (
            pldf.group_by("city")
            .agg(pl.col("amount").sum().alias("revenue"))
            .sort("city")
        )

    if operation == "Sales by Category":
        return (
            pldf.group_by("category")
            .agg(pl.col("amount").sum().alias("revenue"))
            .sort("category")
        )

    if operation == "High Value Sales":
        return pldf.filter(
            pl.col("amount") >= 30000
        ).height

    if operation == "Top Products":
        return (
            pldf.group_by("product")
            .agg(pl.col("quantity").sum().alias("total_quantity"))
            .sort("product")
        )

    raise ValueError(f"Unknown operation: {operation}")


# --------------------------------------------------
# 7. Normalize grouped results for validation
# --------------------------------------------------

def normalize_result(operation, duck_result, pandas_result, polars_result):
    if operation == "Total Sales":
        duck_value = duck_result.iloc[0]["total_sales"]
        assert duck_value == pandas_result == polars_result
        return

    if operation == "High Value Sales":
        duck_value = duck_result.iloc[0]["transaction_count"]
        assert duck_value == pandas_result == polars_result
        return

    if operation in ("Sales by City", "Sales by Category"):
        key = "city" if operation == "Sales by City" else "category"

        duck_map = dict(
            zip(duck_result[key], duck_result["revenue"])
        )
        pandas_map = pandas_result.to_dict()
        polars_map = dict(
            zip(
                polars_result[key].to_list(),
                polars_result["revenue"].to_list(),
            )
        )

    elif operation == "Top Products":
        duck_map = dict(
            zip(
                duck_result["product"],
                duck_result["total_quantity"],
            )
        )
        pandas_map = pandas_result.to_dict()
        polars_map = dict(
            zip(
                polars_result["product"].to_list(),
                polars_result["total_quantity"].to_list(),
            )
        )

    else:
        raise ValueError(f"Unknown operation: {operation}")

    assert duck_map == pandas_map == polars_map, (
        f"Results differ for {operation}\n"
        f"DuckDB: {duck_map}\n"
        f"Pandas: {pandas_map}\n"
        f"Polars: {polars_map}"
    )


# --------------------------------------------------
# 8. Run benchmarks and validate results
# --------------------------------------------------

benchmark_results = []
all_passed = True

for operation, sql in queries.items():
    try:
        start = time.perf_counter()
        duck_result = con.execute(sql).fetchdf()
        duck_time = time.perf_counter() - start

        start = time.perf_counter()
        pandas_result = run_pandas(operation)
        pandas_time = time.perf_counter() - start

        start = time.perf_counter()
        polars_result = run_polars(operation)
        polars_time = time.perf_counter() - start

        normalize_result(
            operation,
            duck_result,
            pandas_result,
            polars_result,
        )

        validation = "PASS"

    except Exception as error:
        validation = "FAIL"
        all_passed = False
        print(f"\nValidation error for {operation}: {error}")
        raise

    print(f"\nOperation: {operation}")
    print(f"  DuckDB: {duck_time:.6f} seconds")
    print(f"  Pandas: {pandas_time:.6f} seconds")
    print(f"  Polars: {polars_time:.6f} seconds")
    print(f"  Validation: {validation}")

    benchmark_results.append({
        "Operation": operation,
        "DuckDB_seconds": round(duck_time, 6),
        "Pandas_seconds": round(pandas_time, 6),
        "Polars_seconds": round(polars_time, 6),
        "Validation": validation,
    })


# --------------------------------------------------
# 9. Save benchmark results
# --------------------------------------------------

output_file = Path("benchmark_results.csv")

pd.DataFrame(benchmark_results).to_csv(
    output_file,
    index=False,
)

print("\n" + "=" * 60)
print("BENCHMARK SUMMARY")
print("=" * 60)
print(f"Rows processed: {len(pdf):,}")
print(f"Operations completed: {len(benchmark_results)}")
print(f"All validations passed: {all_passed}")
print(f"Results saved to: {output_file.resolve()}")

print("\nImportant benchmark note:")
print(
    "DuckDB queries the CSV directly, while Pandas and Polars "
    "operate on preloaded data. Query timings are therefore "
    "illustrative, not a perfectly equal comparison."
)

con.close()
