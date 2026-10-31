# W6D1 Testing Report — Vanna SQL Analyst

## Environment
- Vanna: 2.0.2
- LLM: Ollama llama3.2:1b
- Database: SQLite
- API: FastAPI
- Endpoint: POST /cia/sql-analyst

## API Testing Results

| Test | Question | SQL Result | AI Interpretation |
|---|---|---|---|
| 1 | Total sales revenue | ₹289,500 | Correct |
| 2 | Number of sales records | 10 | Correct |
| 3 | Average sale amount | ₹28,950 | Incorrectly reported ₹29,950 |
| 4 | Highest revenue city | Bengaluru, ₹94,000 | Correct |
| 5 | Revenue by city | Correct database values | Incorrectly inflated values |

## Observations

- FastAPI endpoint responded successfully.
- Vanna connected to the SQLite database.
- SQL execution returned correct results in the observed tests.
- The small local language model sometimes misinterpreted numerical results.
- SQL output and AI-generated explanations must be validated separately.

## Limitations

- Only five natural-language questions were attempted.
- Ten-query testing is not yet complete.
- AI answer accuracy needs improvement.
- Read-only SQL execution needs stronger enforcement before production use.

## Conclusion

The local Vanna and FastAPI integration is working. However, the observed numerical interpretation errors show why database results should be validated independently of LLM-generated explanations.