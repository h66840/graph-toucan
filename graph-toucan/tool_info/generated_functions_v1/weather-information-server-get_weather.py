from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - city (str): Name of the city for which weather data is provided
        - temperature (str): Current temperature in Celsius with unit (e.g., "31°C")
        - condition (str): Current weather condition description (e.g., "Partly cloudy")
        - humidity (str): Current humidity level as a percentage with unit (e.g., "55%")
        - wind (str): Current wind speed with unit (e.g., "20 km/h")
        - forecast_0_date (str): Date of the first forecast entry
        - forecast_0_max (str): Maximum temperature of the first forecast day
        - forecast_0_min (str): Minimum temperature of the first forecast day
        - forecast_0_condition (str): Weather condition of the first forecast day
        - forecast_1_date (str): Date of the second forecast entry
        - forecast_1_max (str): Maximum temperature of the second forecast day
        - forecast_1_min (str): Minimum temperature of the second forecast day
        - forecast_1_condition (str): Weather condition of the second forecast day
    """
    return {
        "city": "Sydney",
        "temperature": "24°C",
        "condition": "Sunny",
        "humidity": "45%",
        "wind": "15 km/h",
        "forecast_0_date": "2023-10-01",
        "forecast_0_max": "26°C",
        "forecast_0_min": "18°C",
        "forecast_0_condition": "Clear sky",
        "forecast_1_date": "2023-10-02",
        "forecast_1_max": "23°C",
        "forecast_1_min": "16°C",
        "forecast_1_condition": "Partly cloudy"
    }

def weather_information_server_get_weather() -> Dict[str, Any]:
    """
    Get weather information using Open-Meteo API.
    
    Returns:
        Dict containing weather data with the following structure:
        - city (str): name of the city for which weather data is provided
        - temperature (str): current temperature in Celsius with unit (e.g., "31°C")
        - condition (str): current weather condition description (e.g., "Partly cloudy")
        - humidity (str): current humidity level as a percentage with unit (e.g., "55%")
        - wind (str): current wind speed with unit (e.g., "20 km/h")
        - forecast (List[Dict]): list of daily forecast entries, each containing:
            - date (str): date of the forecast
            - max (str): maximum temperature
            - min (str): minimum temperature
            - condition (str): weather condition description
    """
    try:
        # Call external API to get weather data
        api_data = call_external_api("weather-information-server-get_weather")
        
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
        
        # Construct final result dictionary matching output schema
        result = {
            "city": api_data["city"],
            "temperature": api_data["temperature"],
            "condition": api_data["condition"],
            "humidity": api_data["humidity"],
            "wind": api_data["wind"],
            "forecast": forecast
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields
        raise ValueError(f"Missing required data field: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve weather information: {str(e)}")