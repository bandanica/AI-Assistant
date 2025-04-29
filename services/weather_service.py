import requests
from typing import Optional
from schemas.weather_info import WeatherInfo
import logging

logger = logging.getLogger(__name__)

class WeatherServiceError(Exception):
    pass

class WeatherService:
    WEATHER_CODE_MAPPING = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        95: "Thunderstorm",
        99: "Thunderstorm with hail",
    }

    @classmethod
    def get_coordinates(cls, city: str) -> tuple:
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
            response = requests.get(url, headers={"User-Agent": "weather-assistant"})
            response.raise_for_status()
            data = response.json()

            if not data:
                logger.error(f"No coordinates found for city: {city}")
                raise WeatherServiceError(f"No coordinates found for city: {city}")

            lat = float(data[0]['lat'])
            lon = float(data[0]['lon'])
            return lat, lon

        except requests.RequestException as e:
            logger.exception(f"Request failed while fetching coordinates for city {city}")
            raise WeatherServiceError(f"Error fetching coordinates for city {city}") from e
        
        except KeyError as e:
            logger.exception(f"Missing expected data in response while fetching coordinates for city {city}")
            raise WeatherServiceError(f"Error parsing coordinates for city {city}") from e
        
        except ValueError as e:
            logger.exception(f"Invalid value while parsing coordinates for city {city}")
            raise WeatherServiceError(f"Error processing coordinates for city {city}") from e

    @classmethod
    def get_weather_info(cls, city: str) -> WeatherInfo:
        try:
            lat, lon = cls.get_coordinates(city)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            current = data["current_weather"]
            return WeatherInfo(
                city=city,
                temperature=current["temperature"],
                condition=cls.interpret_weather_code(current["weathercode"]),
                wind=current["windspeed"]
            )
        
        except requests.RequestException as e:
            logger.exception(f"Request failed while fetching weather info for city {city}")
            raise WeatherServiceError(f"Error fetching weather information for city {city}") from e
        
        except KeyError as e:
            logger.exception(f"Missing expected data in response while fetching weather info for city {city}")
            raise WeatherServiceError(f"Error parsing weather information for city {city}") from e
        
        except ValueError as e:
            logger.exception(f"Invalid value while processing weather info for city {city}")
            raise WeatherServiceError(f"Error processing weather information for city {city}") from e


    @classmethod
    def interpret_weather_code(cls, code: int) -> str:
        return cls.WEATHER_CODE_MAPPING.get(code, "Unknown weather condition")
