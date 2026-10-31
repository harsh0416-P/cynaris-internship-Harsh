# Week 6 Day 1 — Vanna Setup: NL to SQL on Real Database

## Project Overview

This project implements a Natural Language to SQL system using Vanna AI, Ollama, SQLite, and FastAPI.

Users can submit questions in natural language through a REST API. The Vanna agent uses a local LLM to generate SQL queries and execute them against a SQLite sales database.

## Technologies Used

- Python
- Vanna AI 2.0.2
- Ollama
- Llama 3.2 (1B)
- SQLite
- FastAPI
- Uvicorn
- Pandas

## Project Structure

```text
week-6-day-1-vanna/
│
├── data/
│   └── sales.db
│
├── outputs/
│   └── query_results/
│
├── main.py
├── create_database.py
├── verify_database.py
├── requirements.txt
└── README.md
```

## Database Details

Database: `sales.db`

Table: `sales`

| Column | Description |
|---|---|
| sale_id | Unique sale identifier |
| customer_name | Customer name |
| product | Product name |
| category | Product category |
| amount | Sale amount |
| city | Customer city |
| quantity | Quantity sold |

The sample database contains 10 sales records.

## System Architecture

1. User submits a natural-language question.
2. FastAPI receives the request.
3. Vanna agent processes the question.
4. Ollama runs the local Llama 3.2 model.
5. Vanna generates an SQL query.
6. SQLite executes the SQL query.
7. The API returns the database result and AI-generated response.

## API Endpoint

**POST** `/cia/sql-analyst`

Example request:

```json
{
  "question": "What is the total sales revenue?"
}
```

Example local URL:

`http://127.0.0.1:8000/cia/sql-analyst`

Swagger documentation:

`http://127.0.0.1:8000/docs`

## Setup Instructions

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Activate environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start Ollama

Ensure Ollama is running and the model is available:

```powershell
ollama list
```

### 5. Start FastAPI

```powershell
uvicorn main:app --reload
```

## Testing and Observations

The API was tested with natural-language questions involving:

- Total sales revenue
- Number of sales records
- Average sale amount
- Revenue by city
- Highest-revenue city

SQL execution returned correct database results in the observed tests.

### Identified AI Accuracy Issue

During average revenue testing:

- SQLite returned `28950.0`.
- The AI generated an answer of `$29,950.00`.

During revenue-by-city testing:

- SQLite returned Bengaluru revenue of `94000.0`.
- The AI generated `₹94,000,000`.

These results demonstrate that an LLM-generated explanation can differ from the actual database output.

The API was modified to expose `database_result` separately from `ai_answer`, allowing independent verification.

## Conclusion

The project demonstrates a local Natural Language to SQL workflow using Vanna, Ollama, SQLite, and FastAPI.

It also highlights the importance of validating AI-generated answers against actual database results before using them in analytical or business decisions.

## Future Improvements

- Enforce read-only SQL execution.
- Improve AI response grounding.
- Add SQL query validation.
- Expand the test dataset.
- Add automated API tests.
- Improve error handling and logging.
