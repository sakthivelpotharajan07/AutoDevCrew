# File: utilities.py

from typing import Dict, List
from pydantic import BaseModel

class WeatherData(BaseModel):
    """Represents the weather data response from the API."""
    main: Dict
    weather: List[Dict]

def parse_weather_data(weather_api_response: Dict) -> WeatherData:
    """
    Extracts the relevant weather data from the API response.

    Args:
        weather_api_response: The raw response from the weather API.

    Returns:
        A WeatherData object containing the extracted data.
    """
    return WeatherData(
        main=weather_api_response['main'],
        weather=weather_api_response['weather']
    )

class Units(BaseModel):
    """Represents the unit preferences."""
    temperature: str

UNITS = [
    Units(temperature='metric'),
    Units(temperature='imperial'),
    Units(temperature='standard')
]

def get_units_by_key(key: str) -> Units:
    """
    Retrieves the units by the given key.

    Args:
        key: The key for the units.

    Returns:
        The Units object for the given key.
    """
    return next((u for u in UNITS if u.temperature == key), None)