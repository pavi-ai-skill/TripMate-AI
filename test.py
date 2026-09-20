from services.hotel_service import HotelSearchService
from services.weather_service import WeatherService
from services.aviation_service import AviationService

def test_all_services():
    print("=" * 50)
    print("TESTING 1: Hotel Search Service (Tavily)")
    print("=" * 50)
    try:
        hotel_service = HotelSearchService()
        hotel_result = hotel_service.search_hotels(
            location="Charlotte, NC", 
            preferences="boutique", 
            max_results=2
        )
        print("Hotel Result Status:", hotel_result.get("success"))
        print(f"Found {len(hotel_result.get('hotels', []))} hotels.")
        for h in hotel_result.get("hotels", []):
            print(f" - {h.get('title')}")
    except Exception as e:
        print("Hotel Test Failed:", str(e))

    print("\n" + "=" * 50)
    print("TESTING 2: Weather Service (OpenWeather)")
    print("=" * 50)
    try:
        weather_service = WeatherService()
        weather_result = weather_service.get_current_weather(city="Paris, FR")
        print("Weather Result:", weather_result)
    except Exception as e:
        print("Weather Test Failed:", str(e))

    print("\n" + "=" * 50)
    print("TESTING 3: Flight Search Service (AviationStack)")
    print("=" * 50)
    try:
        aviation_service = AviationService()
        aviation_result = aviation_service.search_flights_by_city(
            dep_city="CLT", 
            arr_city="CDG", 
            limit=2
        )
        print("Aviation Result Status:", aviation_result.get("success"))
        print(f"Found {len(aviation_result.get('flights', []))} flights.")
        for f in aviation_result.get("flights", []):
            print(f" - Airline: {f.get('airline')} | Flight: {f.get('flight_number')} | Status: {f.get('status')}")
    except Exception as e:
        print("Aviation Test Failed:", str(e))
    
    print("\n" + "=" * 50)
    print("All service tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    test_all_services()