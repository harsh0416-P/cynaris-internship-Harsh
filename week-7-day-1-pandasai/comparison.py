
from pathlib import Path
import pandas as pd

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

ai = pd.read_csv(output_dir / "pandasai_results.csv")

report = """# W7D1 — PandasAI vs Manual Pandas Comparison

## 1. Dataset
- Dataset: US Superstore Sales CSV
- Rows: 9,800
- Columns: 18
- Note: This is a practice substitute, not an Indian business dataset.

## 2. Manual Pandas Baseline

| Question | Verified result |
|---|---|
| Total Sales | 2,261,536.78 |
| Top 5 Cities | New York City, Los Angeles, Seattle, San Francisco, Philadelphia |
| Highest Sales Category | Technology |
| Average Sales | 230.7691 |
| Highest Sales Region | West — 710,219.6845 |
| Highest Sales Segment | Consumer |
| Top Product | Canon imageCLASS 2200 Advanced Copier — 61,599.824 |
| Unique Order IDs | 4,922 |
| Highest Sales Month | November |
| Highest Sales Category Total | Technology — 827,455.873 |

## 3. PandasAI Evaluation

| Query | PandasAI outcome | Assessment |
|---|---|---|
| 1. Total Sales | 2,261,536.78 | Match |
| 2. Top 5 Cities | Correct top 5 returned | Match |
| 3. Highest Sales Category | Execution/code-generation error | Failed |
| 4. Average Sales | Code-generation error | Failed |
| 5. Sales by Region | Correct region totals returned | Match |
| 6. Highest Sales Segment | Execution error | Failed |
| 7. Top 10 Products | Returned 1,849 rows; first 10 match | Partial |
| 8. Unique Order IDs | 4,922 | Match |
| 9. Highest Sales Month | FileNotFoundError | Failed |
| 10. Sales by Category | Code-generation error | Failed |

## 4. Findings

- Four queries returned answers matching the manual baseline.
- One query returned the correct top 10 entries but included extra rows.
- Five queries failed.
- PandasAI sometimes generated invalid code or referenced a missing CSV file.
- Manual Pandas provided a consistent baseline for validating AI-generated results.

## 5. Conclusion

PandasAI can simplify natural-language data analysis, but its generated code
and answers require validation. For this experiment, manual Pandas was more
reliable than the local PandasAI setup.

## 6. Dataset Limitation

The available practice dataset is the US Superstore dataset.
The Indian business dataset specified in the internship lesson has not yet
been obtained. Mentor confirmation or an approved replacement is required.
"""

(output_dir / "comparison_report.md").write_text(report, encoding="utf-8")

print("Comparison report created:")
print(output_dir / "comparison_report.md")

print("\nPandasAI recorded statuses:")
print(ai[["Question", "Status"]].to_string(index=False))
