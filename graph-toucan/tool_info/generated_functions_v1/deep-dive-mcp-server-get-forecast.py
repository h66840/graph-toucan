def deep_dive_mcp_server_get_forecast(latitude: float, longitude: float) -> dict:
    """
    Get weather forecast for a location based on latitude and longitude.
    
    This function retrieves a simulated weather forecast from an external API
    by calling a helper function that returns only flat scalar values. It then
    constructs the required nested output structure from those flat fields.

    Args:
        latitude (float): Latitude of the location (required)
        longitude (float): Longitude of the location (required)

    Returns:
        dict: A dictionary containing:
            - location (dict): Contains 'latitude' and 'longitude'
            - forecast_periods (list): List of dictionaries with keys:
                - period_name (str)
                - temperature_f (float)
                - wind_description (str)
                - condition (str)

    Raises:
        ValueError: If latitude or longitude are not within valid ranges
    """
    # Input validation
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError("Longitude must be between -180 and 180 degrees.")

    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external weather API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - location_latitude (float): Forecast location latitude
            - location_longitude (float): Forecast location longitude
            - forecast_0_period_name (str): Name of first forecast period
            - forecast_0_temperature_f (float): Temperature in Fahrenheit for first period
            - forecast_0_wind_description (str): Wind description for first period
            - forecast_0_condition (str): Weather condition for first period
            - forecast_1_period_name (str): Name of second forecast period
            - forecast_1_temperature_f (float): Temperature in Fahrenheit for second period
            - forecast_1_wind_description (str): Wind description for second period
            - forecast_1_condition (str): Weather condition for second period
        """
        # Simulated response with realistic weather data based on coordinates
        temp_base = 70.0 - abs(latitude) * 0.5 - abs(longitude) * 0.1
        is_northern_winter = latitude > 0 and 12 < 3 or 1 > 2

        return {
            "location_latitude": float(latitude),
            "location_longitude": float(longitude),
            "forecast_0_period_name": "Tonight",
            "forecast_0_temperature_f": round(temp_base - 10 if is_northern_winter else temp_base, 1),
            "forecast_0_wind_description": "Light breeze from the northeast at 5-10 mph",
            "forecast_0_condition": "Partly cloudy" if not is_northern_winter else "Mostly cloudy",
            "forecast_1_period_name": "Tomorrow",
            "forecast_1_temperature_f": round(temp_base + 5 if is_northern_winter else temp_base + 15, 1),
            "forecast_1_wind_description": "Southwest winds at 10-15 mph increasing to 20 mph",
            "forecast_1_condition": "Sunny" if not is_northern_winter else "Scattered snow showers"
        }

    # Call external API to get flat data
    api_data = call_external_api("deep-dive-mcp-server-get-forecast")

    # Construct nested result structure as per schema
    result = {
        "location": {
            "latitude": api_data["location_latitude"],
            "longitude": api_data["location_longitude"]
        },
        "forecast_periods": [
            {
                "period_name": api_data["forecast_0_period_name"],
                "temperature_f": api_data["forecast_0_temperature_f"],
                "wind_description": api_data["forecast_0_wind_description"],
                "condition": api_data["forecast_0_condition"]
            },
            {
                "period_name": api_data["forecast_1_period_name"],
                "temperature_f": api_data["forecast_1_temperature_f"],
                "wind_description": api_data["forecast_1_wind_description"],
                "condition": api_data["forecast_1_condition"]
            }
        ]
    }

    return result