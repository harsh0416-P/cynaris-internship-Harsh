# Week 5 Day 1 — PandasAI: Natural Language to DataFrame Operations

## Project Overview
This project analyzes Indian air-quality data using PandasAI, a local Ollama language model, and Pandas for reliable data analysis.

## Dataset
- File: `data/indian_air_quality.csv`
- Rows: 3,752
- Columns: 11
- Unique cities: 282
- Pollutants: CO, NH3, NO2, OZONE, PM10, PM2.5, SO2

## Features
- Loads and validates the CSV dataset.
- Attempts natural-language queries using PandasAI and Ollama (`llama3.2:1b`).
- Answers 10 analysis questions using Pandas.
- Compares three manual Pandas calculations.
- Logs errors for troubleshooting.
- Saves query results to text files.

## Analysis Questions
1. Total record count.
2. States represented.
3. Unique city count.
4. Counts by pollutant.
5. Overall average pollutant value.
6. Five cities with the highest average pollutant value.
7. Average pollutant value by pollutant type.
8. Missing values by column.
9. Records where `pollutant_avg > 100`.
10. Average pollutant value by state and pollutant.

## Files
- `main.py` — PandasAI and Ollama integration.
- `reliable_analysis.py` — deterministic Pandas analysis.
- `manual_pandas_results.txt` — three manual baseline calculations.
- `pandasai_results.txt` — actual PandasAI results and failures.
- `error_log.txt` — recorded errors.
- `reliable_results.txt` — results from the reliable analysis.
- `data/indian_air_quality.csv` — input dataset.

## Setup
Install the dependencies in `requirements.txt`, ensure Ollama is installed, and download the model:

```powershell
ollama pull llama3.2:1b
```

Activate the project virtual environment and run:

```powershell
python main.py
python reliable_analysis.py
```

## Findings
- 3,752 records and 282 unique cities.
- 308 missing values in each of `pollutant_min`, `pollutant_max`, and `pollutant_avg`.
- The overall mean of `pollutant_avg` is 49.02.
- The highest city-level average in this dataset is Baraut at 134.50.

## Limitations
The local model sometimes generates invalid code. PandasAI failures are logged and retained as failures; the deterministic Pandas analysis provides a separate, reproducible result set. Manual analysis results must not be represented as successful PandasAI answers.
