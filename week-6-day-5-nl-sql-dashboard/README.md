

\# Cynaris NL SQL Dashboard



\## Project Overview



The Cynaris NL SQL Dashboard is an AI-powered data analytics application that allows users to query a sales database using natural language.



Users can ask questions in English and receive SQL-generated database results, AI explanations, tables, and visual analysis.



\## Features



\- Natural Language to SQL queries

\- AI-powered responses using Vanna and Ollama

\- SQLite database integration

\- FastAPI backend

\- Interactive dashboard interface

\- Dynamic bar chart visualization

\- Database results displayed in tables

\- CSV export functionality

\- Conversation ID support



\## Technologies Used



| Technology | Purpose |

|---|---|

| Python | Backend programming |

| Vanna 2.0.2 | Natural Language SQL |

| Ollama | Local language model |

| Llama 3.2:1b | AI model |

| FastAPI | REST API |

| SQLite | Database |

| HTML | Dashboard structure |

| CSS | Dashboard styling |

| JavaScript | Frontend functionality |



\## Project Structure



```text

week-6-day-5-nl-sql-dashboard/

│

├── data/

│   └── sales.db

│

├── static/

│   └── index.html

│

├── outputs/

│   └── cynaris\_query\_results.csv

│

├── tests/

│

├── main.py

├── database.py

├── training\_data.py

├── requirements.txt

├── .env

└── README.md

```



\## Database Information



Database: SQLite



Table: sales



Columns:



\- sale\_id

\- customer\_name

\- product

\- category

\- amount

\- city

\- quantity



Total records: 10



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/harsh8907-k/cynaris-internship-Harsh.git

```



\### 2. Navigate to the project



```bash

cd week-6-day-5-nl-sql-dashboard

```



\### 3. Create virtual environment



```bash

python -m venv .venv

```



\### 4. Activate environment



Windows PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



\### 5. Install dependencies



```bash

pip install -r requirements.txt

```



\### 6. Start Ollama



Make sure Ollama is installed and the model is available:



```bash

ollama pull llama3.2:1b

```



\### 7. Run the application



```bash

python -m uvicorn main:app --reload

```



\## Access the Application



Dashboard:



http://127.0.0.1:8000



API Documentation:



http://127.0.0.1:8000/docs



Health Check:



http://127.0.0.1:8000/health



\## Example Natural Language Queries



1\. Show all sales records.

2\. Calculate total sales revenue.

3\. Show total sales revenue by city.

4\. Find the top five products by revenue.

5\. Show customers who spent more than 30000.



\## Sample Results



| City | Total Sales |

|---|---:|

| Bengaluru | 94000 |

| Chennai | 73000 |

| Delhi | 30000 |

| Mumbai | 92500 |



\## Testing



The application was tested for:



\- Database connectivity

\- Ollama model availability

\- FastAPI endpoint functionality

\- Natural language SQL queries

\- AI-generated explanations

\- Database result display

\- Dynamic chart generation

\- CSV export



\## Important Note



The database query results are the source of truth. AI-generated explanations may contain numerical inaccuracies and should be checked against SQL results.



\## Author



Harsh Sanchaniya



Cynaris Data Analyst Internship



Week 6 - Day 5 Project
