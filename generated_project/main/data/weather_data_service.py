from datetime import datetime
from typing import List

from pydantic import BaseModel

class WeatherData(BaseModel):
    id: int
    main: str
    description: str
    icon: str

class CurrentWeatherData(BaseModel):
    id: int
    temp: float
    feels_like: float
    humidity: int
    weather: List[WeatherData]

class WeatherDataResponse(BaseModel):
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current_weather: CurrentWeatherData
    hourly_forecast: List

class WeatherApi:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_weather(self, lat: float, lon: float):
        # Replace this with your actual API call
        data = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }
        
        # Mock data
        return {
            "cod": "200",
            "message": 0,
            "cnt": 40,
            "list": [
                {
                    "dt": 1643723400,
                    "main": {
                        "temp": 297.15,
                        "feels_like": 296.71,
                        "humidity": 80,
                        "temp_min": 296.15,
                        "temp_max": 298.15,
                        "pressure": 1013,
                        "sea_level": 1013,
                        "grnd_level": 1013,
                    },
                    "weather": [
                        {
                            "id": 500,
                            "main": "Rain",
                            "description": "light rain",
                            "icon": "10d",
                        }
                    ],
                    "clouds": {
                        "all": 90,
                    },
                    "wind": {
                        "speed": 5.1,
                        "deg": 230,
                    },
                    "sys": {
                        "pod": "d",
                    },
                    "dt_txt": "2022-02-01 12:00:00"
                }
            ],
            "city": {
                "id": 3331111,
                "name": "Anytown",
                "coord": {
                    "lat": 45.12,
                    "lon": 1.23
                },
            }
        }
        
        # Parse JSON response using pydantic
        response = WeatherDataResponse(**data)
        if response.cod == "200":
            current_weather = CurrentWeatherData(
                **response.list[0],
                id=response.city.id
            )
            hourly_forecast = [
                WeatherData(**weather)
                for weather in response.list[:8]
            ]
            return {
                "current_weather": current_weather,
                "hourly_forecast": hourly_forecast
            }