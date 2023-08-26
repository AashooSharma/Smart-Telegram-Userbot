import requests
from bs4 import BeautifulSoup

class Function2:
    def __init__(self, client):
        self.client = client

    async def handle_weather(self, event, location):
        try:
            weather_data = self.get_weather_data(location)
            if weather_data:
                await event.reply(self.format_weather_data(weather_data))
            else:
                await event.reply("Sorry, couldn't retrieve weather information.")
        except Exception as e:
            await event.reply("An error occurred while fetching weather information.")

    def get_weather_data(self, location):
        url = f"https://www.weather.com/en-IN/weather/today/l/{location}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            temperature = soup.find("div", class_="today_nowcard-temp").text.strip()
            condition = soup.find("div", class_="today_nowcard-phrase").text.strip()
            return {"temperature": temperature, "condition": condition}
        return None

    def format_weather_data(self, data):
        return f"Current weather:\nTemperature: {data['temperature']}°C\nCondition: {data['condition']}"

# Usage example:
# function_2 = Function2(client)
# await function_2.handle_weather(event, "your_location_code")

