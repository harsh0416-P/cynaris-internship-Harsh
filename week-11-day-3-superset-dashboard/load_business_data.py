from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "indian_business_data.csv"

if not CSV_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

if df.empty:
    raise ValueError("The CSV contains no data rows.")

if df.columns.duplicated().any():
    raise ValueError("The CSV contains duplicate column names.")

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="business_user",
    password="business_local_2026",
    host="localhost",
    port=5433,
    database="business_analytics",
)

engine = create_engine(connection_url)

with engine.begin() as connection:
    df.to_sql(
        name="indian_business_data",
        con=connection,
        if_exists="replace",
        index=False,
    )

    row_count = connection.execute(
        text("SELECT COUNT(*) FROM indian_business_data")
    ).scalar_one()

print("DATA LOAD SUCCESSFUL")
print("Rows:", row_count)
print("Columns:", df.columns.tolist())
print("Table: public.indian_business_data")