from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date
from typing import Optional
import requests

from main import settings
from main.routes.auth_routes import get_authenticated_user

class WeatherResponse(BaseModel):
    location: str
    temperature: float
    conditions: str

def get_weather_data(location: str):
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

router = APIRouter(prefix="/weather", tags=["Weather"])

@router.get("/{location}")
async def get_weather(location: str = "", 
                      auth_user: dict = Depends(get_authenticated_user)) -> JSONResponse:
    if location:
        weather_data = get_weather_data(location)
        if weather_data:
            weather_response = WeatherResponse(
                location=weather_data["name"],
                temperature=weather_data["main"]["temp"] - 273.15,
                conditions=weather_data["weather"][0]["description"]
            )
            return {"user": auth_user, "weather": weather_response}
        else:
            return {"error": "Failed to retrieve weather data"}
    return {"error": "Missing location"}

@router.get("/today")
async def get_today_weather(auth_user: dict = Depends(get_authenticated_user)) -> JSONResponse:
    today = date.today().strftime("%Y-%m-%d")
    return Response(content={"today": today, "user": auth_user}, medium="text")

@router.get("/settings")
async def get_settings(auth_user: dict = Depends(get_authenticated_user)) -> dict:
    return {"api_key": settings.OPENWEATHERMAP_API_KEY, "user": auth_user}