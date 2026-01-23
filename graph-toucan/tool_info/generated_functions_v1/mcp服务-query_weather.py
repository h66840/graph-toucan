from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external weather API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - location (str): Full location string including city and country
        - temperature_celsius (float): Current temperature in degrees Celsius
        - humidity (float): Relative humidity percentage
        - wind_speed_m_s (float): Wind speed in meters per second
        - weather_condition (str): Textual description of current weather
        - city (str): Name of the city queried
        - country (str): ISO country code or full country name
    """
    return {
        "location": "New York, US",
        "temperature_celsius": 23.5,
        "humidity": 60.0,
        "wind_speed_m_s": 3.2,
        "weather_condition": "晴",
        "city": "New York",
        "country": "US"
    }

def mcp服务_query_weather(city: str) -> Dict[str, Any]:
    """
    查询指定城市的今日天气信息。
    
    :param city: 城市名称（需使用英文）
    :return: 格式化后的天气信息，包含位置、温度、湿度、风速、天气状况等
    
    Raises:
        ValueError: 当城市名称为空或非字符串类型时抛出异常
    """
    # 输入验证
    if not city:
        raise ValueError("City name cannot be empty.")
    if not isinstance(city, str):
        raise ValueError("City name must be a string.")

    # 调用外部API获取数据（模拟）
    api_data = call_external_api("mcp服务-query_weather")

    # 构造符合输出schema的嵌套结构
    result = {
        "location": api_data["location"],
        "temperature_celsius": api_data["temperature_celsius"],
        "humidity": api_data["humidity"],
        "wind_speed_m_s": api_data["wind_speed_m_s"],
        "weather_condition": api_data["weather_condition"],
        "city": api_data["city"],
        "country": api_data["country"]
    }

    return result