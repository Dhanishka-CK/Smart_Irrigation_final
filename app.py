import streamlit as st
import numpy as np
import joblib
import requests

st.set_page_config(page_title="Smart Sprinkler System", layout="centered")

st.title("💧 Smart Sprinkler System")
st.subheader("Enter scaled sensor values (0 to 1) to predict sprinkler status")

# Load weather API key from secrets
api_key = st.secrets["weather_api"]["key"]

# Load model
model_path = "Farm_irrigation.pkl"
try:
    model = joblib.load(model_path)
except Exception as e:
    st.error(f"❌ Could not load model file: {e}")
    st.stop()

# Collect sensor inputs
sensor_values = []
for i in range(20):
    val = st.slider(f"Sensor {i}", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    sensor_values.append(val)

# Auto Weather Mode
auto_weather_mode = st.checkbox("🌦️ Auto Weather Mode (Skip if Rain Expected)", value=True)

# City Input
city = st.text_input("Enter your city for weather forecast", value="Coimbatore")

# Predict button
if st.button("Predict Sprinklers"):
    # Weather check
    skip_due_to_weather = False
    if auto_weather_mode:
        try:
            url = (
                f"http://api.openweathermap.org/data/2.5/forecast"
                f"?q={city}&appid={api_key}&units=metric"
            )
            response = requests.get(url)
            data = response.json()
            if "list" in data:
                next_12h = data["list"][:4]
                rain_expected = any("rain" in entry for entry in next_12h)
                if rain_expected:
                    skip_due_to_weather = True
                    st.warning("🌧️ Rain is expected in the next 12 hours. Irrigation skipped.")
            else:
                st.warning("⚠️ Weather data unavailable. Proceeding without weather control.")
        except Exception as e:
            st.warning(f"⚠️ Weather API error: {e}")

    if not skip_due_to_weather:
        input_array = np.array(sensor_values).reshape(1, -1)
        try:
            prediction = model.predict(input_array)[0]
            st.markdown("### 🧠 Prediction Result:")
            for i, status in enumerate(prediction):
                st.write(f"Sprinkler {i}: **{'ON' if status == 1 else 'OFF'}**")
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")