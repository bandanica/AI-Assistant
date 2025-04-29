from langchain.tools import tool
from services.weather_service import WeatherService

class WeatherTools:
    @tool
    def get_weather_info(city: str) -> str:
        """
        Get the weather for a given location.

        Args:
            location (str): The name of the location for which to retrieve weather.

        Returns:
            str: A string representing the weather forecast for the location.
        """
        weather = WeatherService.get_weather_info(city)
        return weather.to_prompt()
