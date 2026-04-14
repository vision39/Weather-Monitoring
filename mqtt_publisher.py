import paho.mqtt.client as mqtt
import time
import json
from weather_api import get_weather
from config import CITIES, MQTT_BROKER, MQTT_PORT, TOPIC

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

while True:
    for city in CITIES:
        data = get_weather(city)
        data["timestamp"] = time.time()

        client.publish(TOPIC, json.dumps(data))
        print(f"MQTT Sent for {city}:", data)

    time.sleep(5)
