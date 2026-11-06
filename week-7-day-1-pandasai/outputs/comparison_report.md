# W7D1 - PandasAI vs Manual Pandas Comparison

## Dataset
- Dataset: US Superstore Sales CSV
- Rows: 9,800
- Columns: 18
- Limitation: This is a practice substitute, not an Indian business dataset.

## Manual Pandas Baseline

| Question | Verified result |
|---|---|
| Total Sales | 2,261,536.78 |
| Top 5 Cities | New York City, Los Angeles, Seattle, San Francisco, Philadelphia |
| Highest Sales Category | Technology |
| Average Sales | 230.7691 |
| Highest Sales Region | West |
| Highest Sales Segment | Consumer |
| Unique Order IDs | 4,922 |
| Highest Sales Month | November |
| Highest Sales Category Total | Technology - 827,455.873 |

## PandasAI Evaluation

| Query | PandasAI outcome | Assessment |
|---|---|---|
| 1. Total Sales | 2,261,536.78 | Match |
| 2. Top 5 Cities | Correct top 5 returned | Match |
| 3. Highest Sales Category | Code-generation error | Failed |
| 4. Average Sales | Code-generation error | Failed |
| 5. Sales by Region | Correct region totals returned | Match |
| 6. Highest Sales Segment | Execution error | Failed |
| 7. Top 10 Products | 1,849 rows returned; first 10 match | Partial |
| 8. Unique Order IDs | 4,922 | Match |
| 9. Highest Sales Month | Missing CSV file error | Failed |
| 10. Sales by Category | Code-generation error | Failed |

## Findings
- Four queries returned answers matching the manual baseline.
- One query returned the correct top 10 entries but included extra rows.
- Five queries failed.
- AI-generated code requires validation before business use.
- Manual Pandas provided a reliable comparison baseline.

## Conclusion
PandasAI supports natural-language data analysis, but its generated code
can fail or return incorrect output. Manual Pandas was more reliable
in this experiment.

## Dataset Limitation
The available dataset is the US Superstore dataset. The Indian business
dataset specified in the internship lesson is still required.
