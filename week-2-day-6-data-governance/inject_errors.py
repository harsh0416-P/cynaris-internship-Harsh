
import pandas as pd

df = pd.read_csv("sales.csv")

# Inject three deliberate data quality errors
df.loc[0, "customer_id"] = None       # Missing required value
df.loc[1, "order_id"] = 101           # Duplicate order ID
df.loc[2, "age"] = 150                # Invalid age

df.to_csv("sales_with_errors.csv", index=False)

print("Three errors injected successfully.")
print(df.head(3))
