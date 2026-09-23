from mcp.server.fastmcp import FastMCP
from services.aviation_service import AviationService

aviation_service = AviationService()

def register_aviation_tools(mcp: FastMCP):
    """Registers aviation and flight tools onto the FastMCP server instance."""
    
    @mcp.tool()
    def search_flights(origin: str, destination: str, flight_date: str, max_results: int = 5) -> dict:
        """
        Search for available flights between an origin city/airport and destination city/airport for a specific date.
        
        Args:
            origin: Origin airport or city IATA code (e.g., "CLT").
            destination: Destination airport or city IATA code (e.g., "CDG").
            flight_date: Date of the flight in YYYY-MM-DD format (Current year is 2026).
            max_results: Maximum number of flight results to return.
        """
        return aviation_service.search_flights_by_city(
            dep_city=origin,
            arr_city=destination,
            flight_date=flight_date,
            limit=max_results
        )