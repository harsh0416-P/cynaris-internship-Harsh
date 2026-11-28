# Indian Business Data — Production Architecture

A modular Python EDA pipeline developed as part of the Cynaris Solutions Data Analytics Internship (Week 12, Day 1).

## Project Structure

```text
week-12-day-1-production-architecture/
├── config/
│   └── settings.json
├── data/
│   └── indian_business_data.csv
├── docs/
│   └── architecture_review.md
├── logs/
│   └── pipeline.log
├── outputs/
│   ├── charts/
│   ├── analysis_summary.json
│   └── summary CSV files
└── src/
    └── production_pipeline.py
```

## Features

- Centralized JSON configuration
- CSV data ingestion
- Data validation
- Modular business analysis
- Automated chart generation
- CSV and JSON exports
- Structured execution logging
- Error handling

## Requirements

- Python 3.10+
- pandas
- matplotlib

Install dependencies:

```bash
pip install pandas matplotlib
```

## Run the Pipeline

From the repository root:

```bash
python week-12-day-1-production-architecture/src/production_pipeline.py
```

## Outputs

The pipeline generates:

- Seven analytical CSV summary files
- One JSON analysis summary
- Six PNG charts
- An execution log at `logs/pipeline.log`

## Documentation

See `docs/architecture_review.md` for the architecture assessment, implementation details, execution results, and future production improvements.

## Status

Pipeline execution and output generation verified successfully on 28 November 2026.