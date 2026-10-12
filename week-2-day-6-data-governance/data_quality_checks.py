
import pandas as pd
import great_expectations as gx

from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.validator.validator import Validator
from great_expectations.execution_engine import PandasExecutionEngine
from great_expectations.core.batch import Batch

df = pd.read_csv("sales.csv")

# Set up a Great Expectations pandas execution engine
engine = PandasExecutionEngine()
batch = Batch(data=df)

validator = Validator(
    execution_engine=engine,
    batches=[batch],
    data_context=gx.get_context(),
)

# Define 8 Great Expectations checks
checks = [
    validator.expect_column_values_to_not_be_null("order_id"),
    validator.expect_column_values_to_be_unique("order_id"),
    validator.expect_column_values_to_not_be_null("customer_id"),
    validator.expect_column_values_to_not_be_null("customer_email"),
    validator.expect_column_values_to_match_regex(
        "customer_email", r"^[\w.-]+@[\w.-]+\.\w+$"
    ),
    validator.expect_column_values_to_be_between(
        "age", min_value=18, max_value=100
    ),
    validator.expect_column_values_to_be_between(
        "amount", min_value=0
    ),
    validator.expect_column_values_to_not_be_null("order_date"),
]

results = []

for i, result in enumerate(checks, start=1):
    results.append({
        "check": i,
        "expectation": result.expectation_config.type,
        "success": result.success,
    })

report = pd.DataFrame(results)
print(report.to_string(index=False))
print("\nOverall success:", report["success"].all())

report.to_html("validation_report.html", index=False)
print("\nReport saved: validation_report.html")
