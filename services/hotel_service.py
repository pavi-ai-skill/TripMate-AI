from tavily import TavilyClient
from config import Config

class HotelSearchService:
    def __init__(self):
        # Validate that the API key exists in .env before initializing client
        Config.validate()
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)

    def search_hotels(self, location: str, preferences: str = "", max_results: int = 5) -> dict:
        search_query = f"best hotels in {location} {preferences}".strip()
        
        try:
            response = self.client.search(
                query=search_query,
                search_depth="advanced",
                max_results=max_results,
                include_images=True
            )
            
            parsed_hotels = []
            for item in response.get("results", []):
                parsed_hotels.append({
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "snippet": item.get("content"),
                    "score": item.get("score")
                })
                
            return {
                "success": True,
                "location": location,
                "hotels": parsed_hotels
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "hotels": []
            }