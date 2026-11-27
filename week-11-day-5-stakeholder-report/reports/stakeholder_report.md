\# Indian Business Dataset — Stakeholder Report



\## 1. Executive Summary



This report analyzes 600 Indian property listings across 8 cities using 15 variables. The analysis examines listing distribution, property pricing, transaction types, market duration, and the sold flag.



The dataset contains no missing values or duplicate listing IDs. The analysis period ranges from January 2, 2023, to December 30, 2024.



\## 2. Five Key Business Insights



\### Insight 1: Chennai has the highest listing volume



\- Chennai: 93 listings (15.50%).

\- Pune: 79 listings (13.17%).

\- Kolkata: 67 listings (11.17%), the lowest among the eight cities.



\*\*Business implication:\*\* Chennai represents the largest share of listings in this dataset. Businesses can examine its property mix and listing characteristics before allocating local marketing resources.



!\[Listings by City](../outputs/charts/01\_listings\_by\_city.png)



\### Insight 2: Villas have the highest median property price



\- Villas: ₹506.43 lakh median price.

\- 4BHK: ₹341.11 lakh.

\- Plots: ₹72.57 lakh, the lowest median price.



\*\*Business implication:\*\* Property type is an important pricing segment. Pricing strategies should distinguish premium villa listings from lower-priced property categories.



!\[Median Price by Type](../outputs/charts/02\_median\_price\_by\_type.png)



\### Insight 3: Sale listings dominate the dataset



\- Sale: 463 listings (77.17%).

\- Rent: 137 listings (22.83%).

\- Median days on market: Sale 184 days; Rent 187 days.



\*\*Business implication:\*\* Sale listings form the larger part of this dataset. However, the median time on market is similar for both transaction types, so transaction type alone does not explain listing duration.



!\[Transaction Distribution](../outputs/charts/03\_transaction\_distribution.png)



\### Insight 4: Commercial properties have the longest median market duration



\- Commercial: 200.5 days.

\- 3BHK: 194 days.

\- 1BHK: 194 days.

\- 2BHK: 169 days, the shortest median duration.



\*\*Business implication:\*\* Commercial listings may need closer review of pricing, presentation, and target customer segments to understand their longer market duration.



!\[Market Duration](../outputs/charts/04\_market\_duration\_by\_type.png)



\### Insight 5: The sold flag varies across cities



\- Overall, 209 listings (34.83%) have `sold = 1`.

\- Pune has the highest `sold = 1` share at 43.04%.

\- Chennai has the lowest `sold = 1` share at 25.81%.



\*\*Business implication:\*\* The variation across cities deserves further investigation. Compare property mix, pricing, and listing duration before deciding what explains the difference.



\*\*Data limitation:\*\* The dataset does not include a definition of the `sold` field. Therefore, these figures are reported as sold-flag values, not confirmed sales conversion rates.



!\[Sold Flag Distribution](../outputs/charts/05\_sold\_flag\_distribution.png)



\## 3. Additional Observation: Monthly Listings



Monthly listing counts vary during the analysis period. January 2023 recorded 29 listings, while December 2024 recorded 17.



This dataset alone does not establish seasonality or explain the reasons for monthly changes.



!\[Monthly Listing Trend](../outputs/charts/06\_monthly\_listing\_trend.png)



\## 4. Recommendations



1\. Investigate Chennai's listing mix to understand its higher listing volume.

2\. Develop separate pricing benchmarks for villas, apartments, commercial properties, and plots.

3\. Review commercial listings with long market durations to identify pricing or positioning issues.

4\. Compare Sale and Rent listings by city and property type to investigate market-duration differences.

5\. Confirm the definition of the `sold` field before using it for sales performance or conversion reporting.



\## 5. Limitations



\- The analysis covers 600 records, not necessarily the entire Indian property market.

\- The dataset does not provide a documented definition of the `sold` flag.

\- Descriptive comparisons do not establish causation.

\- Further analysis is needed to evaluate demand, profitability, and actual sales conversion.



\## 6. Conclusion



The analysis identifies differences in listing volume, property pricing, and market duration across the dataset. These findings provide a starting point for stakeholder discussions and further investigation.

