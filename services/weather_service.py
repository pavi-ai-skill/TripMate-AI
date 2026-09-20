import requests
from config import Config

class WeatherService:
    def __init__(self):
        Config.validate()
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self, city: str) -> dict:
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"  # Change to 'imperial' if you prefer Fahrenheit
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "city": data.get("name"),
                    "temperature": data["main"]["temp"],
                    "condition": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"]
                }
            else:
                return {
                    "success": False,
                    "error": data.get("message", "Failed to fetch weather data."),
                    "city": city
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "city": city
            }