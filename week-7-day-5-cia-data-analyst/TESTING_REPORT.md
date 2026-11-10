# W7D5 — Testing Report

## Project: Cynaris CIA Data Analyst

### 1. Testing Environment

- Operating System: Windows
- Backend: FastAPI
- Language: Python 3.11
- Data Processing: Pandas
- AI Analysis: PandasAI with local Ollama
- Visualization: Chart.js and Plotly
- Frontend: HTML, CSS, JavaScript

### 2. Test Cases

| Test ID | Test Description | Expected Result | Observed Result | Status |
|---|---|---|---|---|
| TC01 | Upload sales.csv | CSV uploads successfully | 9,800 rows and 18 columns detected | PASS |
| TC02 | Analyze sales by category | Return category-wise sales | Correct category totals returned | PASS |
| TC03 | Analyze sales by region | Return regional sales totals | Four regional totals returned | PASS |
| TC04 | Find highest-sales city | Identify the city with highest sales | New York City, 252,462.55 | PASS |
| TC05 | Generate category pie chart | Display category-wise pie chart | Chart.js pie chart rendered successfully | PASS |

### 3. Dataset Validation

- Total records: 9,800
- Total columns: 18
- Missing values: 11
- Dataset: US Superstore sales dataset

### 4. Visualization Testing

The application successfully generated and displayed a pie chart for sales by category using Chart.js.

The frontend also supports bar charts and includes a dark/light theme switch.

### 5. Issues Identified and Resolved

1. PandasAI sometimes returned a `No result returned` error.
2. Added a deterministic Pandas-based analytical fallback.
3. Corrected stale chart behavior in the frontend.
4. Improved chart rendering and error handling.
5. Added persistent dark/light theme selection.

### 6. Conclusion

The W7D5 CIA Data Analyst application successfully supports CSV upload, dataset inspection, natural-language analysis, and interactive chart visualization.

The application was tested using the Superstore sales dataset.

**Overall result:** Core functional tests passed.

**Note:** This is a local internship demonstration. Production deployment would require additional security, session management, and scalability testing.