
# Week 6 - Deep-Dive Analysis Methodology

## Objective
Analyze Bengaluru property sale listings, compare micro-markets,
and evaluate regression models for predicting price per square foot.

## Dataset
Source: Cynaris PropTech real estate listings dataset.
The analysis uses valid Bengaluru sale listings.

## Segmentation
Properties are grouped by locality.
Average and median price per square foot, listing count,
average area, property age, and days on market are calculated.

## Prediction Target
price_per_sqft

## Features
- area_sqft
- age_years
- floor
- parking
- locality

## Models
- Median Dummy Regressor
- Linear Regression
- Ridge Regression
- Random Forest Regressor

## Validation
Five-fold cross-validation with shuffled folds and random_state=42.

## Evaluation Metrics
- MAE
- RMSE
- MAPE

## Assumptions and Limitations
- Only Bengaluru sale listings are included.
- Price per square foot is used as the prediction target.
- Missing numeric feature values are imputed using the median.
- Missing locality values are imputed using the most frequent category.
- The dataset contains a limited number of Bengaluru sale listings.
- Cross-validation results are preliminary and may vary with new data.
- The 18% MAPE target is an acceptance criterion, not an assumed result.
- Locality codes are used as supplied; no geographic coordinates are inferred.
