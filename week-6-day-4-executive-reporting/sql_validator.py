import re


def validate_sql(sql: str) -> tuple[bool, str]:
    if not sql or not sql.strip():
        return False, "SQL query cannot be empty"

    query = sql.strip()

    # Allow only one SQL statement
    if ";" in query.rstrip(";"):
        return False, "Multiple SQL statements are not allowed"

    # Only SELECT or WITH queries are accepted
    if not re.match(r"^(SELECT|WITH)\b", query, re.IGNORECASE):
        return False, "Only SELECT queries are allowed"

    # Block potentially destructive SQL operations
    forbidden = re.compile(
        r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|"
        r"ATTACH|DETACH|PRAGMA|VACUUM|REINDEX|TRIGGER)\b",
        re.IGNORECASE
    )

    if forbidden.search(query):
        return False, "Unsafe SQL operation detected"

    return True, "SQL query passed basic validation"