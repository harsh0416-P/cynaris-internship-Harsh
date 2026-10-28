# Week 5 Day 3 — Pandas vs DuckDB vs Polars

## Objective
Analyze a 100,000-row sales CSV using DuckDB, Pandas, and Polars, compare execution times, and validate the results.

## Comparison

| Criterion | Pandas | DuckDB | Polars |
|---|---|---|---|
| Interface | Python DataFrames | SQL | DataFrame expressions |
| CSV analysis | Loads into memory | Can query CSV directly | Supports eager and lazy processing |
| Best use | Data cleaning and exploration | SQL analytics | Efficient DataFrame transformations |
| Memory considerations | DataFrame must fit in available memory | Can handle larger-than-memory analytical workloads | Lazy scans can reduce unnecessary reads |
| Strength | Familiar Python workflow | SQL and analytical query optimization | Parallel execution and efficient expressions |

## Benchmark Results

Dataset: 100,000 rows.

| Operation | DuckDB (s) | Pandas (s) | Polars (s) |
|---|---:|---:|---:|
| Total Sales | 0.071919 | 0.000884 | 0.001159 |
| Sales by City | 0.076386 | 0.012309 | 0.006282 |
| Sales by Category | 0.108955 | 0.009738 | 0.003733 |
| High Value Sales | 0.094629 | 0.001680 | 0.000826 |
| Top Products | 0.096043 | 0.017383 | 0.004656 |

These are single-run query timings from the local environment. DuckDB queries a CSV-backed view, whereas Pandas and Polars operate on already-loaded DataFrames. The timings therefore do not constitute a controlled, end-to-end performance comparison.

## Validation
All five analytical operations matched across all three tools.

- Total sales: 2,505,000,000
- High-value sales: 40,200

## Conclusion
DuckDB provides a convenient SQL interface for file-based analytics. Pandas is useful for exploratory analysis and data manipulation, while Polars provides an efficient DataFrame API. Tool selection should depend on the workload and should be validated with repeatable benchmarks.
