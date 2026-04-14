import streamlit as st
import paho.mqtt.client as mqtt
import json
import pandas as pd
from datetime import datetime
import threading
import time
from config import MQTT_BROKER, MQTT_PORT, TOPIC

# Page setup
st.set_page_config(page_title="Weather IoT Dashboard", layout="wide")
st.title("🌦️ Weather Monitoring Dashboard (MQTT)")

# --- Single cache_resource to initialize MQTT + shared data store atomically ---
@st.cache_resource
def init_mqtt():
    """Initialize MQTT client, callbacks, connection, and shared data store once."""
    data_store = []

    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("✅ Connected to MQTT Broker!")
            client.subscribe(TOPIC)
            print(f"✅ Subscribed to topic: {TOPIC}")
        else:
            print(f"❌ Failed to connect, reason code: {reason_code}")

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            data["time"] = datetime.now().strftime("%H:%M:%S")
            data_store.append(data)
            print(f"📩 Message Received: {data}")
        except Exception as e:
            print(f"❌ Error parsing message: {e}")

    def on_disconnect(client, userdata, flags, reason_code, properties=None):
        print(f"⚠️ Disconnected (reason: {reason_code}). Reconnecting...")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    # Connect and start the network loop in a background thread
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()  # Non-blocking background thread (better than loop_forever in a thread)

    return data_store

# Initialize once — returns the shared list
data_store = init_mqtt()

# --- UI Display ---
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
    st.info("⏳ Waiting for data... Make sure the MQTT publisher is running.")

# Auto-refresh every 2 seconds
time.sleep(2)
st.rerun()