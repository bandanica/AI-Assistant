import requests
from openai import OpenAI

class WhatToWearAssistant:
    def __init__(self, model="llama3.2", base_url="http://localhost:11434/v1/"):
        self.client = OpenAI(api_key="ollama", base_url=base_url)
        self.model = model

    def get_weather_info(self, city: str) -> dict:
        """
        Fetch weather data for a given city.
        Currently hardcoded.
        """
        return {
            "city": city,
            "temperature": 20,     # in Celsius
            "condition": "Cloudy",
            "wind": 6,             # in km/h
            "humidity": 60         # in percent
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
