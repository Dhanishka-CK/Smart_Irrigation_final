import streamlit as st
import numpy as np
import joblib
import os

st.set_page_config(page_title="Smart Sprinkler System", layout="centered")

st.title("💧 Smart Sprinkler System")
st.subheader("Enter scaled sensor values (0 to 1) to predict sprinkler status")

# Use absolute path to model file
model_path = os.path.join(os.path.dirname(__file__), "Farm_irrigation.pkl")

# Load the model if available
if not os.path.exists(model_path):
    st.error(f"Model file '{model_path}' not found. Please check the file name or path.")
else:
    model = joblib.load(model_path)

    # Collect sensor inputs (scaled values)
    sensor_values = []
    for i in range(20):
        val = st.slider(f"Sensor {i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        sensor_values.append(val)

    # Add a toggle switch for weather-based control
    auto_weather_mode = st.checkbox("🌦️ Auto Weather Mode (Skip if Rain Expected)", value=True)

    skip_irrigation = False  # default

    if auto_weather_mode:
        api_key = st.secrets["weather"]["api_key"]
        st.info("Auto Weather Mode is ON — checking for rainfall forecast...")
        # Simulate rain condition (this will be replaced by actual API result)
        rain_expected = True  # <-- Assume it's going to rain (we'll use actual API later)
        if rain_expected:
            st.warning("🌧️ Rain is expected — Irrigation will be skipped.")
            skip_irrigation = True
        else:
            st.success("No rain expected — Proceeding with prediction.")
    
    # Predict button
    if st.button("Predict Sprinklers"):
        if skip_irrigation:
            st.info("Prediction skipped due to expected rainfall.")
        else:
            input_array = np.array(sensor_values).reshape(1, -1)
            try:
                prediction = model.predict(input_array)[0]
                st.markdown("### 🧠 Prediction Result:")
                for i, status in enumerate(prediction):
                    st.write(f"Sprinkler {i} (parcel_{i}): **{'ON' if status == 1 else 'OFF'}**")
            except Exception as e:
                st.error(f"Prediction failed: {e}")
