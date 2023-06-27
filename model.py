"""
This module converts the outputs come from live requests
into more readible formatted shapes.
"""

from datetime import datetime as dt
from dataclasses import dataclass, field
from typing import Final, Dict


@dataclass
class WeatherFiveDays:
    date: dt
    details: dict
    temp: str
    weather: list[dict]
    description: str

    def __str__(self):
        return f'[{self.date:%H:%M}] {self.temp:.1f}°C ({self.description})'

@dataclass
class CurrentWeather:
    temp: float
    temp_min: float
    temp_max: float
    feels_like: float
    humidity: float
    wind: dict

    def __str__(self):
        return f'{self.temp:.1f}°C-{self.temp_min:.1f}°C-{self.temp_max:.1f}°C-{self.feels_like:.1f}°C-{self.humidity}%-{self.wind} m/s'

@dataclass
class AirQuality:
    score: int
    AIR_QUALITY_INDEX: Dict[str, str] = field(default_factory=lambda: {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    })

    def __str__(self):
        return str(f"{self.score}/5 ({self.AIR_QUALITY_INDEX[self.score]})")
