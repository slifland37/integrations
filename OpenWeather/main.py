import requests
from requests.exceptions import HTTPError
import os
from dotenv import load_dotenv
import argparse
from models.current_weather import WeatherReport, WeatherReportParams, Units
import datetime

load_dotenv()
BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

def _print_daily_forecasts(forecast: WeatherReport):
    print("|Date|Summary|Morn|Day|Eve|Night|")
    print("|--|--|--|--|--|--|")
    for day in forecast.daily:
        ts = datetime.datetime.fromtimestamp(day.dt)
        temps = day.temp
        print(f"|{ts.strftime("%Y-%m-%d %H:%M:%S")}|{day.summary}|{temps.morn}|{temps.day}|{temps.eve}|{temps.night}|")


def get_weather(lat, long):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    params = WeatherReportParams(lat=lat, lon=long, appid=api_key, units=Units.imperial)
    try:
        response = requests.get(BASE_URL, params=params.model_dump(exclude_none=True))
        response.raise_for_status()
        data = response.json()
        if response.status_code == 200:
            weather = WeatherReport(**data)
            print(f"Lat: {weather.lat}, Long: {weather.lon}, Current Desc: {weather.current.weather[0].description}")
            _print_daily_forecasts(weather)
        else:
            print(f"Error: {data.get('message')}")
    except HTTPError as errh:
        print(f"HTTP error: {errh}")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch weather data based on lat-long")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--long", type=float, required=True, help="Longitude")
    args = parser.parse_args()

    get_weather(args.lat, args.long)