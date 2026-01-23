from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather forecast data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - city (str): Name of the city for which weather forecast is provided
        - coordinates_latitude (float): Latitude of the city
        - coordinates_longitude (float): Longitude of the city
        - last_updated (str): Timestamp of the last update in ISO 8601 format
        - forecast_0_date (str): Date of the first forecast day (YYYY-MM-DD)
        - forecast_0_min_temperature (float): Minimum temperature on first day
        - forecast_0_max_temperature (float): Maximum temperature on first day
        - forecast_0_conditions (str): Weather conditions on first day
        - forecast_0_precipitation_probability (int): Precipitation probability on first day (%)
        - forecast_0_wind_direction (str): Wind direction on first day
        - forecast_1_date (str): Date of the second forecast day (YYYY-MM-DD)
        - forecast_1_min_temperature (float): Minimum temperature on second day
        - forecast_1_max_temperature (float): Maximum temperature on second day
        - forecast_1_conditions (str): Weather conditions on second day
        - forecast_1_precipitation_probability (int): Precipitation probability on second day (%)
        - forecast_1_wind_direction (str): Wind direction on second day
    """
    # Generate realistic mock data based on tool name
    if tool_name == "ipma-weather-data-server-get_weather_forecast":
        now = datetime.now()
        return {
            "city": "Lisboa",
            "coordinates_latitude": 38.7223,
            "coordinates_longitude": -9.1393,
            "last_updated": now.isoformat(),
            "forecast_0_date": (now).strftime("%Y-%m-%d"),
            "forecast_0_min_temperature": round(random.uniform(12, 18), 1),
            "forecast_0_max_temperature": round(random.uniform(20, 28), 1),
            "forecast_0_conditions": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"]),
            "forecast_0_precipitation_probability": random.randint(0, 80),
            "forecast_0_wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"]),
            "forecast_1_date": (now + timedelta(days=1)).strftime("%Y-%m-%d"),
            "forecast_1_min_temperature": round(random.uniform(12, 18), 1),
            "forecast_1_max_temperature": round(random.uniform(20, 28), 1),
            "forecast_1_conditions": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"]),
            "forecast_1_precipitation_probability": random.randint(0, 80),
            "forecast_1_wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        }
    return {}


def ipma_weather_data_server_get_weather_forecast(city: str, days: Optional[int] = None) -> Dict[str, Any]:
    """
    Obter previsão meteorológica para uma cidade específica em Portugal.

    Args:
        city (str): Nome da cidade (ex: Lisboa, Porto, Coimbra, Faro, etc.)
        days (Optional[int]): Número de dias de previsão (máximo 10). Default é 2.

    Returns:
        Dict[str, Any]: Dicionário contendo:
            - city (str): nome da cidade
            - coordinates (Dict): com 'latitude' e 'longitude'
            - last_updated (str): timestamp da última atualização no formato ISO 8601
            - forecast (List[Dict]): lista com previsões diárias contendo:
                - date (str): data da previsão (YYYY-MM-DD)
                - min_temperature (float): temperatura mínima
                - max_temperature (float): temperatura máxima
                - conditions (str): condições meteorológicas
                - precipitation_probability (int): probabilidade de precipitação (%)
                - wind_direction (str): direção do vento

    Raises:
        ValueError: Se a cidade não for fornecida ou se 'days' não estiver entre 1 e 10.
    """
    # Input validation
    if not city or not city.strip():
        raise ValueError("City name is required.")
    
    city = city.strip()
    
    if days is not None:
        if not isinstance(days, int):
            raise ValueError("Days must be an integer.")
        if days < 1 or days > 10:
            raise ValueError("Days must be between 1 and 10.")
    else:
        days = 2  # default value
    
    # Call external API to get flat data
    api_data = call_external_api("ipma-weather-data-server-get_weather_forecast")
    
    # Override city in response with input city
    api_data["city"] = city
    
    # Construct nested output structure manually
    result = {
        "city": api_data["city"],
        "coordinates": {
            "latitude": api_data["coordinates_latitude"],
            "longitude": api_data["coordinates_longitude"]
        },
        "last_updated": api_data["last_updated"],
        "forecast": []
    }
    
    # Build forecast list from indexed fields
    for i in range(min(days, 2)):  # Only 2 items available in mock data
        prefix = f"forecast_{i}_"
        result["forecast"].append({
            "date": api_data[f"{prefix}date"],
            "min_temperature": api_data[f"{prefix}min_temperature"],
            "max_temperature": api_data[f"{prefix}max_temperature"],
            "conditions": api_data[f"{prefix}conditions"],
            "precipitation_probability": api_data[f"{prefix}precipitation_probability"],
            "wind_direction": api_data[f"{prefix}wind_direction"]
        })
    
    # If more than 2 days requested, extend with generated data
    base_date = datetime.fromisoformat(api_data["forecast_0_date"])
    for i in range(2, days):
        next_date = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        result["forecast"].append({
            "date": next_date,
            "min_temperature": round(random.uniform(12, 18), 1),
            "max_temperature": round(random.uniform(20, 28), 1),
            "conditions": random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Light Rain"]),
            "precipitation_probability": random.randint(0, 80),
            "wind_direction": random.choice(["N", "NE", "E", "SE", "S", "SW", "W", "NW"])
        })
    
    return result