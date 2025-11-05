import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

print("Creating synthetic oil quality data...")
np.random.seed(42)

# Generate realistic oil sensor data
data = {
    'Temperature (C)': np.random.normal(65, 8, 200).clip(50, 85),
    'Viscosity (cSt)': np.random.normal(45, 10, 200).clip(25, 70),
    'Turbidity': np.random.normal(15, 5, 200).clip(5, 30),
    'Oil_Humidity_percent': np.random.normal(25, 8, 200).clip(10, 45),
    'Oil_Condition': np.random.normal(75, 12, 200).clip(40, 95)
}

df = pd.DataFrame(data)

# Train ML model
X = df[["Temperature (C)", "Viscosity (cSt)", "Turbidity", "Oil_Humidity_percent"]]
y = df["Oil_Condition"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
joblib.dump(model, "model.joblib")

# Test prediction
sample_pred = model.predict([[60, 45, 15, 30]])[0]
print(f"✅ Model trained successfully!")
print(f"📊 Sample prediction for [60,45,15,30]: {sample_pred:.2f}")
print(f"📁 Model saved as 'model.joblib'")
print(f"📈 Dataset shape: {df.shape}")