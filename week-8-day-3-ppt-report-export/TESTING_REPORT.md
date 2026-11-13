# W8D3 - PPT Report Export Testing Report

## 1. Project Overview

**Project:** Superstore Business Report Generator  
**Task:** Week 8 - Day 3: PPT Report Export  
**Dataset:** Superstore Sales Dataset  
**Output:** superstore_business_report.pptx

## 2. Testing Environment

- Python
- Pandas
- python-pptx
- Groq API
- PowerPoint

## 3. Test Cases and Results

| Test ID | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC01 | Load Superstore CSV | Dataset loads successfully | Dataset loaded | PASS |
| TC02 | Calculate sales insights | Sales metrics are calculated | Total sales: $2,261,536.78 | PASS |
| TC03 | Generate AI summary | Groq returns an executive summary | Summary generated successfully | PASS |
| TC04 | Export PowerPoint | PPTX file is created | File created successfully | PASS |
| TC05 | Validate slide count | Presentation contains 8 slides | 8 slides found | PASS |
| TC06 | Validate charts | Presentation contains 5 charts | 5 charts found | PASS |
| TC07 | Validate slide titles | All expected slides are present | 8 slide titles found | PASS |
| TC08 | Open presentation | Presentation opens in PowerPoint | Opened successfully | PASS |

## 4. PowerPoint Slide Structure

1. Title Slide
2. AI-Generated Executive Summary
3. Sales by Category
4. Sales by Region
5. Sales by Customer Segment
6. Sales by Shipping Mode
7. Yearly Sales
8. Business Recommendations

## 5. Key Results

- Total sales: $2,261,536.78
- Total slides: 8
- Charts generated: 5
- AI executive summary: Generated using Groq
- PowerPoint export: Successful

## 6. Known Limitations

- The report uses a predefined dataset path.
- The presentation is generated as a PPTX file rather than through a CSV upload interface.
- Profitability cannot be evaluated using sales figures alone.
- Visual formatting can be improved further for readability.

## 7. Final Status

**Result:** Core PowerPoint generation and validation tests passed.

**Output File:** superstore_business_report.pptx
