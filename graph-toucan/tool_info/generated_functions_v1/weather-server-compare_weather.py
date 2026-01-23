from typing import List, Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - metric (str): the weather metric used for comparison (e.g., "temperature")
        - city_0_name (str): First city name
        - city_0_temperature (str): Temperature of first city
        - city_0_humidity (str): Humidity of first city
        - city_0_wind (str): Wind condition of first city
        - city_1_name (str): Second city name
        - city_1_temperature (str): Temperature of second city
        - city_1_humidity (str): Humidity of second city
        - city_1_wind (str): Wind condition of second city
    """
    return {
        "metric": "temperature",
        "city_0_name": "New York",
        "city_0_temperature": "23°C",
        "city_0_humidity": "60%",
        "city_0_wind": "15 km/h",
        "city_1_name": "Los Angeles",
        "city_1_temperature": "28°C",
        "city_1_humidity": "45%",
        "city_1_wind": "10 km/h"
    }

def weather_server_compare_weather(cities: List[str], metric: Optional[str] = None) -> Dict[str, Any]:
    """
    Compare weather between multiple cities.
    
    Args:
        cities (List[str]): List of city names to compare weather for.
        metric (Optional[str]): The weather metric to use for comparison (e.g., "temperature").
                              If not provided, defaults to "temperature".
    
    Returns:
        Dict containing:
            - metric (str): the weather metric used for comparison
            - cities (List[Dict]): list of city weather data, each containing 'city' (str),
              'temperature' (str), 'humidity' (str), and 'wind' (str) fields
    
    Raises:
        ValueError: If cities list is empty.
    """
    if not cities:
        raise ValueError("Cities list cannot be empty.")
    
    # Call external API to get simulated data
    api_data = call_external_api("weather-server-compare_weather")
    
    # Use provided metric or fallback to API default
    result_metric = metric if metric is not None else api_data["metric"]
    
    # Construct cities list from indexed API fields
    result_cities = []
    
    for i in range(2):  # We expect 2 cities based on API response structure
        city_key = f"city_{i}_name"
        temp_key = f"city_{i}_temperature"
        humidity_key = f"city_{i}_humidity"
        wind_key = f"city_{i}_wind"
        
        if city_key in api_data:
            result_cities.append({
                "city": api_data[city_key],
                "temperature": api_data[temp_key],
                "humidity": api_data[humidity_key],
                "wind": api_data[wind_key]
            })
    
    return {
        "metric": result_metric,
        "cities": result_cities
    }