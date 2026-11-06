# W7D2 - CIA Auto EDA

## Project Overview
Generate two automated EDA reports using ydata-profiling and SweetViz.

## Dataset
- File: data/sales.csv
- Rows: 9,800
- Columns: 18
- Source: W4 Capstone US Superstore dataset.

## Technologies
- Python 3.11
- Pandas
- NumPy
- ydata-profiling
- SweetViz
- Matplotlib

## Project Structure
- data/ - Input dataset
- reports/ - Generated HTML reports
- scripts/ - Python scripts
- requirements.txt - Dependencies

## Run the project
Activate environment:
.\.venv\Scripts\Activate.ps1

Install dependencies:
python -m pip install -r requirements.txt

Generate reports:
python .\scripts\run_eda.py

Validate reports:
python .\scripts\validate_reports.py

## Generated Reports
- reports/profile_report.html
- reports/sweetviz_report.html

## Validation
Both reports passed file existence and size validation.
