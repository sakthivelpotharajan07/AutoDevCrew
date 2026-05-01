from pydantic import BaseModel
from typing import Optional

class City(BaseModel):
    id: int
    name: str
    lat: float
    lon: float

class CurrentWeather(BaseModel):
    dt_txt: str
    main: dict
    weather: list

class ForecastWeather(BaseModel):
    dt_txt: str
    main: dict
    list: list

class UserPreferences(BaseModel):
    unit_of_measurement: Optional[str] = "metric"

class WeatherResponse(BaseModel):
    current_weather: Optional[CurrentWeather]
    forecast_weather: Optional[ForecastWeather]
    user_preferences: UserPreferences

class CityRequest(BaseModel):
    name: str