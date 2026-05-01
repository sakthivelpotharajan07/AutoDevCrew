from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI()

class WeatherData(BaseModel):
    location: str
    temperature: float
    humidity: float
    condition: str

@app.get("/")
def read_root():
    return {"Welcome": "to Weather API"}

@app.get("/weather/{location}")
async def get_weather_info(location: str):
    try:
        api_key = "your_openweathermap_api_key"
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            return {
                "location": location,
                "temperature": data["main"]["temp"] - 273.15,
                "humidity": data["main"]["humidity"],
                "condition": data["weather"][0]["description"]
            }
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server Error")