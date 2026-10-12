# Week 2 Day 6 — Data Governance

## Objective
Validate sales data, define a data contract, and classify personal information.

## Deliverables
- `sales.csv` — Clean sample dataset
- `sales_with_errors.csv` — Dataset with three injected errors
- `gx_validation.py` — Great Expectations validation suite
- `validation_report.html` — HTML summary of actual GX results
- `error_validation_report.html` — Error-checking summary
- `data_contract.yaml` — Producer-consumer data contract
- `data_quality_scorecard.md` — DAMA quality assessment
- `create_dataset.py` — Dataset creation script
- `inject_errors.py` — Intentional error injection
- `validate_errors.py` — Additional pandas verification

## Run the project
From this folder, run:

```powershell
& ..\week-2-day-1-visualisation\.venv\Scripts\python.exe .\create_dataset.py
& ..\week-2-day-1-visualisation\.venv\Scripts\python.exe .\inject_errors.py
& ..\week-2-day-1-visualisation\.venv\Scripts\python.exe .\gx_validation.py
```

## Validation results
The corrupted dataset should produce 3 failed and 5 passed expectations.

## PII classification
Customer email is confidential personal information. Mask it in dashboard outputs and restrict access to raw data.

## Limitations
Timeliness requires ingestion timestamps. Cross-table consistency requires related tables. The HTML validation file is a custom summary, not the native GX Data Docs report.
