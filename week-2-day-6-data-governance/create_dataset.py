import pandas as pd

data = {
    "order_id": range(101, 111),
    "customer_id": [f"C{i:02}" for i in range(1, 11)],
    "customer_email": [
        f"customer{i}@example.com" for i in range(1, 11)
    ],
    "age": [22, 30, 25, 40, 35, 28, 45, 32, 26, 38],
    "amount": [500, 1200, 750, 2000, 1500, 900, 3000, 650, 850, 1100],
    "order_date": [
        f"2026-10-{i:02}" for i in range(1, 11)
    ]
}

df = pd.DataFrame(data)
df.to_csv("sales.csv", index=False)
print("Dataset created successfully!")
print("Rows:", len(df))
print(df.head())
