import requests
from openai import OpenAI

class WhatToWearAssistant:
    def __init__(self, model="llama3.2", base_url="http://localhost:11434/v1/"):
        self.client = OpenAI(api_key="ollama", base_url=base_url)
        self.model = model

    def get_coordinates(self, city: str) -> tuple:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
        response = requests.get(url, headers={"User-Agent": "weather-assistant"})
        data = response.json()
        
        if not data:
            raise ValueError("City not found.")
        
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    
    def interpret_weather_code(self, code: int) -> str:
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

    def get_weather_info(self, city: str) -> dict:
        lat, lon = self.get_coordinates(city)

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )

        response = requests.get(weather_url)
        data = response.json()

        current = data["current_weather"]

        return {
            "city": city,
            "temperature": current["temperature"],
            "condition": self.interpret_weather_code(current["weathercode"]),
            "wind": current["windspeed"],
            "humidity": None 
        }

    def build_prompt(self, weather_data: dict) -> str:
        """
        Build the user prompt for the LLM based on the current weather data.
        """
        return (
            f"The current weather in {weather_data['city']} is {weather_data['condition']}, "
            f"{weather_data['temperature']}°C with wind speed {weather_data['wind']} km/h. "
            f"Humidity is {weather_data['humidity']}%.\n\n"
            "Based on this weather, what should I wear today? Provide a brief and practical outfit recommendation."
        )

    def get_outfit_recommendation(self, city: str) -> str:
        """
        Main function to get a clothing recommendation based on city weather.
        """
        weather = self.get_weather_info(city)
        user_prompt = self.build_prompt(weather)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that recommends appropriate clothing based on weather."},
                {"role": "user", "content": user_prompt}
            ],
            stream=False
        )

        return response.choices[0].message.content.strip()
