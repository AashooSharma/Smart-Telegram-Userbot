import requests
from dotenv import load_dotenv
import os

load_dotenv()

class WeatherManager:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city_name):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city_name,
            "appid": self.api_key,
            "units": "metric"
        }

        response = requests.get(base_url, params=params)
        weather_data = response.json()

        if response.status_code == 200:
            weather_info = {
                "city": weather_data["name"],
                "temperature": weather_data["main"]["temp"],
                "description": weather_data["weather"][0]["description"]
            }
            return weather_info
        else:
            return None

# Initialize the WeatherManager
weather_manager = WeatherManager(os.getenv("WEATHER_API_KEY"))

