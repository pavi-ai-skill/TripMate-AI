from mcp.server.fastmcp import FastMCP
from services.weather_service import WeatherService

weather_service = WeatherService()

def register_weather_tools(mcp: FastMCP):
    """Registers weather search tools onto the FastMCP server instance."""
    
    @mcp.tool()
    def get_current_weather(city: str) -> dict:
        """
        Get current weather conditions and temperature for a given city.
        
        Args:
            city: The name of the city (e.g., "Charlotte, US" or "Paris, FR").
        """
        return weather_service.get_current_weather(city=city)