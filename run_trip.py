from agents.travel_graph import travel_graph

def main():
    initial_state = {
        "user_query": "I want to plan a trip from Charlotte to Paris from September 18, 2026 to September 25, 2026, staying at a boutique hotel.",
        "origin": "",
        "destination": "",
        "preferences": "",
        "start_date": "",
        "end_date": "",
        "flight_data": {},
        "hotel_data": {},
        "weather_data": {},
        "consolidated_itinerary": ""
    }
    
    print("Starting Date-Aware Travel Workflow...\n")
    final_state = travel_graph.invoke(initial_state)
    
    print("\n" + "="*40 + "\n")
    print("FINAL CONSOLIDATED ITINERARY:")
    print("="*40 + "\n")
    print(final_state["consolidated_itinerary"])

if __name__ == "__main__":
    main()