from pydantic import BaseModel
from typing import Optional

class Weather(BaseModel):
    id: Optional[int]
    city: str
    country: str
    temperature: float
    humidity: float
    wind_speed: float
    forecast: str

class Location(BaseModel):
    id: Optional[int]
    city: str
    country: str

class WeatherData(BaseModel):
    id: Optional[int]
    location_id: int
    temperature: float
    humidity: float
    wind_speed: float
    forecast: str
    created_at: Optional[str]