import sqlite3
import json
from pathlib import Path

# Load data from SQLite
db_path = Path("../week-6-day-5-nl-sql-dashboard/data/sales.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT city, SUM(amount)
    FROM sales
    GROUP BY city
""")

rows = cursor.fetchall()
conn.close()

cities = [row[0] for row in rows]
amounts = [row[1] for row in rows]

# Prepare ECharts HTML
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>W7D3 - ECharts Sales Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
</head>
<body>
    <h2>Indian Business Sales Dashboard</h2>

    <div id="chart" style="width: 900px; height: 500px;"></div>

    <script>
        const chart = echarts.init(document.getElementById('chart'));

        const option = {{
            title: {{
                text: 'Total Sales by City'
            }},
            tooltip: {{}},
            xAxis: {{
                type: 'category',
                data: {json.dumps(cities)}
            }},
            yAxis: {{
                type: 'value',
                name: 'Sales Amount (₹)'
            }},
            series: [{{
                name: 'Sales',
                type: 'bar',
                data: {json.dumps(amounts)},
                label: {{
                    show: true,
                    position: 'top'
                }}
            }}]
        }};

        chart.setOption(option);

        window.addEventListener('resize', () => chart.resize());
    </script>
</body>
</html>
"""

output = Path("charts/echarts_sales_by_city.html")
output.parent.mkdir(exist_ok=True)
output.write_text(html, encoding="utf-8")

print("ECharts HTML generated:", output.resolve())