import subprocess
import sys
import os
import time
import signal

dir_path = os.path.dirname(os.path.abspath(__file__))

print("🚀 Starting MQTT Publisher...")
publisher = subprocess.Popen(
    [sys.executable, os.path.join(dir_path, "mqtt_publisher.py")],
    cwd=dir_path
)

print("🌐 Starting Streamlit Dashboard...")
dashboard = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", os.path.join(dir_path, "dashboard.py")],
    cwd=dir_path
)

print("\n✅ Both services running. Press Ctrl+C to stop.\n")

try:
    dashboard.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    publisher.terminate()
    dashboard.terminate()
    publisher.wait()
    dashboard.wait()
    print("✅ Done.")
