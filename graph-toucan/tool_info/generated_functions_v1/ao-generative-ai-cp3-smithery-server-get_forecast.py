from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather forecast.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_0_date (str): Date of the first forecast day (YYYY-MM-DD)
        - forecast_0_min_temp_celsius (float): Minimum temperature in Celsius for the first day
        - forecast_0_max_temp_celsius (float): Maximum temperature in Celsius for the first day
        - forecast_0_precipitation_probability_percent (float): Precipitation probability for the first day
        - forecast_0_wind_direction (str): Wind direction for the first day
        - forecast_1_date (str): Date of the second forecast day (YYYY-MM-DD)
        - forecast_1_min_temp_celsius (float): Minimum temperature in Celsius for the second day
        - forecast_1_max_temp_celsius (float): Maximum temperature in Celsius for the second day
        - forecast_1_precipitation_probability_percent (float): Precipitation probability for the second day
        - forecast_1_wind_direction (str): Wind direction for the second day
        - forecast_2_date (str): Date of the third forecast day (YYYY-MM-DD)
        - forecast_2_min_temp_celsius (float): Minimum temperature in Celsius for the third day
        - forecast_2_max_temp_celsius (float): Maximum temperature in Celsius for the third day
        - forecast_2_precipitation_probability_percent (float): Precipitation probability for the third day
        - forecast_2_wind_direction (str): Wind direction for the third day
        - forecast_3_date (str): Date of the fourth forecast day (YYYY-MM-DD)
        - forecast_3_min_temp_celsius (float): Minimum temperature in Celsius for the fourth day
        - forecast_3_max_temp_celsius (float): Maximum temperature in Celsius for the fourth day
        - forecast_3_precipitation_probability_percent (float): Precipitation probability for the fourth day
        - forecast_3_wind_direction (str): Wind direction for the fourth day
        - forecast_4_date (str): Date of the fifth forecast day (YYYY-MM-DD)
        - forecast_4_min_temp_celsius (float): Minimum temperature in Celsius for the fifth day
        - forecast_4_max_temp_celsius (float): Maximum temperature in Celsius for the fifth day
        - forecast_4_precipitation_probability_percent (float): Precipitation probability for the fifth day
        - forecast_4_wind_direction (str): Wind direction for the fifth day
        - error (str): Error message if any, otherwise empty string
    """
    return {
        "forecast_0_date": "2023-10-01",
        "forecast_0_min_temp_celsius": 15.0,
        "forecast_0_max_temp_celsius": 22.0,
        "forecast_0_precipitation_probability_percent": 10.0,
        "forecast_0_wind_direction": "NW",
        "forecast_1_date": "2023-10-02",
        "forecast_1_min_temp_celsius": 16.0,
        "forecast_1_max_temp_celsius": 23.0,
        "forecast_1_precipitation_probability_percent": 20.0,
        "forecast_1_wind_direction": "W",
        "forecast_2_date": "2023-10-03",
        "forecast_2_min_temp_celsius": 14.0,
        "forecast_2_max_temp_celsius": 20.0,
        "forecast_2_precipitation_probability_percent": 80.0,
        "forecast_2_wind_direction": "SW",
        "forecast_3_date": "2023-10-04",
        "forecast_3_min_temp_celsius": 13.0,
        "forecast_3_max_temp_celsius": 19.0,
        "forecast_3_precipitation_probability_percent": 90.0,
        "forecast_3_wind_direction": "S",
        "forecast_4_date": "2023-10-05",
        "forecast_4_min_temp_celsius": 15.0,
        "forecast_4_max_temp_celsius": 21.0,
        "forecast_4_precipitation_probability_percent": 40.0,
        "forecast_4_wind_direction": "SE",
        "error": ""
    }

def ao_generative_ai_cp3_smithery_server_get_forecast(city: str) -> Dict[str, Any]:
    """
    Get 5-day weather forecast for a Portuguese city.

    Args:
        city (str): Name of the city (e.g. Lisboa, Porto, Faro)

    Returns:
        Dict containing:
        - forecast (List[Dict]): list of daily forecast entries with keys:
            'date' (str), 'min_temp_celsius' (float), 'max_temp_celsius' (float),
            'precipitation_probability_percent' (float), 'wind_direction' (str)
        - error (str): error message if the city could not be found or data is unavailable
    """
    if not city or not isinstance(city, str):
        return {
            "forecast": [],
            "error": "Invalid city name provided."
        }

    # Simulate external API call
    api_data = call_external_api("ao-generative-ai-cp3-smithery-server-get_forecast")

    # Check for error from API
    if api_data.get("error"):
        return {
            "forecast": [],
            "error": api_data["error"]
        }

    # Construct forecast list from flattened API response
    forecast = []
    for i in range(5):
        entry = {
            "date": api_data.get(f"forecast_{i}_date", ""),
            "min_temp_celsius": api_data.get(f"forecast_{i}_min_temp_celsius", 0.0),
            "max_temp_celsius": api_data.get(f"forecast_{i}_max_temp_celsius", 0.0),
            "precipitation_probability_percent": api_data.get(f"forecast_{i}_precipitation_probability_percent", 0.0),
            "wind_direction": api_data.get(f"forecast_{i}_wind_direction", "")
        }
        forecast.append(entry)

    return {
        "forecast": forecast,
        "error": ""
    }