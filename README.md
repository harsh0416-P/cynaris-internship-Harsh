# 🚀 Data Analytics Internship — Cynaris Solutions

## 👋 About This Repository

Welcome to my Data Analytics Internship repository at Cynaris Solutions Private Limited, Bengaluru.

I am pursuing an MSc in Data Science and used this internship to develop practical skills in data analytics, database management, Python programming, data visualization, statistical analysis and AI-powered data applications.

This repository documents my 7-week internship journey, including assignments, practical implementations, datasets, SQL queries, Python scripts, analytical reports and projects.

My goal was not just to complete assignments but to understand how real-world data problems are solved using analytical and AI technologies.

## 🎯 Internship Objectives

- Develop strong SQL and database management skills.
- Perform data cleaning, transformation and exploratory data analysis.
- Work with Python libraries for data analytics.
- Build meaningful data visualizations, dashboards and reports.
- Understand statistical analysis and predictive modeling.
- Explore AI-powered analytics and Natural Language to SQL.
- Learn Git and GitHub workflows.
- Develop practical projects suitable for real-world applications.

## 🛠️ Technical Skills & Technologies

| Category | Technologies |
|---|---|
| Programming | Python |
| Database | SQL, SQLite, DuckDB |
| Data Analysis | Pandas, NumPy, Polars |
| Visualization | Matplotlib, Seaborn |
| Automated EDA | AutoViz, SweetViz, ydata-profiling |
| AI & LLM | Vanna, PandasAI, Ollama (Llama 3.2) |
| API Development | FastAPI |
| Data Quality | Great Expectations |
| BI & Reporting | Power BI (DAX), Excel, Looker Studio, Apache Superset |
| Development Tools | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

## 📊 Internship at a Glance

| Week | Focus | Main Tools |
|---|---|---|
| 1 | SQL Fundamentals | SQL, CSV exports |
| 2 | Python for Data Analytics | Pandas, NumPy, Matplotlib, Seaborn, Great Expectations |
| 3 | Business Intelligence & Reporting | Power BI, DAX, Excel, Looker Studio |
| 4 | Statistics & Predictive Analytics | Python, regression analysis |
| 5 | Advanced Data Analytics & AI Tools | PandasAI, AutoViz, SweetViz, DuckDB, Polars |
| 6 | AI-Powered Analytics | Vanna, Ollama, SQLite, FastAPI, Superset |
| 7 | PandasAI & Automated EDA | PandasAI, ydata-profiling, SweetViz |

## 📚 Internship Learning Journey

### Week 1 — SQL Fundamentals

**Focus:** Understanding relational databases and writing SQL queries.

**Topics:** SELECT, WHERE and filtering · JOIN operations · GROUP BY and HAVING · Subqueries and Common Table Expressions (CTEs)

**Practical work:**
- Created SQL databases and tables.
- Practised data retrieval and filtering.
- Combined multiple tables using JOINs.
- Performed aggregations and grouped analysis.
- Saved queries as SQL files and exported results to CSV.

### Week 2 — Python for Data Analytics

**Focus:** Working with datasets using Python and analytical libraries.

**Topics:** Data visualization · data cleaning and missing values · NumPy · data governance · data quality and validation

**Practical work:**
- Explored and manipulated datasets with Pandas and NumPy.
- Created charts using Matplotlib and Seaborn.
- Handled missing values and compared data quality.
- Implemented data quality checks and explored Great Expectations.
- Generated validation reports and data quality scorecards.

### Week 3 — Business Intelligence & Reporting

**Focus:** Turning data into business insights.

**Topics:** Power BI · DAX basics · Excel-based analysis · Looker Studio · KPI design

**Practical work:**
- Built Power BI work and practised DAX basics.
- Analysed data in Excel.
- Created visual reports in Looker Studio.
- Designed KPI-focused analytical outputs.

### Week 4 — Statistics & Predictive Analytics

**Focus:** Applying statistical methods to understand data and relationships.

**Topics:** Descriptive statistics · probability · regression analysis · hypothesis testing

**Practical work:**
- Performed descriptive statistical analysis.
- Explored probability concepts.
- Built regression analysis workflows.
- Practised hypothesis testing.
- Completed a statistical capstone project.

### Week 5 — Advanced Data Analytics & AI Tools

**Focus:** Modern analytical tools and AI-assisted workflows.

**Topics:** PandasAI · AutoViz and SweetViz · DuckDB · Polars · AI-powered EDA

**Practical work:**
- Automated exploratory data analysis and generated visual reports.
- Queried analytical datasets using DuckDB.
- **Performance comparison:** benchmarked five analytical operations across Pandas, Polars and DuckDB on a 100,000-row sales dataset and validated that the results matched.
- Explored AI-assisted data analysis and documented findings.

### Week 6 — AI-Powered Analytics

**Focus:** Building AI-powered Natural Language to SQL applications and reporting.

**Day 1 — Vanna setup (NL to SQL on a real database)**
- Configured Vanna 2.0.2 with Ollama and the Llama 3.2:1b local language model.
- Created a SQLite sales database and integrated Vanna with FastAPI.
- Developed the `POST /cia/sql-analyst` endpoint.
- Tested natural-language questions and documented results and model limitations.

**Day 2 — Vanna training:** custom question-to-SQL training and business rules.

**Day 3 — Apache Superset:** Superset for BI and dashboards.

**Day 4 — Executive reporting.**

**Day 5 — Natural-language SQL dashboard.**

<!-- Verify: add one or two real lines for Days 3 to 5 from those folders' own READMEs. -->

### Week 7 — PandasAI & Automated EDA

**Day 1 — CSV upload and PandasAI queries**
- Explored natural-language data analysis with PandasAI 2.3.2, Pandas and a locally hosted Llama 3.2 3B model through Ollama (Python 3.11).
- Dataset: `data/sales.csv`, 9,800 rows and 18 columns (US Superstore practice dataset).

**Day 2 — CIA Auto EDA**
- Used **ydata-profiling** and **SweetViz** on the 9,800-row, 18-column sales dataset.
- Generated **two HTML reports**: `profile_report.html` and `sweetviz_report.html`.
- Created automation (`run_eda.py`) and validation (`validate_reports.py`) scripts.
- Saved report snapshots in `docs/` and documented the outputs.

> **Dataset note:** the Week 7 data is a substitute practice dataset (US Superstore), not the Indian business dataset named in the internship lesson. Mentor confirmation was pending when this was written.

## 💻 Featured Projects

### Vanna SQL Analyst (Week 6)

A local AI-powered SQL assistant that lets users ask questions about sales data in natural language.

- **LLM:** Ollama, Llama 3.2:1b
- **NL-to-SQL framework:** Vanna 2.0.2
- **Database:** SQLite
- **API:** FastAPI (`POST /cia/sql-analyst`)
- **Key features:** natural-language question processing, SQL generation and execution, local LLM integration, API-based interaction, documented testing and limitations.

### CIA Auto EDA (Week 7)

An automated EDA pipeline that profiles a sales dataset and produces shareable reports.

- **Input:** 9,800 rows × 18 columns
- **Output:** two HTML reports (ydata-profiling and SweetViz)
- **Key features:** automation script, validation script, report snapshots, requirements file and documentation.

### Pandas vs Polars vs DuckDB Benchmark (Week 5)

A performance comparison of five analytical operations on a 100,000-row sales dataset, with results validated across all three libraries.

## 📂 Repository Structure

```
cynaris-internship-Harsh/
│
├── project 1 Stakeholder brief + data inven…/
│
├── sql week-1-day-1 complete/
├── sql week-1-day-3complete/
├── sql week-1-day-4complete/
├── sql week-1-day-5complete/
│
├── week-2-day-1-visualisation/
├── week-2-day-4-data-cleaning/
├── week-2-day-5-numpy/
├── week-2-day-6-data-governance/
│
├── week-3 – day 2-dax-Basics/
├── week-3-day-1-powerbi/
├── week-3-day-3-excel-analysis/
├── week-3-day-4-looker-studio/
├── week-3-day-5-kpi-design/
│
├── week-4-day-1-statistics/
├── week-4-day-2-probability/
├── week-4-day-3-regression/
├── week-4-day-4-hypothesis-testing/
├── week-4-day-5-capstone/
│
├── week-5-day-1-pandasai/
├── week-5-day-2-autoviz-sweetviz/
├── week-5-day-3-duckdb/
├── week-5-day-4-polars/
├── week-5-day-5-ai-eda/
│
├── week-6-day-1-vanna/
├── week-6-day-2-vanna-training/
├── week-6-day-3-superset/
├── week-6-day-4-executive-reporting/
├── week-6-day-5-nl-sql-dashboard/
│
├── week-7-day-1-pandasai/
├── week-7-day-2-auto-eda/
│   ├── data/sales.csv
│   ├── docs/
│   │   ├── profile_snapshot.png
│   │   └── sweetviz_snapshot.png
│   ├── reports/
│   │   ├── profile_report.html
│   │   └── sweetviz_report.html
│   ├── scripts/
│   │   ├── run_eda.py
│   │   └── validate_reports.py
│   ├── requirements.txt
│   └── README.md
│
├── .gitignore
└── README.md
```

## 📈 What I Learned

- Working with structured and relational data.
- Writing SQL queries for analytical problems.
- Cleaning, transforming and exploring datasets.
- Performing statistical analysis and regression.
- Building dashboards and analytical reports in Power BI, Looker Studio and Superset.
- Using Python libraries for data processing and comparing their performance.
- Connecting language models with databases through Vanna and FastAPI.
- Automating EDA and validating generated outputs.
- Maintaining professional project documentation with Git and GitHub.

## 🚀 Future Learning Goals

- Advanced Python and SQL.
- Machine Learning and Deep Learning.
- AI Engineering and Large Language Models (LLMs).
- Retrieval-Augmented Generation (RAG).
- AI Agents and agentic workflows.
- Production-ready AI applications.

## 👨‍💻 About Me

**Harsh Sanchaniya**
MSc Data Science Student | Data Analytics Intern | Aspiring AI Engineer

- GitHub: [@harsh0416-P](https://github.com/harsh0416-P)
- LinkedIn: [Harsh Sanchaniya](https://www.linkedin.com/in/harsh-sanchaniya-10310b3a2/)

## ⭐ Final Note

This repository represents my continuous learning, practical experimentation and professional development throughout my internship at Cynaris Solutions.

**Learn → Build → Analyze → Improve → Repeat.**
