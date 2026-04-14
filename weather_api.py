import requests
from config import API_KEY

def get_weather(city_name):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric"
        
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            raise Exception(f"API Error: {response.status_code}, {response.text}")

        data_json = response.json()

        main = data_json.get("main", {})

        data = {
            "city": city_name,
            "temperature": main.get("temp", 0),
            "humidity": main.get("humidity", 0),
            "pressure": main.get("pressure", 0)
        }

        return data

    except Exception as e:
        print(f"Error fetching weather for {city_name}:", e)
        return {
            "city": city_name,
            "temperature": 0,
            "humidity": 0,
            "pressure": 0
        }