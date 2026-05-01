from pydantic import BaseModel
from typing import Optional

class WeatherData(BaseModel):
    coord: dict
    weather: list
    base: str
    main: dict
    visibility: int
    wind: dict
    clouds: dict
    dt: int
    sys: dict
    timezone: int
    id: int
    name: str
    cod: int

class WeatherLocation(BaseModel):
    name: str
    weather: list[WeatherData]

class WeatherForecast(BaseModel):
    lat: float
    lon: float
    timezone: int
    current_weather: WeatherData
    location_forecast: list[WeatherLocation]

class WeatherLocationForecast(BaseModel):
    name: str
    weather: list
    temp_min: float
    temp_max: float

class WeatherForecastResponse(BaseModel):
    lat: float
    lon: float
    timezone: int
    current_weather: WeatherData
    location_forecasts: list[WeatherLocationForecast]