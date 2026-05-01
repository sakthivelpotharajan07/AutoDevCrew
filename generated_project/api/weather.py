# weather.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import requests

app = FastAPI()

# Define data models for API responses
class Location(BaseModel):
    name: str
    lat: float
    lon: float

class CurrentWeatherResponse(BaseModel):
    lat: float
    lon: float
    weather: list[dict]
    main: dict
    wind: dict
    clouds: dict

class ForecastsWeatherResponse(BaseModel):
    lat: float
    lon: float
    forecast: list[dict]

# API routes

@app.get("/weather/current")
async def get_current_weather(lat: float, lon: float):
    try:
        api_response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=YOUR_API_KEY"
        )
        return CurrentWeatherResponse(**api_response.json())
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching weather data")

@app.get("/weather/forecast")
async def get_forecasts_weather(lat: float, lon: float):
    try:
        api_response = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid=YOUR_API_KEY&cnt=16"
        )
        return ForecastsWeatherResponse(**api_response.json())
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching weather forecast data")

@app.post("/weather/")
async def create_location(location: Location):
    return location