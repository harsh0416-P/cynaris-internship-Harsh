
import pandas as pd
import great_expectations as gx

# Load the dataset containing three intentional errors
df = pd.read_csv("sales_with_errors.csv")

# Create an ephemeral Great Expectations context
context = gx.get_context(mode="ephemeral")

# Configure the pandas data source
data_source = context.data_sources.add_pandas(
    name="sales_source"
)

asset = data_source.add_dataframe_asset(
    name="sales_asset"
)

batch_definition = asset.add_batch_definition_whole_dataframe(
    "sales_batch"
)

# Define eight data quality expectations
suite = gx.ExpectationSuite(
    name="sales_quality_suite"
)

expectations = [
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="order_id"
    ),
    gx.expectations.ExpectColumnValuesToBeUnique(
        column="order_id"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="customer_id"
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="customer_email"
    ),
    gx.expectations.ExpectColumnValuesToMatchRegex(
        column="customer_email",
        regex=r"^[\w.-]+@[\w.-]+\.\w+$",
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="age",
        min_value=18,
        max_value=100,
    ),
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="amount",
        min_value=0,
    ),
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="order_date"
    ),
]

for expectation in expectations:
    suite.add_expectation(expectation)

context.suites.add(suite)

# Register the validation
validation_definition = gx.ValidationDefinition(
    name="sales_validation",
    data=batch_definition,
    suite=suite,
)

context.validation_definitions.add(
    validation_definition
)

# Run validation using the required "dataframe" parameter
result = validation_definition.run(
    batch_parameters={"dataframe": df}
)

# Display results
print("\nGREAT EXPECTATIONS VALIDATION")
print("=" * 45)

rows = []

for item in result.results:
    name = item.expectation_config.type
    passed = item.success

    rows.append({
        "Expectation": name,
        "Status": "PASS" if passed else "FAIL",
        "Success": passed,
    })

    print(f"{name}: {'PASS' if passed else 'FAIL'}")

report = pd.DataFrame(rows)

print("\nOverall validation success:", result.success)
print("Passed:", int(report["Success"].sum()))
print("Failed:", int((~report["Success"]).sum()))

# Generate an HTML summary from actual GX results
html = report.to_html(index=False)

with open(
    "validation_report.html",
    "w",
    encoding="utf-8"
) as file:
    file.write(
        "<!DOCTYPE html><html><head>"
        "<title>Great Expectations Validation Report</title>"
        "</head><body>"
        "<h1>Sales Data Quality Validation</h1>"
        "<p>Dataset: sales_with_errors.csv</p>"
        + html
        + f"<p>Overall success: {result.success}</p>"
        + "</body></html>"
    )

print("\nHTML report saved: validation_report.html")
