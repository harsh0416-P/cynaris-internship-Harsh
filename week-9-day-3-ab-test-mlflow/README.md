# W9D3 - A/B Test Tracking with MLflow

## Objective
Compare two experiment groups (A and B) and track their metrics using MLflow.

## Dataset
Indian Business Sales dataset.

## Tools Used
- Python
- Pandas
- NumPy
- SciPy
- MLflow

## Experiment Design
- Group A: Control group
- Group B: Variant group
- Conversion outcomes: Simulated for demonstration
- Statistical test: Chi-square test

## Results

| Metric | Group A | Group B |
|---|---:|---:|
| Visitors | 49,937 | 50,063 |
| Conversions | 4,885 | 6,693 |
| Conversion Rate | 9.78% | 13.37% |

P-value: 3.2122e-70

## Conclusion
Group B achieved a higher simulated conversion rate than Group A.
The chi-square test indicated a statistically significant difference
under the simulation assumptions.

## Important Limitation
Conversion outcomes were simulated using random probabilities.
They do not represent actual customer experiments or observed
customer purchasing behaviour.

## MLflow Tracking
Experiment: W9D3_AB_Test_Tracking
Run: checkout_ab_test

Logged metrics:
- conversion_rate_A
- conversion_rate_B
- p_value
- chi_square

## Run
python ab_test_mlflow.py
