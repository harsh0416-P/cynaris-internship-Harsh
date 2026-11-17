
# W9D2 - MLflow Model Registry for Analyst Models

## Objective
Train, evaluate, register and load a business sales prediction model using MLflow.

## Dataset
Business Sales Dataset

Features:
- City
- Category
- Product
- Quantity

Target:
- Amount

## Model
Random Forest Regressor

## Evaluation Metrics
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R-squared (R2)

## MLflow Registry
Registered Model: CynarisSalesAmountModel
Version: 1

## Testing
Loaded the registered model using MLflow PyFunc and generated predictions for three sample records.

## Output Files
- reports/model_evaluation.txt
- reports/registration_details.txt
- reports/model_predictions.csv

## Technologies
Python, Pandas, NumPy, Scikit-learn, MLflow
