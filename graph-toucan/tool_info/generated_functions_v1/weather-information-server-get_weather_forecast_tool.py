from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather forecast data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - city (str): Name of the city
        - country (str): Country where the city is located
        - region (str): Administrative region or state
        - forecast_0_date (str): Date of first forecast day (YYYY-MM-DD)
        - forecast_0_temp_c (float): Temperature in Celsius for first day
        - forecast_0_temp_f (float): Temperature in Fahrenheit for first day
        - forecast_0_condition (str): Weather condition description for first day
        - forecast_0_icon (str): URL to weather icon for first day
        - forecast_0_rain_chance (int): Chance of rain percentage for first day
        - forecast_0_snow_chance (int): Chance of snow percentage for first day
        - forecast_0_wind_kph (float): Wind speed in kph for first day
        - forecast_0_humidity (int): Average humidity percentage for first day
        - forecast_0_uv_index (float): UV index for first day
        - forecast_1_date (str): Date of second forecast day (YYYY-MM-DD)
        - forecast_1_temp_c (float): Temperature in Celsius for second day
        - forecast_1_temp_f (float): Temperature in Fahrenheit for second day
        - forecast_1_condition (str): Weather condition description for second day
        - forecast_1_icon (str): URL to weather icon for second day
        - forecast_1_rain_chance (int): Chance of rain percentage for second day
        - forecast_1_snow_chance (int): Chance of snow percentage for second day
        - forecast_1_wind_kph (float): Wind speed in kph for second day
        - forecast_1_humidity (int): Average humidity percentage for second day
        - forecast_1_uv_index (float): UV index for second day
    """
    base_date = datetime.now()
    cities_data = {
        "London": ("United Kingdom", "England"),
        "New York": ("United States", "New York"),
        "Tokyo": ("Japan", "Kanto"),
        "Sydney": ("Australia", "New South Wales"),
        "Paris": ("France", "Île-de-France")
    }
    
    # Default to generic data if city not in our mock database
    country, region = cities_data.get(tool_name.split("-")[-1].title(), ("Unknown", "Unknown"))
    
    def random_weather_condition():
        conditions = ["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Moderate rain", "Thunderstorms", "Snow", "Fog"]
        return random.choice(conditions)
    
    def condition_to_icon(condition: str) -> str:
        icons = {
            "Sunny": "https://example.com/icons/sunny.png",
            "Partly cloudy": "https://example.com/icons/partly_cloudy.png",
            "Cloudy": "https://example.com/icons/cloudy.png",
            "Light rain": "https://example.com/icons/light_rain.png",
            "Moderate rain": "https://example.com/icons/rain.png",
            "Thunderstorms": "https://example.com/icons/thunderstorm.png",
            "Snow": "https://example.com/icons/snow.png",
            "Fog": "https://example.com/icons/fog.png"
        }
        return icons.get(condition, "https://example.com/icons/unknown.png")
    
    # Generate two days of forecast data
    data = {}
    for i in range(2):
        date_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        temp_c = round(random.uniform(0, 35), 1)
        temp_f = round(temp_c * 9/5 + 32, 1)
        condition = random_weather_condition()
        rain_chance = random.randint(0, 100) if "rain" in condition.lower() else random.randint(0, 30)
        snow_chance = random.randint(20, 80) if "snow" in condition.lower() else 0
        wind_kph = round(random.uniform(5, 40), 1)
        humidity = random.randint(40, 95)
        uv_index = round(random.uniform(1, 11), 1)
        
        data[f"forecast_{i}_date"] = date_str
        data[f"forecast_{i}_temp_c"] = temp_c
        data[f"forecast_{i}_temp_f"] = temp_f
        data[f"forecast_{i}_condition"] = condition
        data[f"forecast_{i}_icon"] = condition_to_icon(condition)
        data[f"forecast_{i}_rain_chance"] = rain_chance
        data[f"forecast_{i}_snow_chance"] = snow_chance
        data[f"forecast_{i}_wind_kph"] = wind_kph
        data[f"forecast_{i}_humidity"] = humidity
        data[f"forecast_{i}_uv_index"] = uv_index
    
    data["city"] = tool_name.split("-")[-1].title()
    data["country"] = country
    data["region"] = region
    
    return data

def weather_information_server_get_weather_forecast_tool(city: str, days: Optional[int] = 3) -> Dict[str, Any]:
    """
    Get weather forecast for a specific city.
    
    Args:
        city (str): Name of the city to get forecast for
        days (int, optional): Number of days to forecast (1-10, default: 3)
    
    Returns:
        Dict containing:
        - city (str): name of the city for which weather forecast is provided
        - country (str): country where the city is located
        - region (str): administrative region or state within the country
        - forecast (List[Dict]): list of daily forecast entries with date, temperature values (C and F),
          weather condition, icon URL, precipitation chances (rain/snow), wind speed (kph),
          average humidity, and UV index
    
    Raises:
        ValueError: If days is not between 1 and 10
    """
    # Input validation
    if not city or not city.strip():
        raise ValueError("City name is required")
    
    if days is None:
        days = 3
    elif not isinstance(days, int) or days < 1 or days > 10:
        raise ValueError("Days must be an integer between 1 and 10")
    
    # Call external API to get data (with flattened structure)
    api_data = call_external_api("weather-information-server-get_weather_forecast_tool")
    
    # Construct the forecast list from indexed fields
    forecast = []
    for i in range(min(2, days)):  # We only have 2 days of mock data
        forecast_entry = {
            "date": api_data[f"forecast_{i}_date"],
            "temp_c": api_data[f"forecast_{i}_temp_c"],
            "temp_f": api_data[f"forecast_{i}_temp_f"],
            "condition": api_data[f"forecast_{i}_condition"],
            "icon": api_data[f"forecast_{i}_icon"],
            "rain_chance": api_data[f"forecast_{i}_rain_chance"],
            "snow_chance": api_data[f"forecast_{i}_snow_chance"],
            "wind_kph": api_data[f"forecast_{i}_wind_kph"],
            "humidity": api_data[f"forecast_{i}_humidity"],
            "uv_index": api_data[f"forecast_{i}_uv_index"]
        }
        forecast.append(forecast_entry)
    
    # For additional days beyond our mock data, extrapolate from last day
    if days > 2:
        last_forecast = forecast[-1] if forecast else {}
        for i in range(2, days):
            future_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            # Slightly modify the last forecast values for variation
            variation = random.uniform(-3, 3)
            temp_c = max(-10, min(40, last_forecast["temp_c"] + variation))
            temp_f = round(temp_c * 9/5 + 32, 1)
            
            # Randomly change condition with some probability
            if random.random() < 0.3:
                conditions = ["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Moderate rain", "Thunderstorms"]
                condition = random.choice(conditions)
            else:
                condition = last_forecast["condition"]
            
            forecast_entry = {
                "date": future_date,
                "temp_c": round(temp_c, 1),
                "temp_f": temp_f,
                "condition": condition,
                "icon": ("https://example.com/icons/sunny.png" if "sun" in condition.lower() else
                        "https://example.com/icons/cloudy.png" if "cloud" in condition.lower() else
                        "https://example.com/icons/rain.png"),
                "rain_chance": random.randint(0, 100) if "rain" in condition.lower() else random.randint(0, 30),
                "snow_chance": random.randint(20, 80) if "snow" in condition.lower() else 0,
                "wind_kph": round(random.uniform(5, 40), 1),
                "humidity": random.randint(40, 95),
                "uv_index": round(random.uniform(1, 11), 1)
            }
            forecast.append(forecast_entry)
    
    return {
        "city": api_data["city"],
        "country": api_data["country"],
        "region": api_data["region"],
        "forecast": forecast
    }