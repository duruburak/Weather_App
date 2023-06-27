"""
This module is responsible for API interaction.
"""

import requests

from model import AirQuality, CurrentWeather, Final, WeatherFiveDays, dt


# Constants
API_KEY: Final[str] = <<YOUR_API_KEY>>
BASE_URL: Final[str] = 'https://api.openweathermap.org/data/2.5/forecast'
CURRENT_WEATHER_URL: Final[str] = "https://api.openweathermap.org/data/2.5/weather"
POLLUTION_URL: Final[str] = "http://api.openweathermap.org/data/2.5/air_pollution"
GEOCODING_URL: Final[str] = "http://api.openweathermap.org/geo/1.0/direct"


def get_five_days_weather(city_name: str) -> dict:
    """Gets the five days weather data from the weather api"""
    parameters: dict = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    request = requests.get(url=BASE_URL, params=parameters, timeout=15)
    data: dict = request.json()

    return data


def get_five_days_weather_details(weather: dict) -> list[WeatherFiveDays]:
    """
    Takes the five days weather json and turns it into
    a nice list of WeatherFiveDays objects
    """

    days: list[dict] = weather.get('list')

    # Try to add the info we want to our list_of_weather
    list_of_weather: list[WeatherFiveDays] = []
    for day in days:
        w: WeatherFiveDays = WeatherFiveDays(date=dt.fromtimestamp(day.get('dt')),
                             details=(details := day.get('main')),
                             temp=details.get('temp'),
                             weather=(weather := day.get('weather')),
                             description=weather[0].get('description'))
        list_of_weather.append(w)

    return list_of_weather


def get_current_weather(city_name: str) -> dict:
    """Gets the current weather data from the weather api"""
    parameters: dict = {'q': city_name, 'appid': API_KEY, 'units': 'metric'}
    request = requests.get(url=CURRENT_WEATHER_URL, params=parameters, timeout=15)
    data: dict = request.json()

    return data


def get_current_weather_details(weather: dict) -> CurrentWeather:
    """Takes the current weather json and turns it into a nice CurrentWeather object"""
    w: CurrentWeather = CurrentWeather(temp = weather["main"].get('temp', " "),
                            temp_min = weather["main"].get('temp_min', " "),
                            temp_max = weather["main"].get('temp_max', " "),
                            feels_like = weather["main"].get('feels_like', " "),
                            humidity = weather["main"].get('humidity', " "),
                            wind = weather["wind"].get('speed', " ")
                        )

    return w


def location_to_geo_coords(location: str) -> list:
    """Converts the input location into geographical coordinates (latitude and longitude)"""
    parameters: dict = {'q': location, 'appid': API_KEY}
    request = requests.get(url=GEOCODING_URL, params=parameters, timeout=15)
    data: dict = request.json()

    return data[0]


def get_current_air_pollution(latitude: float, longitude: float) -> dict:
    """Gets the current air pollution data from the weather api"""

    parameters: dict = {'lat': latitude, 'lon': longitude, 'appid': API_KEY}
    request = requests.get(url=POLLUTION_URL, params=parameters, timeout=15)
    data: dict = request.json()

    return data


def get_current_air_pollution_details(weather: dict) -> AirQuality:
    """Takes the air pollution weather json and turns it into a nice AirQuality object"""
    w: AirQuality = AirQuality(weather["list"][0]["main"].get('aqi', " "))

    return w
