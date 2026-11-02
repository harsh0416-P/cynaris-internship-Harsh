@'
# W6D3 - Apache Superset Dashboard

## Project
Cynaris Sales Analytics Dashboard

## Charts
1. Revenue by City - Bar Chart
2. Revenue by Sale ID - Line Chart
3. Revenue by Category - Pie Chart
4. Total Revenue - Big Number
5. Sales Details - Table

## Technology
- Apache Superset
- Docker Desktop
- SQLite
- SQLAlchemy

## Database
Source: W6D1 sales.db

## Dashboard Evidence
See the exported dashboard JPG in this folder.

## Setup
1. Start Docker Desktop.
2. Run docker compose up -d.
3. Open http://localhost:8088.
4. Log in with your local Superset admin account.

## Review
See feedback.md.

## Security
This configuration is for local learning only.
Do not expose the Superset instance publicly.
'@ | Set-Content README.md