# W7D1 - CSV Upload and PandasAI Queries

## Project Overview
This project explores natural-language data analysis using PandasAI,
Pandas, and a locally hosted LLM through Ollama.

## Technologies
- Python 3.11
- Pandas
- PandasAI 2.3.2
- Ollama
- Llama 3.2 3B

## Dataset
- File: data/sales.csv
- Rows: 9,800
- Columns: 18
- Source: US Superstore practice dataset.

Note: This is a substitute practice dataset, not the Indian business
dataset specified in the internship lesson. Mentor confirmation is pending.

## Setup

Create and activate a Python 3.11 virtual environment:

    py -3.11 -m venv .venv311
    .venv311\Scripts\Activate.ps1

Install dependencies:

    pip install pandas==1.5.3 numpy==1.26.4 pandasai==2.3.2 matplotlib PyYAML==6.0.3

Ensure Ollama is installed and the model is available:

    ollama pull llama3.2:3b

## Run

Start Ollama, activate the virtual environment, then run:

    python main.py

Generate manual validation:

    python manual_validation.py

Generate the comparison report:

    python comparison_report.py

## Outputs
- outputs/pandasai_results.csv
- outputs/manual_baseline.txt
- outputs/manual_comparison.txt
- outputs/comparison_report.md
- logs/pandasai_errors.log

## Findings
PandasAI successfully returned some answers but failed on several
queries due to generated-code and execution errors.

Manual Pandas calculations were used as the validation baseline.
AI-generated answers must be checked before business use.

## Limitations
- Local LLM output is not consistently reliable.
- The dataset is a US Superstore practice dataset.
- The required Indian business dataset is pending mentor confirmation.
