from typing import Dict, List, Any
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - city (str): Name of the city for which weather is provided
        - temperature (str): Current temperature with unit (e.g., "22°C")
        - condition (str): Current weather condition (e.g., "Sunny", "Light rain")
        - humidity (str): Humidity level with percentage (e.g., "65%")
        - wind (str): Wind speed with unit (e.g., "5 km/h")
        - forecast_0_date (str): Date of first forecast entry
        - forecast_0_max (str): Max temperature of first forecast day
        - forecast_0_min (str): Min temperature of first forecast day
        - forecast_0_condition (str): Weather condition of first forecast day
        - forecast_1_date (str): Date of second forecast entry
        - forecast_1_max (str): Max temperature of second forecast day
        - forecast_1_min (str): Min temperature of second forecast day
        - forecast_1_condition (str): Weather condition of second forecast day
    """
    return {
        "city": "Beijing",
        "temperature": "25°C",
        "condition": "Sunny",
        "humidity": "40%",
        "wind": "10 km/h",
        "forecast_0_date": "2023-10-01",
        "forecast_0_max": "28°C",
        "forecast_0_min": "18°C",
        "forecast_0_condition": "Sunny",
        "forecast_1_date": "2023-10-02",
        "forecast_1_max": "26°C",
        "forecast_1_min": "17°C",
        "forecast_1_condition": "Partly cloudy"
    }



def weather_server_get_weather(city: str, detailed: bool = False, units: str = None) -> Dict[str, Any]:
    """
    Get current weather for a city.

    Args:
        city (str): Name of the city for which weather is provided.
        detailed (bool, optional): Whether to include detailed forecast information. Defaults to False.
        units (str, optional): Temperature units (e.g., 'metric', 'imperial'). Defaults to None.

    Returns:
        Dict containing:
            - city (str): name of the city for which weather is provided
            - temperature (str): current temperature with unit (e.g., "22°C")
            - condition (str): current weather condition (e.g., "Sunny", "Light rain")
            - humidity (str): current humidity level with percentage (e.g., "65%")
            - wind (str): wind speed with unit (e.g., "5 km/h")
            - forecast (List[Dict]): list of daily forecast entries, each containing:
                - date (str): date of forecast
                - max (str): max temperature
                - min (str): min temperature
                - condition (str): weather condition
    """
    if not city or not isinstance(city, str):
        raise ValueError("City must be a non-empty string.")

    api_data = call_external_api("weather-server-get_weather")

    # Construct forecast list from indexed fields
    forecast = [
        {
            "date": api_data["forecast_0_date"],
            "max": api_data["forecast_0_max"],
            "min": api_data["forecast_0_min"],
            "condition": api_data["forecast_0_condition"]
        },
        {
            "date": api_data["forecast_1_date"],
            "max": api_data["forecast_1_max"],
            "min": api_data["forecast_1_min"],
            "condition": api_data["forecast_1_condition"]
        }
    ]

    result = {
        "city": api_data["city"],
        "temperature": api_data["temperature"],
        "condition": api_data["condition"],
        "humidity": api_data["humidity"],
        "wind": api_data["wind"],
        "forecast": forecast
    }

    # If detailed is False, limit forecast to today only
    if not detailed:
        result["forecast"] = forecast[:1]

    return result