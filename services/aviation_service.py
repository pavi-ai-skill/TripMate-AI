import requests
from config import Config

class AviationService:
    def __init__(self):
        self.api_key = Config.AVIATIONSTACK_API_KEY
        self.base_url = Config.AVIATIONSTACK_BASE_URL

    def search_round_trip_flights(self, origin: str, destination: str, start_date: str, end_date: str):
        """Fetches both departure and return flights for the given trip dates."""
        try:
            # 1. Fetch Outbound Flight (Origin -> Destination)
            outbound_params = {
                "access_key": self.api_key,
                "dep_iata": origin,
                "arr_iata": destination,
                "flight_date": start_date
            }
            outbound_res = requests.get(self.base_url, params=outbound_params)
            outbound_res.raise_for_status()
            outbound_data = outbound_res.json().get("data", [])

            # 2. Fetch Return Flight (Destination -> Origin)
            return_params = {
                "access_key": self.api_key,
                "dep_iata": destination,
                "arr_iata": origin,
                "flight_date": end_date
            }
            return_res = requests.get(self.base_url, params=return_params)
            return_res.raise_for_status()
            return_data = return_res.json().get("data", [])

            return {
                "success": True,
                "outbound_flights": outbound_data[:5],  # Limit top results for brevity
                "return_flights": return_data[:5]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }