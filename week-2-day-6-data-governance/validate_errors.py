
import pandas as pd

df = pd.read_csv("sales_with_errors.csv")

checks = [
    ("Missing customer ID", df["customer_id"].notna().all()),
    ("Unique order IDs", df["order_id"].is_unique),
    ("Age between 18 and 100", df["age"].between(18, 100).all()),
]

results = pd.DataFrame(checks, columns=["Check", "Passed"])
results["Status"] = results["Passed"].map(
    {True: "PASS", False: "FAIL"}
)

print(results.to_string(index=False))

# Save an HTML report
html = results.to_html(index=False)
with open("error_validation_report.html", "w", encoding="utf-8") as f:
    f.write(
        "<html><head><title>Data Quality Report</title></head>"
        "<body><h1>Sales Data Quality Validation</h1>"
        + html
        + "</body></html>"
    )

print("\nReport saved: error_validation_report.html")
print("All three errors detected:", (~results["Passed"]).sum() == 3)
