# train_model.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load your dataset (adjust the path or filename if needed)
data = pd.read_csv("irrigation_machine.csv")

# Assuming the first 20 columns are sensor inputs, and next 20 are sprinkler outputs
X = data.iloc[:, :20]     # Sensor values
y = data.iloc[:, 20:]     # Sprinkler on/off status for parcels

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model — note: a multi-output classifier is needed
from sklearn.multioutput import MultiOutputClassifier
clf = MultiOutputClassifier(RandomForestClassifier(random_state=42))
clf.fit(X_train, y_train)

# Save the trained model
joblib.dump(clf, "Farm_irrigation.pkl")

print("✅ Model trained and saved as 'Farm_irrigation.pkl'")
