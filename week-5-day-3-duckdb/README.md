# DuckDB: In-Process SQL Analytics

**Cynaris Internship — Week 5, Day 3**

## Overview
This project compares DuckDB, Pandas, and Polars on a generated sales dataset containing 100,000 rows.

## Features
- Generates a sales CSV dataset.
- Runs five analytical queries.
- Compares execution timings across three libraries.
- Validates analytical results for consistency.
- Exports benchmark results and SQL queries.

## Requirements
- Python
- DuckDB
- Pandas
- Polars
- PyArrow (required by the current validation conversion workflow)

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python main.py
```

## Generated Files
- `data/sales.csv`
- `benchmark_results.csv`
- `queries.sql`
- `comparison.md`

## Validation
All five analytical operations passed cross-library validation in the recorded run.

## Benchmark Notes
The initial timings are illustrative rather than a definitive performance ranking. DuckDB queries the CSV through a view, while Pandas and Polars load the CSV into DataFrames before the operations. Repeatable, equivalent end-to-end tests are needed for a fair comparison.
