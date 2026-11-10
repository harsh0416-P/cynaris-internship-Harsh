# W8D1 – Testing Report

## 1. Project Overview

**Project:** Executive Summary Generation via Groq from Data Insights

**Purpose:** Validate the CSV analysis, AI summary generation, and PowerPoint export workflow.

## 2. Test Environment

- Operating System: Windows
- Language: Python 3.11
- Data Processing: Pandas
- AI Integration: Groq API
- Presentation: python-pptx

## 3. Test Cases

| Test ID | Test Description | Expected Result | Actual Result |
|---|---|---|---|
| TC01 | Load customer profiles CSV | Dataset loads successfully | Passed |
| TC02 | Validate dataset columns | Required columns are present | Passed |
| TC03 | Load incompatible product catalogue | Missing columns are detected | Passed |
| TC04 | Load nonexistent CSV path | FileNotFoundError is raised | Passed |
| TC05 | Calculate five business insights | All five insights are generated | Passed |
| TC06 | Generate executive summary through Groq | Summary is generated and saved | Passed |
| TC07 | Generate PowerPoint presentation | Seven slides are created | Passed |
| TC08 | Verify PowerPoint slide count | Exactly seven slides are present | Passed |

## 4. Dataset Validation Results

- Total records: 200
- Total columns: 10
- Missing values: 0
- Duplicate customer IDs: 0

## 5. Business Analysis Results

The pipeline calculates:

1. Revenue by city.
2. Revenue by acquisition channel.
3. Revenue by age group.
4. Customer churn percentage.
5. Average customer revenue and order metrics.

## 6. AI Integration

The application sends calculated business insights to the Groq API and receives an executive summary.

The generated summary is saved as `executive_summary.txt`.

AI-generated statements must be checked against the calculated statistics before business use.

## 7. PowerPoint Validation

The application generated `executive_summary.pptx` containing seven slides:

1. Executive title.
2. Revenue by city.
3. Revenue by acquisition channel.
4. Revenue by age group.
5. Customer churn overview.
6. Customer value and revenue.
7. Business recommendations.

## 8. Known Limitations

- No acquisition cost data is available.
- No profit margin data is available.
- Churn reasons and churn periods are unavailable.
- AI recommendations require human review.

## 9. Conclusion

The integrated W8D1 pipeline successfully loaded and validated the customer dataset, calculated five business insights, generated an executive summary using Groq, and exported a seven-slide PowerPoint presentation.
