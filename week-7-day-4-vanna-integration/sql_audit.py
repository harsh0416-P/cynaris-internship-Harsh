
import json
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd


class AuditedSqlRunner:

    def __init__(self, database_path):
        self.database_path = Path(database_path).resolve()
        self.log_file = Path(__file__).resolve().parent / "sql_audit.jsonl"

    async def run_sql(self, args, context):

        sql = args.sql.strip()

        entry = {
            "timestamp": datetime.now().isoformat(),
            "sql": sql,
            "status": "executing"
        }

        try:
            # Open SQLite in genuine read-only mode.
            uri = f"{self.database_path.as_uri()}?mode=ro"

            with sqlite3.connect(uri, uri=True) as connection:
                connection.execute("PRAGMA query_only = ON")

                result = pd.read_sql_query(sql, connection)

            entry["status"] = "success"
            entry["row_count"] = len(result)

            return result

        except Exception as error:
            entry["status"] = "failed"
            entry["error"] = str(error)
            raise

        finally:
            with self.log_file.open("a", encoding="utf-8") as file:
                file.write(json.dumps(entry) + "\n")
