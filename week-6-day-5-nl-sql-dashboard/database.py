import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "sales.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def check_database():
    with get_connection() as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()

        count = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

    print("Tables:", [table["name"] for table in tables])
    print("Sales records:", count)


if __name__ == "__main__":
    check_database()