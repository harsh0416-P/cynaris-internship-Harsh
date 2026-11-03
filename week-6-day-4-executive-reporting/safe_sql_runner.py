import sqlite3
import pandas as pd

from vanna.integrations.sqlite import SqliteRunner
from sql_validator import validate_sql


class SafeSqliteRunner(SqliteRunner):

    async def run_sql(self, args, context) -> pd.DataFrame:
        # Validate before database execution
        is_valid, message = validate_sql(args.sql)

        if not is_valid:
            raise ValueError(f"SQL rejected: {message}")

        # Open SQLite in read-only mode
        database_uri = f"file:{self.database_path}?mode=ro"

        conn = sqlite3.connect(database_uri, uri=True)
        conn.row_factory = sqlite3.Row

        try:
            cursor = conn.cursor()

            # Enforce read-only execution at database level
            cursor.execute("PRAGMA query_only = ON")

            cursor.execute(args.sql)

            if cursor.description is None:
                raise ValueError("Only read-only SELECT queries are permitted")

            rows = cursor.fetchall()

            if not rows:
                return pd.DataFrame()

            return pd.DataFrame([dict(row) for row in rows])

        finally:
            conn.close()