
import sqlite3

conn = sqlite3.connect("data/sales.db")

tables = conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
).fetchall()

print("Tables:", tables)

count = conn.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0]

print("Sales records:", count)

conn.close()
