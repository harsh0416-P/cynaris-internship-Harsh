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
- Build meaningful data visualizations and reports.
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
| AI & LLM | Vanna, PandasAI, Ollama |
| API Development | FastAPI |
| Data Quality | Great Expectations |
| BI & Reporting | Excel, Looker Studio |
| Development Tools | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |

## 📊 Internship at a Glance

| Week | Focus | Main Tools |
|---|---|---|
| 1 | SQL Fundamentals | SQL, CSV exports |
| 2 | Python for Data Analytics | Pandas, NumPy, Matplotlib, Seaborn, Great Expectations |
| 3 | Business Intelligence & Reporting | Excel, Looker Studio |
| 4 | Statistics & Predictive Analytics | Python, regression analysis |
| 5 | Advanced Data Analytics & AI Tools | PandasAI, AutoViz, SweetViz, DuckDB, Polars |
| 6 | AI-Powered Analytics | Vanna, Ollama, SQLite, FastAPI |
| 7 | Automated EDA | ydata-profiling, SweetViz |

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

**Topics:** Pandas fundamentals · data cleaning and missing values · data visualization · data governance · data quality and validation

**Practical work:**
- Explored and manipulated datasets with Pandas and NumPy.
- Created charts using Matplotlib and Seaborn.
- Handled missing values and compared data quality.
- Implemented data quality checks and explored Great Expectations.
- Generated validation reports and data quality scorecards.

### Week 3 — Business Intelligence & Reporting

**Focus:** Turning data into business insights.

**Topics:** Excel-based analysis · data visualization and reporting · Looker Studio · KPI design

**Practical work:**
- Analysed data in Excel.
- Created visual reports.
- Explored business performance metrics.
- Designed KPI-focused analytical outputs.

<!-- Verify: your internship brief also mentions a Power BI sales dashboard for Week 3. If you built one, add it here. -->

### Week 4 — Statistics & Predictive Analytics

**Focus:** Applying statistical methods to understand data and relationships.

**Topics:** Descriptive statistics · probability · regression analysis · hypothesis testing · statistical interpretation

**Practical work:**
- Performed descriptive statistical analysis.
- Explored probability concepts.
- Built regression analysis workflows.
- Practised hypothesis testing.
- Completed a statistical capstone project on a sales dataset.

### Week 5 — Advanced Data Analytics & AI Tools

**Focus:** Modern analytical tools and AI-assisted workflows.

**Topics:** PandasAI · AutoViz and SweetViz · DuckDB · Polars · AI-powered EDA

**Practical work:**
- Automated exploratory data analysis and generated visual reports.
- Queried analytical datasets using DuckDB.
- **Performance comparison:** benchmarked five analytical operations across Pandas, Polars and DuckDB on a 100,000-row sales dataset and validated that the results matched.
- Explored AI-assisted data analysis and documented findings.

### Week 6 — AI-Powered Analytics with Vanna

**Focus:** Building AI-powered Natural Language to SQL applications.

**Practical work:**
- Configured Vanna 2.0.2 with Ollama and the Llama 3.2:1b local language model.
- Created a SQLite sales database and integrated Vanna with FastAPI.
- Developed the `POST /cia/sql-analyst` endpoint.
- Ran natural-language questions against the database, verified database operations and exported query results.
- Explored custom question-to-SQL training and documented testing results and model limitations.

### Week 7 — Automated EDA (CIA Auto EDA)

**Focus:** Automating exploratory data analysis and validating the outputs.

**Practical work:**
- Used **ydata-profiling** and **SweetViz** on a **9,800-row, 18-column** sales dataset.
- Generated **two HTML reports**.
- Created automation scripts and validation scripts.
- Documented the outputs.

## 💻 Featured Projects

### Vanna SQL Analyst (Week 6)

A local AI-powered SQL assistant that lets users ask questions about sales data in natural language.

**Architecture:**
- LLM: Ollama, Llama 3.2:1b
- NL-to-SQL framework: Vanna 2.0.2
- Database: SQLite
- API: FastAPI (`POST /cia/sql-analyst`)

**Key features:** natural-language question processing, SQL generation and database execution, local LLM integration, API-based interaction, documented testing and limitations.

**Location:** `week-6-day-1-vanna/`

### CIA Auto EDA (Week 7)

An automated EDA pipeline that profiles a sales dataset and produces shareable reports.

**Inputs and outputs:** 9,800 rows × 18 columns in, two HTML reports out (ydata-profiling and SweetViz).

**Key features:** automation scripts, validation scripts, documented outputs.

### Pandas vs Polars vs DuckDB Benchmark (Week 5)

A performance comparison of five analytical operations on a 100,000-row sales dataset, with results validated across all three libraries.

## 📂 Repository Structure

```
cynaris-internship-Harsh/
│
├── week-1-day-1-sql-fundamentals/
├── week-1-day-2-sql-joins/
├── week-1-day-3-sql-aggregations/
├── week-1-day-4-sql-subqueries/
├── week-1-day-5-python-pandas/
│
├── week-2-day-1-visualisation/
├── week-2-day-6-data-governance/
│
├── week-3-day-1/
├── week-3-day-2/
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
│
└── README.md
```

> The directory names above represent the learning areas. The actual repository contains the implementation folders and files for completed work, including Week 7.

## 📈 What I Learned

- Working with structured and relational data.
- Writing SQL queries for analytical problems.
- Cleaning, transforming and exploring datasets.
- Performing statistical analysis and regression.
- Building visualizations and analytical reports.
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

I aim to combine my Data Science foundation with practical AI Engineering skills.

## 👨‍💻 About Me

**Harsh Sanchaniya**
MSc Data Science Student | Data Analytics Intern | Aspiring AI Engineer

- GitHub: [@harsh0416-P](https://github.com/harsh0416-P)
- LinkedIn: [Harsh Sanchaniya](https://www.linkedin.com/in/harsh-sanchaniya-10310b3a2/)

## ⭐ Final Note

This repository represents my continuous learning, practical experimentation and professional development throughout my internship at Cynaris Solutions.

Every folder reflects a learning milestone, every project represents a practical challenge, and every commit documents my progress.

**Learn → Build → Analyze → Improve → Repeat.**
