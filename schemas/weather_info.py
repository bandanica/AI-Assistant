# models/weather_info.py

from pydantic import BaseModel
from typing import Optional

class WeatherInfo(BaseModel):
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
            "Based on this weather, what should I wear today? Provide a brief and practical outfit recommendation. Recommendation should be based just on the wather conditions."
        )
