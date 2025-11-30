import os
import requests

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None
