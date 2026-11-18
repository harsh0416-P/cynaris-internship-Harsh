# W9D4 — MLflow Dashboard: Compare Model Versions

## Objective
Compare two registered machine learning model versions using MLflow and evaluate their predictive performance.

## Dataset
Indian Business Sales Dataset

- Total records: 100,000
- Training records: 80,000
- Testing records: 20,000

## Models
- Version 1: Existing Random Forest model from W9D2.
- Version 2: Newly trained Random Forest model with 200 estimators.

## Evaluation Results

| Metric | Version 1 | Version 2 |
|---|---:|---:|
| MAE | 12450.864325 | 12450.627446 |
| RMSE | 14382.773695 | 14382.616910 |
| R² | 0.001511 | 0.001533 |

## MLflow Registry
Registered model: `CynarisSalesAmountModel`

- Version 1: Existing model
- Version 2: Newly registered model

Experiment: `W9D4_Model_Version_Comparison`

## Conclusion
Version 2 achieved marginally lower MAE and RMSE and a slightly higher R² than Version 1. However, both models have R² values close to zero, indicating weak predictive performance. Further feature engineering and model experimentation are required before production use.

## Technologies
- Python
- Pandas
- NumPy
- Scikit-learn
- MLflow
- SQLite

## Run
`python compare_models.py`

## Limitation
The model comparison uses the same train/test split, but the current features provide limited predictive power for the sales amount target.