

\# W5D4: Pandas vs DuckDB vs Polars



\## Comparison Table



| Criterion | Pandas | DuckDB | Polars |

|---|---|---|---|

| Primary purpose | General-purpose data analysis | SQL analytics and OLAP | High-performance DataFrame operations |

| Syntax | Python methods | SQL | Python expressions |

| Execution | Primarily eager | Optimized analytical query execution | Eager and lazy |

| File handling | Loads CSV into DataFrames | Queries CSV and Parquet directly | Reads files and supports lazy scans |

| Best use case | Data cleaning and analysis | SQL aggregations over analytical data | Fast transformations and analytical pipelines |



\## Benchmark Results



Dataset: 100,000 rows.



\- Pandas was fastest for Total Sales and High Value Sales.

\- Polars was fastest for Sales by City, Sales by Category, and Top Products.

\- Polars loaded the CSV faster than Pandas in this run.

\- DuckDB queried the CSV directly; Pandas and Polars operated on preloaded data.



\## Conclusion



Polars performed well for grouped aggregations in this benchmark.

Pandas performed well for simple scalar calculations.

DuckDB is useful for SQL-based analytics directly on local files.



These timings are illustrative, not a definitive performance ranking.

Results can vary with caching, machine load, data size, and execution strategy.



