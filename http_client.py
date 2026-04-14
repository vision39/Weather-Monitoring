import paho.mqtt.client as mqtt
import time
import json
from weather_api import get_weather
from config import MQTT_BROKER, MQTT_PORT, TOPIC

# Create MQTT client
client = mqtt.Client(client_id="publisher_client_ankit")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

print("MQTT Publisher Started...")

while True:
    try:
        # Get weather data
        data = get_weather()
        data["timestamp"] = time.time()

        # Send via MQTT
        client.publish(TOPIC, json.dumps(data))
        print("MQTT Sent:", data)

    except Exception as e:
        print("Error:", e)

    time.sleep(5)
