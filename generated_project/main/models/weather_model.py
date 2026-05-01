# File: models/weather_model.py

from pydantic import BaseModel
from datetime import datetime

# Data model for the weather API data
class WeatherData(BaseModel):
    coord: dict
    weather: list
    base: str
    main: dict
    visibility: int
    wind: dict
    clouds: dict
    dt_txt: datetime

    class Config:
        orm_mode = True

class WeatherForecast(BaseModel):
    weather: list
    main: dict
    wind: dict
    clouds: dict
    dt_txt: datetime

    class Config:
        orm_mode = True