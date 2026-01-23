from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching UV forecast data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - forecast_date_0 (str): First forecast date in YYYY-MM-DD format
        - forecast_date_1 (str): Second forecast date in YYYY-MM-DD format
        - forecast_date_2 (str): Third forecast date in YYYY-MM-DD format
        - location_0_location_id (str): First location ID
        - location_0_interval_0 (str): First time interval for first location
        - location_0_interval_1 (str): Second time interval for first location
        - location_0_uv_index_0 (int): UV index for first interval of first location
        - location_0_uv_index_1 (int): UV index for second interval of first location
        - location_0_uv_level_0 (str): UV level classification for first interval of first location
        - location_0_uv_level_1 (str): UV level classification for second interval of first location
        - location_1_location_id (str): Second location ID
        - location_1_interval_0 (str): First time interval for second location
        - location_1_interval_1 (str): Second time interval for second location
        - location_1_uv_index_0 (int): UV index for first interval of second location
        - location_1_uv_index_1 (int): UV index for second interval of second location
        - location_1_uv_level_0 (str): UV level classification for first interval of second location
        - location_1_uv_level_1 (str): UV level classification for second interval of second location
    """
    return {
        "forecast_date_0": "2023-10-05",
        "forecast_date_1": "2023-10-06",
        "forecast_date_2": "2023-10-07",
        "location_0_location_id": "LIS",
        "location_0_interval_0": "08:00-12:00",
        "location_0_interval_1": "12:00-16:00",
        "location_0_uv_index_0": 4,
        "location_0_uv_index_1": 7,
        "location_0_uv_level_0": "Moderate",
        "location_0_uv_level_1": "High",
        "location_1_location_id": "OPO",
        "location_1_interval_0": "08:00-12:00",
        "location_1_interval_1": "12:00-16:00",
        "location_1_uv_index_0": 5,
        "location_1_uv_index_1": 8,
        "location_1_uv_level_0": "Moderate",
        "location_1_uv_level_1": "Very High"
    }

def ao_generative_ai_cp3_smithery_server_uv_forecast() -> Dict[str, Any]:
    """
    Get the Ultraviolet Index (UV) forecast for Portugal for the next 3 days.
    
    Returns:
        A dictionary containing:
        - forecast_dates (List[str]): list of forecasted dates in YYYY-MM-DD format
        - locations (List[Dict]): list of locations with UV index data, each containing 
          'location_id', 'intervals' (list of time ranges), and corresponding 'uv_index' 
          values with 'level' classification
    """
    try:
        api_data = call_external_api("ao-generative-ai-cp3-smithery-server-uv_forecast")
        
        # Extract forecast dates
        forecast_dates: List[str] = [
            api_data["forecast_date_0"],
            api_data["forecast_date_1"],
            api_data["forecast_date_2"]
        ]
        
        # Construct first location data
        location_0 = {
            "location_id": api_data["location_0_location_id"],
            "intervals": [
                api_data["location_0_interval_0"],
                api_data["location_0_interval_1"]
            ],
            "uv_index": [
                {
                    "value": api_data["location_0_uv_index_0"],
                    "level": api_data["location_0_uv_level_0"]
                },
                {
                    "value": api_data["location_0_uv_index_1"],
                    "level": api_data["location_0_uv_level_1"]
                }
            ]
        }
        
        # Construct second location data
        location_1 = {
            "location_id": api_data["location_1_location_id"],
            "intervals": [
                api_data["location_1_interval_0"],
                api_data["location_1_interval_1"]
            ],
            "uv_index": [
                {
                    "value": api_data["location_1_uv_index_0"],
                    "level": api_data["location_1_uv_level_0"]
                },
                {
                    "value": api_data["location_1_uv_index_1"],
                    "level": api_data["location_1_uv_level_1"]
                }
            ]
        }
        
        locations: List[Dict] = [location_0, location_1]
        
        return {
            "forecast_dates": forecast_dates,
            "locations": locations
        }
        
    except KeyError as e:
        raise KeyError(f"Missing expected data field: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to generate UV forecast: {str(e)}")