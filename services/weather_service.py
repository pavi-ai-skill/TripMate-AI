import requests
from datetime import datetime, timedelta
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL # or your chosen endpoint

    def get_forecast_for_date(self, location: str, target_date: str) -> dict:
        """Fetches or matches forecast data for a specific calendar date."""
        # Your underlying OpenWeather API call logic for a single date/timestamp goes here
        try:
            params = {
            "q": location,
            "appid": self.api_key,
            "units": "imperial"
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Filter 3-hour intervals matching the target date
            matching_slots = [
                item for item in data.get("list", []) 
                if item.get("dt_txt", "").startswith(target_date)
            ]
            
            if not matching_slots:
                return {
                    "success": False, 
                    "error": f"No forecast data available for {target_date}", 
                    "date": target_date,
                    "location": location
                }
                
            temps = [slot.get("main", {}).get("temp") for slot in matching_slots if slot.get("main", {}).get("temp") is not None]
            descriptions = [slot.get("weather", [{}])[0].get("description", "") for slot in matching_slots]
            
            return {
                "success": True,
                "date": target_date,
                "location": data.get("city", {}).get("name", location),
                "condition": max(set(descriptions), key=descriptions.count).capitalize() if descriptions else "Clear",
                "temp_high_f": round(max(temps), 1) if temps else 0,
                "temp_low_f": round(min(temps), 1) if temps else 0
            }
        except Exception as e:
            return {"success": False, "error": str(e), "date": target_date}

    def get_forecast_range(self, location: str, start_date: str, end_date: str) -> dict:
        """Loops through each date in the trip window and fetches the weather forecast."""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        delta = end - start
        
        daily_forecasts = {}
        for i in range(delta.days + 1):
            day = start + timedelta(days=i)
            target_date = day.strftime("%Y-%m-%d")
            
            # Fetch for this specific day
            daily_forecasts[target_date] = self.get_forecast_for_date(location, target_date)
            
        return daily_forecasts