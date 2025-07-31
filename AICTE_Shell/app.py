import streamlit as st
import numpy as np
import joblib
import os

st.set_page_config(page_title="Smart Sprinkler System", layout="centered")

st.title("💧 Smart Sprinkler System")
st.subheader("Enter scaled sensor values (0 to 1) to predict sprinkler status")

# Try loading the model
model_path = "Farm_irrigation.pkl"  # make sure the file name matches exactly

if not os.path.exists(model_path):
    st.error(f"Model file '{model_path}' not found. Please check the file name or path.")
else:
    model = joblib.load(model_path)

    # Collect sensor inputs (scaled values)
    sensor_values = []
    for i in range(20):
        val = st.slider(f"Sensor {i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        sensor_values.append(val)

    # Predict button
    if st.button("Predict Sprinklers"):
        input_array = np.array(sensor_values).reshape(1, -1)
        try:
            prediction = model.predict(input_array)[0]
            st.markdown("### 🧠 Prediction Result:")
            for i, status in enumerate(prediction):
                st.write(f"Sprinkler {i} (parcel_{i}): **{'ON' if status == 1 else 'OFF'}**")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
