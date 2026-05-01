from typing import Dict
from fastapi import HTTPException
import requests
import json

class WeatherService:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_weather(self, city: str) -> Dict:
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as errh:
            raise HTTPException(status_code=500, detail="Error fetching weather data") from errh
        except requests.exceptions.ConnectionError as errc:
            raise HTTPException(status_code=500, detail="Error connecting to weather API") from errc
        except requests.exceptions.Timeout as errt:
            raise HTTPException(status_code=500, detail="Timeout error fetching weather data") from errt
        except requests.exceptions.RequestException as err:
            raise HTTPException(status_code=500, detail="Something went wrong") from err

    def get_current_weather(self, city: str) -> Dict:
        data = self.get_weather(city)
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description']
        }