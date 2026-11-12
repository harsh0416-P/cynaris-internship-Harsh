# Testing Report — Business Intelligence Studio (W8D2)

## 1. Testing Overview

Testing was performed to verify dataset loading, data validation, dashboard functionality, KPI calculations, filtering, AI recommendation generation and PowerPoint export.

## 2. Test Environment

| Component | Configuration |
|---|---|
| Operating System | Windows |
| Programming Language | Python 3.13 |
| Dashboard | Streamlit |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |
| AI Integration | Groq API |
| Presentation | python-pptx |

## 3. Test Cases and Results

| Test ID | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC01 | Load customer CSV | 200 customer records loaded | 200 records loaded | PASS |
| TC02 | Validate dataset | No missing values or duplicate IDs | Validation passed | PASS |
| TC03 | Calculate total revenue | ₹4,992,621 | ₹4,992,621 | PASS |
| TC04 | Calculate total orders | 2,307 | 2,307 | PASS |
| TC05 | Calculate churn rate | 3% | 3% | PASS |
| TC06 | Remove Pune city filter | 161 customers remain | 161 customers | PASS |
| TC07 | Filter revenue | KPIs recalculate | Revenue ₹3,890,271 | PASS |
| TC08 | Generate AI recommendations | Executive summary and five recommendations | Generated successfully | PASS |
| TC09 | Generate PowerPoint | 11-slide presentation | 11 slides generated | PASS |
| TC10 | Validate presentation figures | Figures match full dataset | Main figures verified | PASS |

## 4. Dataset Validation

- Total records: 200
- Total columns: 10
- Missing values: 0
- Duplicate customer IDs: 0
- Active customers: 194
- Churned customers: 6

## 5. Dashboard KPI Validation

| Metric | Verified Value |
|---|---:|
| Total Customers | 200 |
| Total Revenue | ₹4,992,621 |
| Total Orders | 2,307 |
| Churn Rate | 3.00% |

## 6. AI Output Validation

The AI successfully generated:

- One executive summary.
- Five business recommendations.
- Findings for each recommendation.
- Recommended business actions.
- Potential benefits.

AI-generated statements were reviewed against the underlying customer data. Revenue was distinguished from profitability, and recommendations were treated as hypotheses requiring validation.

## 7. PowerPoint Validation

The exported presentation contained 11 slides:

1. Title
2. Executive Summary
3. City Performance
4. Acquisition Channel Performance
5. Age Group Performance
6. Customer Churn
7. Recommendation 1
8. Recommendation 2
9. Recommendation 3
10. Recommendation 4
11. Recommendation 5

## 8. Issues Encountered

- Missing Python dependencies in the virtual environment.
- NumPy and Pandas import errors.
- Pydantic dependency incompatibility.
- Pillow import error.
- Incorrect currency formatting in initial AI output.
- Unsupported profitability wording in an AI-generated recommendation.

These issues were addressed through dependency installation, package repair and prompt improvements.

## 9. Known Limitations

- AI output depends on external API availability.
- Recommendations are not proven business outcomes.
- Revenue figures do not represent profit.
- The dataset contains only 200 customers.
- Observational data cannot establish causal relationships.

## 10. Conclusion

The dashboard successfully loaded and analysed the customer dataset, recalculated KPIs under filtering, generated AI-based business recommendations and exported an 11-slide executive presentation.

The core W8D2 functionality was verified against the supplied customer dataset.