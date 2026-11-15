# Exploratory Data Analysis Report

## 1. Project Overview

**Project:** Indian Real Estate Market Analysis  
**Dataset:** `da_realestate_listings.csv`  
**Tools:** Python, Pandas, NumPy, Matplotlib, Seaborn

The objective is to analyze property listings across Indian cities and identify pricing patterns, property trends and potential data-quality issues.

## 2. Dataset Overview

| Metric | Result |
|---|---:|
| Total records | 600 |
| Total columns | 15 |
| Cities | 8 |
| Missing values | 0 |
| Duplicate records | 0 |

## 3. Data Quality Assessment

- No missing values were detected.
- No duplicate records were detected.
- Numerical and categorical variables were examined.
- Potential pricing inconsistencies were identified.

## 4. Exploratory Findings

- Chennai had the highest listing count with 93 records.
- Kolkata had the lowest listing count with 67 records.
- Average price per square foot was ₹10,444.07.
- Median price per square foot was ₹8,401.
- Average property area was 2,204.09 square feet.
- Average days on market was approximately 184 days.
- 209 listings were marked as sold.

## 5. Outlier Analysis

The IQR method was applied to `price_per_sqft`.

- Lower threshold: -₹6,758.375
- Upper threshold: ₹26,654.625
- Detected outliers: 0

No price-per-square-foot observations exceeded these thresholds.

## 6. Data Consistency Issues

The calculated property values differed from the recorded `total_price_lakh` values.

The meaning of the `sold` status for rental listings also requires clarification.

These issues should be investigated before using the dataset for financial decisions.

## 7. Business Recommendations

1. Compare property prices across cities.
2. Investigate premium property segments.
3. Monitor listings with longer market durations.
4. Use property type and locality analysis for pricing strategies.
5. Validate inconsistencies in recorded property values.
6. Clarify the sold-status definition for rental listings.

## 8. Conclusion

The analysis examined 600 property listings across eight Indian cities.

The findings provide an overview of property prices, property categories, transaction types and market durations.

Although the dataset has no missing values or duplicate records, pricing inconsistencies require further investigation.

Further validation is recommended before using these findings for financial or investment decisions.

---

**Note:** This report analyzes the available real-estate dataset. Its equivalence to the specifically assigned Indian Business Dataset has not yet been confirmed.