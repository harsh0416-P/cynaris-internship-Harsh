# Cynaris CIA â€” AI Data Analyst

## Project Overview

Cynaris CIA is an AI-powered data analysis dashboard that allows users to upload CSV datasets, ask questions in natural language, and visualize analytical results.

The application combines PandasAI, Python, FastAPI, and Chart.js to provide an interactive data analysis experience.

## Features

- CSV dataset upload.
- Dataset preview and statistics.
- Row and column count.
- Missing-value detection.
- Natural-language data analysis.
- Pandas-based analytical fallback.
- Automatic chart data generation.
- Interactive Chart.js visualizations.
- Plotly JSON chart output.
- Dark and light themes.
- Responsive dashboard interface.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Pandas | Data processing and aggregation |
| PandasAI | Natural-language data analysis |
| Ollama | Local LLM execution |
| FastAPI | REST API |
| Plotly | Chart data generation |
| Chart.js | Frontend visualizations |
| HTML | Dashboard structure |
| CSS | Dashboard styling and themes |
| JavaScript | Frontend interaction |

## Project Structure

```text
week-7-day-5-cia-data-analyst/
â”‚
â”œâ”€â”€ main.py
â”œâ”€â”€ csv_analyzer.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ README.md
â”œâ”€â”€ uploads/
â”‚
â””â”€â”€ static/
    â”œâ”€â”€ index.html
    â”œâ”€â”€ style.css
    â””â”€â”€ app.js
```

## Dataset

The technical demonstration uses a Superstore sales dataset.

- Records: 9,800
- Columns: 18
- Missing values: 11
- Main analytical measure: Sales
- Grouping dimensions: Category, Region, City, Segment and others.

**Dataset note:** The current demonstration dataset contains United States Superstore data. It is not an Indian business dataset.

## Sample Analytical Findings

### Sales by Category

| Category | Total Sales |
|---|---:|
| Technology | 827,455.87 |
| Furniture | 728,658.58 |
| Office Supplies | 705,422.33 |

### Sales by Region

| Region | Total Sales |
|---|---:|
| West | 710,219.68 |
| East | 669,518.73 |
| Central | 492,646.91 |
| South | 389,151.46 |

### Highest-Sales City

New York City â€” 252,462.55

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API home |
| GET | `/health` | Health status |
| POST | `/cia/upload-csv` | Upload CSV |
| GET | `/cia/dataset-info/{session_id}` | Dataset information |
| POST | `/cia/analyze` | Analyze dataset |

## Running the Project

### 1. Start Ollama

```powershell
ollama serve
```

Ensure the `llama3.2:3b` model is available.

### 2. Start FastAPI

From the project directory:

```powershell
& "D:\Cynaris-Internship\week-7-day-1-pandasai\.venv311\Scripts\python.exe" -m uvicorn main:app --reload --port 8001
```

### 3. Open the dashboard

```text
http://127.0.0.1:8001/
```

### 4. Upload a CSV file

Upload a dataset and start asking analytical questions.

## Limitations

- Uploaded datasets are held in application memory.
- Dataset sessions are not persistent across server restarts.
- Local LLM response time depends on available hardware.
- Chart generation uses a deterministic aggregation approach for supported questions.
- The current application is a local internship demonstration, not a production deployment.

## Future Improvements

- Support Excel and additional data formats.
- Add more chart types.
- Improve natural-language query understanding.
- Add export options for reports and charts.
- Implement session expiry and persistent storage.
- Add authentication and deployment support.

## Internship Project

**Organization:** Cynaris Solutions Private Limited
**Program:** Data Analyst Internship
**Week:** 7 â€” Day 5
**Project:** CIA Data Analyst Mode â€” Full Feature Project

