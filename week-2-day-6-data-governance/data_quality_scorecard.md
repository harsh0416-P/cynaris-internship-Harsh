# Data Quality Scorecard — Sales Orders

## Dataset Overview
- Dataset: sales.csv
- Records: 10
- Columns: 6
- Consumer: BI dashboard

## DAMA Data Quality Assessment

| Dimension | Assessment | Recommendation |
|---|---|---|
| Completeness | Tested required IDs and emails for missing values | Reject records with missing required fields |
| Accuracy | Tested age range 18–100 and non-negative amounts | Investigate invalid values |
| Consistency | Basic date validity checked; cross-table consistency not tested | Add cross-table and date relationship checks |
| Timeliness | SLA set to 2 hours; actual arrival time not measured | Record ingestion timestamps |
| Uniqueness | Duplicate order IDs tested | Enforce unique order IDs |
| Validity | Email format and age range tested | Validate all fields against schema rules |

## Intentional Error Test
Three errors were introduced into sales_with_errors.csv:
1. Missing customer_id
2. Duplicate order_id
3. Age value of 150

These errors should fail their corresponding validation checks.

## PII Classification
- customer_email: Confidential PII; mask before dashboard display.
- customer_id: Internal identifier; restrict access where appropriate.

## Improvement Recommendations
1. Run automated validation before dashboard refresh.
2. Alert the data owner when checks fail.
3. Mask customer emails in reporting outputs.
4. Measure freshness using actual ingestion timestamps.
5. Retain validation results for audit purposes.

Note: Confirm the final results from gx_validation.py before claiming all tests passed.
