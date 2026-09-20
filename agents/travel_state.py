from typing import TypedDict, Dict, Any

class TravelState(TypedDict):
    user_query: str
    
    # Parsed Inputs
    origin: str
    destination: str
    preferences: str
    start_date: str  # YYYY-MM-DD format
    end_date: str    # YYYY-MM-DD format
    
    # Tool Outputs
    flight_data: Dict[str, Any]
    hotel_data: Dict[str, Any]
    weather_data: Dict[str, Any]
    
    # Final Output
    consolidated_itinerary: str