import os
from typing import Optional
import requests
from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool


class WeatherInput(BaseModel):
    location: str = Field(description='City or lat/lon for weather lookup')
    date: Optional[str] = Field(None, description='YYYY-MM-DD (optional)')


class WeatherInputSchema(BaseModel):
    params: WeatherInput


@tool(args_schema=WeatherInputSchema)
def weather_tool(params: WeatherInput):
    """Weather tool: uses OpenWeatherMap current weather API when WEATHER_API_KEY is set.

    If the API key is not set or the call fails, returns a conservative static stub.
    """
    api_key = os.environ.get('WEATHER_API_KEY') or os.environ.get('OPENWEATHER_API_KEY')
    if api_key:
        try:
            # Use current weather endpoint for city name lookups
            resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params={
                'q': params.location,
                'appid': api_key,
                'units': 'metric'
            }, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            return {
                'location': params.location,
                'date': params.date or data.get('dt'),
                'forecast': data.get('weather', [{}])[0].get('description'),
                'temperature_c': data.get('main', {}).get('temp'),
                'precipitation_chance_pct': None
            }
        except Exception:
            pass

    # Fallback conservative stub
    return {
        'location': params.location,
        'date': params.date or '2025-10-16',
        'forecast': 'Partly cloudy',
        'temperature_c': 23,
        'precipitation_chance_pct': 10
    }
