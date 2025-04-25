import requests
from openai import OpenAI
from dataclasses import dataclass
from typing import Optional
import os 

@dataclass
class WeatherInfo:
    city: str
    temperature: float
    condition: str
    wind: float
    humidity: Optional[float] = None

    def to_prompt(self) -> str:
        humidity_str = f"{self.humidity}%" if self.humidity is not None else "unknown"
        return (
            f"The current weather in {self.city} is {self.condition}, "
            f"{self.temperature}°C with wind speed {self.wind} km/h. "
            f"Humidity is {humidity_str}.\n\n"
            "Based on this weather, what should I wear today? Provide a brief and practical outfit recommendation."
        )
    
class WeatherService:
    @staticmethod
    def get_coordinates(city: str) -> tuple:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        response = requests.get(url, headers={"User-Agent": "weather-assistant"})
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError(f"City '{city}' not found.")

        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon

    @staticmethod
    def interpret_weather_code(code: int) -> str:
        weather_map = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            95: "Thunderstorm",
            99: "Thunderstorm with hail"
        }
        return weather_map.get(code, "Unknown")

    @classmethod
    def get_weather_info(cls, city: str) -> WeatherInfo:
        lat, lon = cls.get_coordinates(city)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        current = data["current_weather"]
        return WeatherInfo(
            city=city,
            temperature=current["temperature"],
            condition=cls.interpret_weather_code(current["weathercode"]),
            wind=current["windspeed"]
        )

class WhatToWearAssistant:
    def __init__(self, model="llama3.2", base_url="http://localhost:11434/v1/"):
        api_key = os.getenv("OLLAMA_API_KEY", "ollama")
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def get_outfit_recommendation(self, city: str) -> str:
        weather = WeatherService.get_weather_info(city)
        prompt = weather.to_prompt()

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that recommends appropriate clothing based on weather."
                },
                {"role": "user", "content": prompt}
            ],
            stream=False
        )

        return response.choices[0].message.content.strip()