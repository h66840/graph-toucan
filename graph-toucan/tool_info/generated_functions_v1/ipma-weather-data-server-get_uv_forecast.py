from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching UV forecast data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_date (str): Date of the UV forecast in YYYY-MM-DD format
        - location_0_name (str): Name of the first location
        - location_0_uv_index (int): UV index value for the first location
        - location_0_intensity_level (str): Intensity level description for the first location
        - location_0_time_period (str): Time period for the first location's forecast
        - location_1_name (str): Name of the second location
        - location_1_uv_index (int): UV index value for the second location
        - location_1_intensity_level (str): Intensity level description for the second location
        - location_1_time_period (str): Time period for the second location's forecast
    """
    return {
        "forecast_date": "2023-12-05",
        "location_0_name": "Lisboa",
        "location_0_uv_index": 6,
        "location_0_intensity_level": "Alto",
        "location_0_time_period": "12:00-14:00",
        "location_1_name": "Porto",
        "location_1_uv_index": 5,
        "location_1_intensity_level": "Moderado",
        "location_1_time_period": "13:00-15:00"
    }

def ipma_weather_data_server_get_uv_forecast() -> Dict[str, Any]:
    """
    Obter previsão do índice UV.
    
    Returns:
        Dict containing UV forecast information with the following structure:
        - forecast_date (str): Date of the UV forecast in YYYY-MM-DD format
        - locations (List[Dict]): List of locations with UV index details, each containing:
          - name (str): Location name
          - uv_index (int): UV index value
          - intensity_level (str): Intensity level description
          - time_period (str): Time period for the forecast
    
    Raises:
        KeyError: If expected fields are missing from the API response
        ValueError: If required field values are invalid
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("ipma-weather-data-server-get_uv_forecast")
        
        # Validate required fields
        if not api_data or "forecast_date" not in api_data:
            raise KeyError("Missing required field 'forecast_date' in API response")
            
        # Construct locations list from indexed fields
        locations = []
        
        for i in range(2):  # Process 2 locations (0 and 1)
            location_key = f"location_{i}_name"
            if location_key not in api_data:
                continue
                
            location = {
                "name": api_data[f"location_{i}_name"],
                "uv_index": api_data[f"location_{i}_uv_index"],
                "intensity_level": api_data[f"location_{i}_intensity_level"],
                "time_period": api_data[f"location_{i}_time_period"]
            }
            locations.append(location)
        
        # Construct final result matching output schema
        result = {
            "forecast_date": api_data["forecast_date"],
            "locations": locations
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Missing expected data field: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to process UV forecast data: {str(e)}")