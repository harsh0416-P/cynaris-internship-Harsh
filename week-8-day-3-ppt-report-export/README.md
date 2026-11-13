# Superstore Business Report Generator

## Project Overview

This project generates an automated business sales report using Python, Pandas, Groq AI, and python-pptx.

It analyzes the Superstore Sales dataset, calculates important business insights, generates an AI-powered executive summary, and exports the results into an 8-slide PowerPoint presentation.

## Project Objectives

- Analyze sales data using Pandas.
- Calculate sales performance across different business dimensions.
- Generate an executive summary using Groq AI.
- Create charts using python-pptx.
- Export a professional PowerPoint business report.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data analysis and processing |
| python-pptx | PowerPoint generation |
| Groq API | AI executive summary |
| python-dotenv | Environment variable management |

## Project Structure

```text
week-8-day-3-ppt-report-export/
│
├── ai_summary.py
├── generate_ppt.py
├── project_task_day3.py
├── requirements.txt
├── README.md
├── TESTING_REPORT.md
├── .env.example
├── evidence/
│
└── superstore_business_report.pptx
```

## Dataset

The project uses the Superstore Sales CSV dataset.

Dataset location:

```text
D:\Cynaris-Internship\week-7-day-2-auto-eda\data\sales.csv
```

The analysis includes:

- Category-wise sales
- Region-wise sales
- Customer segment analysis
- Shipping mode analysis
- Yearly sales trends

## Installation

### 1. Activate the Python environment

```powershell
& "D:\Cynaris-Internship\.venv\Scripts\Activate.ps1"
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## Groq API Configuration

The project reads the Groq API key from the existing W8D1 environment file:

```text
D:\Cynaris-Internship\week-8-day-1-executive-summary\.env
```

The environment file should contain:

```text
GROQ_API_KEY=your_groq_api_key
```

Never upload the actual `.env` file or expose your API key on GitHub.

## How to Run

Run the PowerPoint generator:

```powershell
python generate_ppt.py
```

The script:

1. Loads the sales dataset.
2. Calculates business insights.
3. Generates an executive summary using Groq.
4. Creates five business charts.
5. Generates an 8-slide PowerPoint presentation.

## PowerPoint Report Structure

| Slide | Content |
|---|---|
| 1 | Title Slide |
| 2 | AI-Generated Executive Summary |
| 3 | Sales by Category |
| 4 | Sales by Region |
| 5 | Sales by Customer Segment |
| 6 | Sales by Shipping Mode |
| 7 | Yearly Sales |
| 8 | Business Recommendations |

## Key Results

- Total sales analyzed: $2,261,536.78
- PowerPoint slides generated: 8
- Charts generated: 5
- AI executive summary: Successfully generated
- PowerPoint export: Successful

## Testing

See [TESTING_REPORT.md](TESTING_REPORT.md) for test cases and validation results.

## Limitations

- Dataset path is currently predefined.
- The project does not yet include an interactive CSV upload interface.
- Sales data alone cannot establish profit or business profitability.
- The report's visual design can be improved further.

## Output

Generated presentation:

```text
superstore_business_report.pptx
```

## Internship Task

**Program:** Cynaris Data Analyst Internship  
**Week:** 8  
**Day:** 3  
**Task:** PPT Report Export using python-pptx

