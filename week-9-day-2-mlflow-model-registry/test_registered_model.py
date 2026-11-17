
import mlflow
import pandas as pd
import os

# 1. Registered model details
MODEL_NAME = "CynarisSalesAmountModel"

# 2. Load registered model
model_uri = f"models:/{MODEL_NAME}/1"

print("Loading registered model...")

model = mlflow.pyfunc.load_model(model_uri)

# 3. Prepare sample business data
sample_data = pd.DataFrame({
    "city": ["Bengaluru", "Mumbai", "Delhi"],
    "category": ["Electronics", "Electronics", "Furniture"],
    "product": ["Laptop", "Mobile", "Chair"],
    "quantity": [2, 3, 5]
})

# 4. Generate predictions
predictions = model.predict(sample_data)

# 5. Display results
results = sample_data.copy()
results["predicted_amount"] = predictions

print("\nMODEL PREDICTION RESULTS")
print("=" * 45)
print(results.to_string(index=False))

# 6. Save prediction report
os.makedirs("reports", exist_ok=True)

results.to_csv(
    "reports/model_predictions.csv",
    index=False
)

print("\nPrediction test completed!")
print("Report saved: reports/model_predictions.csv")
