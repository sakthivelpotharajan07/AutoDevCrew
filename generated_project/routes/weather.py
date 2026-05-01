from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse
import requests
import logging
from routes.dependencies import get_api_key

router = APIRouter()

class Weather(BaseModel):
    coord: Dict[str, float]
    weather: List[Dict[str, str]]
    main: Dict[str, float]
    wind: Dict[str, float]
    sys: Dict[str, int]
    dt: int
    id: int
    name: str
    cod: int

@router.get("/weather/{city}")
async def get_weather(city: str, api_key: str = Depends(get_api_key)):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return JSONResponse(content=response.json(), media_type="application/json")
    else:
        raise HTTPException(status_code=response.status_code)

@router.get("/weather/{city}/forecast")
async def get_weather_forecast(city: str, api_key: str = Depends(get_api_key)):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return JSONResponse(content=response.json(), media_type="application/json")
    else:
        raise HTTPException(status_code=response.status_code)