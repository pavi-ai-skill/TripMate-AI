import requests
from config import Config

class AviationService:
    def __init__(self):
        Config.validate()
        self.api_key = Config.AVIATIONSTACK_API_KEY
        self.base_url = Config.AVIATIONSTACK_BASE_URL

    def search_flights_by_city(self, dep_city: str, arr_city: str, limit: int = 5) -> dict:
        """
        Searches for flights using departure and arrival cities/airports.
        Note: Depending on your AviationStack plan, parameters can accept airport/city identifiers.
        """
        params = {
            "access_key": self.api_key,
            "dep_iata": dep_city.upper(),  # Expecting codes like 'CLT', 'JFK', etc.
            "arr_iata": arr_city.upper()
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and "data" in data:
                flights = data["data"]
                if not flights:
                    return {
                        "success": True,
                        "departure_city": dep_city,
                        "arrival_city": arr_city,
                        "flights": [],
                        "message": "No active flights found for this route."
                    }
                
                parsed_flights = []
                for flight_info in flights[:limit]:
                    parsed_flights.append({
                        "airline": flight_info.get("airline", {}).get("name"),
                        "flight_number": flight_info.get("flight", {}).get("iata"),
                        "status": flight_info.get("flight_status"),
                        "departure": {
                            "airport": flight_info.get("departure", {}).get("airport"),
                            "scheduled": flight_info.get("departure", {}).get("scheduled")
                        },
                        "arrival": {
                            "airport": flight_info.get("arrival", {}).get("airport"),
                            "scheduled": flight_info.get("arrival", {}).get("scheduled")
                        }
                    })
                
                return {
                    "success": True,
                    "departure_city": dep_city,
                    "arrival_city": arr_city,
                    "flights": parsed_flights
                }
            else:
                return {
                    "success": False,
                    "error": data.get("error", {}).get("message", "Failed to fetch flight data."),
                    "flights": []
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "flights": []
            }