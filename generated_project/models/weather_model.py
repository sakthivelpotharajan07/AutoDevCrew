from pydantic import BaseModel
from typing import Optional

class CurrentWeather(BaseModel):
    """Class to represent current weather."""
    weather_state: str
    temperature: float
    humidity: float
    wind_speed: float

class Forecast(BaseModel):
    """Class to represent forecast weather."""
    date: str
    weather_state: str
    high: float
    low: float

class Location(BaseModel):
    """Class to represent a geographic location."""
    city: str
    state: Optional[str]
    country: Optional[str]
    lat: float
    lon: float

class WeatherModel(BaseModel):
    """Class to represent a weather data model."""
    current: CurrentWeather
    forecast: list[Forecast]
    location: Location