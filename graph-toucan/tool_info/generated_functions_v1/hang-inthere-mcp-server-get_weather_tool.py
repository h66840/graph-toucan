from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - city (str): Name of the city with country code
        - condition (str): Current weather condition in natural language
        - temperature_celsius (float): Temperature in degrees Celsius
        - humidity_percent (int): Relative humidity as percentage
        - wind_speed_mps (float): Wind speed in meters per second
    """
    return {
        "city": "Beijing, CN",
        "condition": "晴",
        "temperature_celsius": 26.94,
        "humidity_percent": 45,
        "wind_speed_mps": 2.24
    }

def hang_inthere_mcp_server_get_weather_tool(city: str) -> Dict[str, Any]:
    """
    获取城市的天气信息
    :param city: 城市名称（需要使用英文，如 beijing）
    :return: 天气数据字典；若发生错误，返回包含error信息的字典
    """
    try:
        if not city or not isinstance(city, str):
            return {"error": "Invalid city name provided. City must be a non-empty string."}
        
        # Call the external API helper to get simulated data
        api_data = call_external_api("hang-inthere-mcp-server-get_weather_tool")
        
        # Construct the result matching the required output schema
        result = {
            "city": api_data["city"],
            "condition": api_data["condition"],
            "temperature_celsius": api_data["temperature_celsius"],
            "humidity_percent": api_data["humidity_percent"],
            "wind_speed_mps": api_data["wind_speed_mps"]
        }
        
        return result
        
    except Exception as e:
        return {"error": f"An error occurred while retrieving weather data: {str(e)}"}