

\# W5D5 — EDA Tool Comparison



| Criterion | Pandas | DuckDB | Polars |

|---|---|---|---|

| Primary purpose | Data cleaning and analysis | SQL analytics | High-performance DataFrame processing |

| Interface | Python DataFrame API | SQL queries | Python expressions |

| Typical strength | Flexible data manipulation | SQL aggregations over files and tables | Fast transformations and lazy execution |

| File access | Reads CSV into a DataFrame | Can query CSV directly | Supports eager reads and lazy scans |

| Best use case | General EDA and reporting | Analytical SQL queries | Efficient DataFrame pipelines |



\## Project Findings



\- Dataset size: 100,000 rows.

\- Total revenue: 2,505,000,000.

\- Highest-revenue city: Ahmedabad.

\- Highest-revenue category: Books.

\- Highest-quantity product: Book.

\- Missing values: zero in all six columns.



\## Validation



Key metrics from Pandas were cross-checked against DuckDB SQL.



\## AI Analysis Status



The current `ai\_analysis.py` report uses Python and Pandas rules to produce insights. It is not an LLM-generated response. PandasAI is installed in a separate Python 3.11 environment, but an API key has not been configured.



\## Limitations



This project provides descriptive analysis, not causal conclusions or predictions. Tool performance comparisons depend on data loading, execution strategy, caching, and hardware.



