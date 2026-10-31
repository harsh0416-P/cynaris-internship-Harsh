# W6D2 - Vanna SQL Training Testing Report

## Project
Vanna AI - Custom SQL Patterns for Domain Data

## Testing Summary
- Total questions tested: 10
- SQL executions successful: 10
- Fully correct AI explanations: 8
- Incorrect AI explanations: 2
- Overall explanation accuracy: 80%

## Test Results

| No. | Question | SQL Result | AI Explanation | Status |
|---|---|---|---|---|
| 1 | Total sales revenue | 289500 | Correct | PASS |
| 2 | Revenue by city | Correct | Mumbai reported 93500 instead of 92500 | FAIL |
| 3 | Average sale amount | 28950 | Reported 29950 | FAIL |
| 4 | Quantity by product | Correct | Correct | PASS |
| 5 | Revenue by category | Correct | Correct | PASS |
| 6 | Highest revenue product | Laptop - 173000 | Correct | PASS |
| 7 | Highest average sale city | Chennai - 36500 | Correct | PASS |
| 8 | Number of transactions | 10 | Correct | PASS |
| 9 | Highest quantity city | Mumbai - 10 | Correct | PASS |
| 10 | Total quantity sold | 30 | Correct | PASS |

## Issues Identified

1. Numerical hallucination in city revenue explanation.
2. Incorrect average sale amount in AI explanation.
3. Currency formatting inconsistency.

## Conclusion

All 10 SQL queries returned database results successfully.
However, two AI-generated explanations contained numerical errors.

The system requires stronger result-grounded answer generation and numerical validation before production use.

## Technology Stack
- Python
- Vanna 2.0.2
- FastAPI
- Ollama
- Llama 3.2 1B
- SQLite
