import requests
import os
from dotenv import load_dotenv
import argparse

load_dotenv()
BASE_URL = "http://api.weatherstack.com/current"

# Helper to build the query parameter
def build_query_param(city, lat, lon):
    query_parts = []
    
    if city and city.strip():  # Check if city is not empty and not just whitespace
        # Support multiple cities: comma or semicolon separated
        if isinstance(city, list):
            query_parts.extend(city)
        elif "," in city:
            query_parts.extend([c.strip() for c in city.split(",") if c.strip()])  # Filter out empty parts
        else:
            query_parts.append(city.strip())
    
    if lat is not None and lon is not None:
        query_parts.append(f"{lat},{lon}")
    
    if not query_parts:
        raise ValueError("You must provide either a city or both lat and lon.")
    
    return ";".join(query_parts)

def print_weather_result(data):
    # If multiple locations, Weatherstack returns a list for location/current
    locations = data["location"] if isinstance(data["location"], list) else [data["location"]]
    currents = data["current"] if isinstance(data["current"], list) else [data["current"]]
    for location, current in zip(locations, currents):
        print(f"Location: {location['name']}, {location['country']}")
        print(f"Local Time: {location['localtime']}")
        print(f"Temperature: {current['temperature']}°C")
        print(f"Weather: {', '.join(current['weather_descriptions'])}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind: {current['wind_speed']} km/h {current['wind_dir']}")
        print(f"Feels Like: {current['feelslike']}°C")
        print()

def get_weather(city=None, lat=None, lon=None):
    api_key = os.getenv("WEATHERSTACK_API_KEY")
    if not api_key:
        print("Missing WEATHERSTACK_API_KEY in .env file.")
        return
    
    # Build initial query
    query = build_query_param(city, lat, lon)
    
    print(f"Query being sent to API: {query}")
    
    print()
    params = {
        "access_key": api_key,
        "query": query
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get("success", True) is False:
            print(f"Error: {data['error']['info']}")
            return
        print_weather_result(data)
    except requests.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch current weather using weatherstack.com API")
    parser.add_argument("--city", type=str, help="City name (e.g. London or 'London,Paris,Berlin'). Can be combined with coordinates.")
    parser.add_argument("--lat", type=float, help="Latitude. Can be combined with city.")
    parser.add_argument("--lon", type=float, help="Longitude. Can be combined with city.")
    args = parser.parse_args()
    get_weather(city=args.city, lat=args.lat, lon=args.lon)