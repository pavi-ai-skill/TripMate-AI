from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from services.aviation_service import AviationService
from services.hotel_service import HotelSearchService
from services.weather_service import WeatherService
from agents.travel_state import TravelState
from config import Config

Config.validate()

aviation_svc = AviationService()
hotel_svc = HotelSearchService()
weather_svc = WeatherService()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    api_key=Config.GROQ_API_KEY
)

# 1. Update extraction schema to include dates
class TravelParameters(BaseModel):
    origin: str = Field(description="Origin city or airport IATA code (e.g., CLT)")
    destination: str = Field(description="Destination city or airport IATA code (e.g., Paris or CDG)")
    preferences: str = Field(description="Hotel style, preferences, or specific requirements")
    start_date: str = Field(description="Trip departure or start date in YYYY-MM-DD format (Current year is 2026)")
    end_date: str = Field(description="Trip return or end date in YYYY-MM-DD format (Current year is 2026)")

def parse_user_query(state: TravelState):
    print("Parsing user input sentence and extracting dates...")
    structured_llm = llm.with_structured_output(TravelParameters)
    prompt = f"Extract the origin, destination, preferences, start_date, and end_date from this travel request: '{state['user_query']}'"
    
    result: TravelParameters = structured_llm.invoke([
        SystemMessage(content="You are a precise data extraction assistant. Resolve relative dates like 'next week' or 'September 18th' into exact YYYY-MM-DD format assuming the current year is 2026."),
        HumanMessage(content=prompt)
    ])
    
    return {
        "origin": result.origin,
        "destination": result.destination,
        "preferences": result.preferences,
        "start_date": result.start_date,
        "end_date": result.end_date
    }

def fetch_flights(state: TravelState):
    """Step 2: Fetch both departure and return flight options."""
    print(f"Fetching round-trip flights between {state['origin']} and {state['destination']} ({state['start_date']} to {state['end_date']})...")
    
    result = aviation_svc.search_round_trip_flights(
        origin=state["origin"],
        destination=state["destination"],
        start_date=state["start_date"],
        end_date=state["end_date"]
    )
    return {"flight_data": result}

def fetch_hotels(state: TravelState):
    print(f"Fetching hotels in {state['destination']} from {state['start_date']} to {state['end_date']}...")
    result = hotel_svc.search_hotels(location=state["destination"], preferences=state["preferences"])
    return {"hotel_data": result}

def fetch_weather(state: TravelState):
    """LangGraph node: fetches the full weather range for the trip."""
    print(f"Fetching daily weather range for {state['destination']}...")
    
    weather_data = weather_svc.get_forecast_range(
        location=state["destination"],
        start_date=state["start_date"],
        end_date=state["end_date"]
    )
    
    return {"weather_data": weather_data}

def consolidate_itinerary(state: TravelState):
    """Step 3/5: Synthesize itinerary with round-trip flights, hotels, and daily weather."""
    print("Consolidating itinerary with round-trip flights...")
    prompt = f"""
    You are an expert travel agent. Create a polished, comprehensive travel itinerary based on:
    
    - Request: {state['user_query']}
    - Trip Dates: {state['start_date']} through {state['end_date']}
    - Origin: {state['origin']}
    - Destination: {state['destination']}
    - Preferences: {state['preferences']}
    
    Round-Trip Flight Options:
    {state['flight_data']}
    
    Hotel Options:
    {state['hotel_data']}
    
    Filtered Weather Forecast for Trip Dates:
    {state['weather_data']}
    
    MANDATORY INSTRUCTIONS:
    1. Structure the itinerary strictly day-by-day from departure on {state['start_date']} to return on {state['end_date']}.
    2. For **each specific calendar date**, look up its corresponding entry in the **Day-by-Day Weather Forecast** dictionary.
    3. Prominently display the expected temperature and conditions at the beginning of each daily schedule block.
    4. Provide practical packing or activity adjustments tailored directly to that specific day's forecasted weather (e.g., rain gear if precipitation is expected, comfortable layers for cooler days).
    """
    
    response = llm.invoke([
        SystemMessage(content="You are a professional travel coordinator assistant who expertly integrates round-trip flight schedules into daily itineraries."),
        HumanMessage(content=prompt)
    ])
    
    return {"consolidated_itinerary": response.content}

# Build Workflow
workflow = StateGraph(TravelState)

workflow.add_node("parse_query", parse_user_query)
workflow.add_node("fetch_flights", fetch_flights)
workflow.add_node("fetch_hotels", fetch_hotels)
workflow.add_node("fetch_weather", fetch_weather)
workflow.add_node("consolidate_itinerary", consolidate_itinerary)

workflow.set_entry_point("parse_query")
workflow.add_edge("parse_query", "fetch_flights")
workflow.add_edge("fetch_flights", "fetch_hotels")
workflow.add_edge("fetch_hotels", "fetch_weather")
workflow.add_edge("fetch_weather", "consolidate_itinerary")
workflow.add_edge("consolidate_itinerary", END)

travel_graph = workflow.compile()