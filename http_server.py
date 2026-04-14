from flask import Flask, request
import time

app = Flask(__name__)

@app.route('/weather', methods=['POST'])
def receive_data():
    data = request.json
    receive_time = time.time()

    latency = receive_time - data["timestamp"]

    print("HTTP Received:", data)
    print("Latency:", latency, "\n")

    return {"status": "ok"}

app.run(port=5000)
