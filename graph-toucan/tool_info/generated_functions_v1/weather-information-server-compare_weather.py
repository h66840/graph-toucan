from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather comparison data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - metric (str): The weather metric being compared (e.g., temperature)
        - city_0_name (str): First city name
        - city_0_temperature (str): Temperature of first city
        - city_0_humidity (str): Humidity of first city
        - city_0_wind (str): Wind speed of first city
        - city_1_name (str): Second city name
        - city_1_temperature (str): Temperature of second city
        - city_1_humidity (str): Humidity of second city
        - city_1_wind (str): Wind speed of second city
    """
    return {
        "metric": "temperature",
        "city_0_name": "Beijing",
        "city_0_temperature": "25°C",
        "city_0_humidity": "60%",
        "city_0_wind": "15 km/h",
        "city_1_name": "Shanghai",
        "city_1_temperature": "28°C",
        "city_1_humidity": "75%",
        "city_1_wind": "10 km/h"
    }

def weather_information_server_compare_weather(cities: List[str], metric: Optional[str] = None) -> Dict[str, Any]:
    """
    Compare weather between multiple cities.
    
    Args:
        cities (List[str]): List of city names to compare weather for.
        metric (Optional[str]): The weather metric to focus on (e.g., temperature, humidity).
                               If not provided, defaults to 'temperature'.
    
    Returns:
        Dict containing:
        - metric (str): The weather metric being compared across cities.
        - cities (List[Dict]): List of city weather data, each with:
            - city (str): City name
            - temperature (str): Temperature value
            - humidity (str): Humidity percentage
            - wind (str): Wind speed
    """
    if not cities or len(cities) == 0:
        raise ValueError("At least one city must be provided for comparison.")
    
    # Fetch simulated external data
    api_data = call_external_api("weather-information-server-compare_weather")
    
    # Use provided metric or fallback to default from API
    result_metric = metric if metric is not None else api_data["metric"]
    
    # Construct list of city weather data
    city_weather_list = []
    
    # Process first city
    city_weather_list.append({
        "city": api_data["city_0_name"],
        "temperature": api_data["city_0_temperature"],
        "humidity": api_data["city_0_humidity"],
        "wind": api_data["city_0_wind"]
    })
    
    # Process second city
    city_weather_list.append({
        "city": api_data["city_1_name"],
        "temperature": api_data["city_1_temperature"],
        "humidity": api_data["city_1_humidity"],
        "wind": api_data["city_1_wind"]
    })
    
    # Return structured response matching output schema
    return {
        "metric": result_metric,
        "cities": city_weather_list
    }