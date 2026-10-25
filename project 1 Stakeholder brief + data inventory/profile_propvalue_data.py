
from pathlib import Path
import pandas as pd

# Folder containing the two CSV files
DATA_DIR = Path("data")

FILES = [
    "da_customer_profiles.csv",
    "da_product_catalogue.csv",
]

for filename in FILES:
    path = DATA_DIR / filename

    print("\n" + "=" * 50)
    print("FILE:", filename)
    print("=" * 50)

    if not path.exists():
        print("ERROR: File not found:", path)
        continue

    df = pd.read_csv(path)

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

print("\nData inspection completed!")
