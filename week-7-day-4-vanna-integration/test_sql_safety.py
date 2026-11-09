import asyncio
from types import SimpleNamespace
from sql_audit import AuditedSqlRunner


async def main():
    runner = AuditedSqlRunner(
        "../week-6-day-5-nl-sql-dashboard/data/sales.db"
    )

    context = SimpleNamespace()

    # Test a permitted SELECT.
    select_args = SimpleNamespace(
        sql="SELECT COUNT(*) AS total FROM sales"
    )

    result = await runner.run_sql(select_args, context)
    print("SELECT result:", result.to_dict("records"))

    # Test a blocked DELETE.
    delete_args = SimpleNamespace(
        sql="DELETE FROM sales"
    )

    try:
        await runner.run_sql(delete_args, context)
        print("FAIL: DELETE was allowed")
    except Exception as error:
        print("PASS: DELETE blocked:", error)


asyncio.run(main())