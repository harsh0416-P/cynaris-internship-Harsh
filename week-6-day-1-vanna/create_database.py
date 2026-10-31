
import sqlite3

conn = sqlite3.connect("data/sales.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    product TEXT,
    category TEXT,
    amount REAL,
    city TEXT,
    quantity INTEGER
)
""")

sales = [
    ("Rahul", "Laptop", "Electronics", 55000, "Bengaluru", 2),
    ("Priya", "Mobile", "Electronics", 25000, "Mumbai", 3),
    ("Amit", "Chair", "Furniture", 8000, "Delhi", 5),
    ("Neha", "Table", "Furniture", 12000, "Bengaluru", 2),
    ("Karan", "Laptop", "Electronics", 60000, "Mumbai", 1),
    ("Sneha", "Mobile", "Electronics", 22000, "Delhi", 4),
    ("Arjun", "Desk", "Furniture", 15000, "Chennai", 3),
    ("Riya", "Laptop", "Electronics", 58000, "Chennai", 2),
    ("Vikram", "Chair", "Furniture", 7500, "Mumbai", 6),
    ("Ananya", "Mobile", "Electronics", 27000, "Bengaluru", 2)
]

conn.executemany("""
INSERT INTO sales
(customer_name, product, category, amount, city, quantity)
VALUES (?, ?, ?, ?, ?, ?)
""", sales)

conn.commit()

print("Records inserted:", conn.execute(
    "SELECT COUNT(*) FROM sales"
).fetchone()[0])

conn.close()
