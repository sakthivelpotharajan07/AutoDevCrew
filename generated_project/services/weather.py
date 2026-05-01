from typing import Dict, List
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

class Location:
    def __init__(self, name: str, city: str):
        self.name = name
        self.city = city

class WeatherService:
    def fetch_weather(self, location: Location, api_key: str = None) -> Dict:
        if api_key is None:
            url = f"http://wttr.in/{location.city}?m"
        else:
            url = f"http://wttr.in/{location.city}?m&format=j1&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        weather_data = soup.get_text().strip()

        return {
            'location_name': location.name,
            'city': location.city,
            'weather': weather_data
        }

    def process_weather_data(self, location_name: str, weather_data: str) -> Dict:
        return {
            'location_name': location_name,
            'weather': weather_data
        }