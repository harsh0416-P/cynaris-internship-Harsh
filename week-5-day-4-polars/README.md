

\# W5D4 — Polars High-Performance DataFrame Operations



\## Objective

Benchmark Pandas, DuckDB, and Polars on a 100,000-row sales dataset.



\## Requirements

Python, Pandas, Polars, and DuckDB.



Install dependencies:



```bash

python -m pip install pandas polars duckdb

```



\## Run

From this directory, activate the repository virtual environment and run:



```bash

python main.py

```



\## Input Dataset

The project reuses the W5D3 dataset:



`../week-5-day-3-duckdb/data/sales.csv`



\## Outputs

\- `main.py` — five analytical operations and validation

\- `benchmark\_results.csv` — measured execution times

\- `comparison.md` — library comparison



\## Benchmark Notes

DuckDB queries the CSV directly, whereas Pandas and Polars use preloaded data. The timings are not a perfectly equal comparison.



