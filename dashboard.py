import streamlit as st
import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime
import threading
from config import MQTT_BROKER, MQTT_PORT, TOPIC

# Page setup
st.set_page_config(page_title="Weather IoT Dashboard", layout="wide")
st.title("🌦️ Weather Monitoring Dashboard (MQTT)")

# 1. Global state using cache_resource to persist across all reruns and user sessions
@st.cache_resource
def get_mqtt_client():
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

@st.cache_resource
def get_global_data():
    return []

client = get_mqtt_client()
data_store = get_global_data()

# 2. MQTT Callbacks
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        data["time"] = datetime.now().strftime("%H:%M:%S")
        data_store.append(data)
        print("Message Received:", data)
    except Exception as e:
        print("Error:", e)

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect")

client.on_message = on_message
client.on_connect = on_connect

# 3. Start MQTT thread only once globally
@st.cache_resource
def start_mqtt_thread():
    def mqtt_loop():
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_forever()
    threading.Thread(target=mqtt_loop, daemon=True).start()
    return True

start_mqtt_thread()

# 4. UI Display
st.subheader("📡 Live Weather Data")

if data_store:
    df = pd.DataFrame(data_store)
    
    # Select city to display
    cities = df["city"].unique().tolist()
    selected_city = st.selectbox("Select City", cities)
    
    city_df = df[df["city"] == selected_city].reset_index(drop=True)
    
    if not city_df.empty:
        latest = city_df.iloc[-1]

        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Temperature (°C)", latest.get("temperature", "N/A"))
        col2.metric("💧 Humidity (%)", latest.get("humidity", "N/A"))
        col3.metric("🌪️ Pressure (hPa)", latest.get("pressure", "N/A"))

        st.subheader(f"📈 Temperature Trend for {selected_city}")
        if "time" in city_df.columns:
            st.line_chart(city_df.set_index("time")["temperature"])
        else:
            st.line_chart(city_df["temperature"])

        st.subheader(f"📋 Raw Data for {selected_city}")
        st.dataframe(city_df)
else:
    st.info("Waiting for data...")

# Auto refresh (important for live updates)
import time
time.sleep(1)
st.rerun()