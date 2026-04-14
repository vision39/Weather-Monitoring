import paho.mqtt.client as mqtt
import json
import time
from config import MQTT_BROKER, MQTT_PORT, TOPIC

def on_message(client, userdata, msg):
    receive_time = time.time()
    data = json.loads(msg.payload.decode())
    
    latency = receive_time - data["timestamp"]

    print("Received:", data)
    print("Latency:", latency, "seconds\n")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(TOPIC)

client.loop_forever()
