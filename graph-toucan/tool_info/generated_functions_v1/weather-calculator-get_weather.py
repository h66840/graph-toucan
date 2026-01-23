def weather_calculator_get_weather(city: str) -> dict:
    """
    Get current weather information for a city.
    
    Args:
        city (str): City name (e.g., "Istanbul", "London", "New York")
    
    Returns:
        dict: Weather information with the following structure:
            - location (str): full location name including city and country, e.g., "Tokyo, Japan"
            - city (str): name of the city for which weather is provided
            - country (str): name of the country corresponding to the city
            - temperature_celsius (float): current temperature in degrees Celsius
            - temperature_fahrenheit (float): current temperature in degrees Fahrenheit
            - condition (str): textual description of current weather condition, e.g., "Sunny", "Partly cloudy"
            - humidity (int): relative humidity percentage
            - wind_speed_kmh (float): wind speed in kilometers per hour
            - feels_like_celsius (float): apparent temperature in degrees Celsius
            - feels_like_fahrenheit (float): apparent temperature in degrees Fahrenheit
    
    Raises:
        ValueError: If city is empty or not a string
    """
    if not city or not isinstance(city, str):
        raise ValueError("City must be a non-empty string")

    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - location (str): Full location name including city and country
            - city (str): Name of the city
            - country (str): Name of the country
            - temperature_celsius (float): Temperature in Celsius
            - temperature_fahrenheit (float): Temperature in Fahrenheit
            - condition (str): Weather condition description
            - humidity (int): Relative humidity percentage
            - wind_speed_kmh (float): Wind speed in km/h
            - feels_like_celsius (float): Apparent temperature in Celsius
            - feels_like_fahrenheit (float): Apparent temperature in Fahrenheit
        """
        return {
            "location": f"{city}, Country",
            "city": city,
            "country": "Country",
            "temperature_celsius": 20.5,
            "temperature_fahrenheit": 68.9,
            "condition": "Partly cloudy",
            "humidity": 65,
            "wind_speed_kmh": 12.3,
            "feels_like_celsius": 22.0,
            "feels_like_fahrenheit": 71.6
        }

    try:
        api_data = call_external_api("weather-calculator-get_weather")
        
        result = {
            "location": api_data["location"],
            "city": api_data["city"],
            "country": api_data["country"],
            "temperature_celsius": api_data["temperature_celsius"],
            "temperature_fahrenheit": api_data["temperature_fahrenheit"],
            "condition": api_data["condition"],
            "humidity": api_data["humidity"],
            "wind_speed_kmh": api_data["wind_speed_kmh"],
            "feels_like_celsius": api_data["feels_like_celsius"],
            "feels_like_fahrenheit": api_data["feels_like_fahrenheit"]
        }
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve weather data: {str(e)}")