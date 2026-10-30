# Indian Business Dataset — EDA Findings

## Dataset
- Rows: 100,000
- Columns: 6
- CSV loading time: 0.1156 seconds

## Business Metrics
- Total revenue: 2,505,000,000.00
- Average sale amount: 25,050.00
- High-value transactions (amount >= 30000): 40,200
- Duplicate rows: 0

## Key Findings
- Highest-revenue city: Ahmedabad (630,000,000.00)
- Highest-revenue category: Books (630,000,000.00)
- Highest-quantity product: Book (150,000 units)

## Data Quality
Missing values are recorded in `data_quality_report.json`.
Summary statistics are saved in `summary_statistics.csv`.

## Validation
Pandas revenue, average sale, and high-value transaction count
were cross-checked against DuckDB SQL results successfully.

## Limitations
This is descriptive analysis of the supplied dataset. It does not
establish causal relationships or guarantee future business performance.
