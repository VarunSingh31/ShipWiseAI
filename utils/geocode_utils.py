import os
import requests
from dotenv import load_dotenv

load_dotenv()

ROUTES_API_KEY = os.getenv("OPENROUTESERVICE_API_KEY")

def get_coordinates(location_name):
    url = "https://api.openrouteservice.org/geocode/search"
    headers = {
        'Authorization': ROUTES_API_KEY 
    }
    params = {
        'text': location_name,
        'size': 1
    }

    print(f"API Key Loaded: {ROUTES_API_KEY}")

    response = requests.get(url, headers=headers, params=params)

    print(f" API URL Called: {response.url}")
    print(f" API Status Code: {response.status_code}")
    print(f" API Raw JSON: {response.text}")

    if response.status_code != 200:
        print(f"API call failed for {location_name}.")
        return None, None

    data = response.json()
    features = data.get('features', [])

    if not features:
        print(f"No coordinates found for {location_name}.")
        return None, None

    coordinates = features[0]['geometry']['coordinates']
    return coordinates[1], coordinates[0]  
