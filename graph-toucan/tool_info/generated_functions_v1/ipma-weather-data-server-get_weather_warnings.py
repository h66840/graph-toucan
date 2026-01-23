from typing import Dict,Any,List
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather warning data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - warning_0_event (str): Type of weather event for first warning
        - warning_0_area (str): Affected area for first warning
        - warning_0_level (int): Warning level (1-4) for first warning
        - warning_0_start_time (str): Start time in ISO format for first warning
        - warning_0_end_time (str): End time in ISO format for first warning
        - warning_0_details (str): Additional details for first warning
        - warning_1_event (str): Type of weather event for second warning
        - warning_1_area (str): Affected area for second warning
        - warning_1_level (int): Warning level (1-4) for second warning
        - warning_1_start_time (str): Start time in ISO format for second warning
        - warning_1_end_time (str): End time in ISO format for second warning
        - warning_1_details (str): Additional details for second warning
    """
    return {
        "warning_0_event": "Tempestade",
        "warning_0_area": "Norte do país",
        "warning_0_level": 3,
        "warning_0_start_time": "2023-10-15T10:00:00Z",
        "warning_0_end_time": "2023-10-15T18:00:00Z",
        "warning_0_details": "Chuvas intensas e ventos fortes esperados.",
        "warning_1_event": "Neve",
        "warning_1_area": "Serra da Estrela",
        "warning_1_level": 4,
        "warning_1_start_time": "2023-10-15T12:00:00Z",
        "warning_1_end_time": "2023-10-16T08:00:00Z",
        "warning_1_details": "Acumulação de neve acima de 500m."
    }


def ipma_weather_data_server_get_weather_warnings() -> Dict[str, List[Dict]]:
    """
    Obter avisos meteorológicos ativos em Portugal.
    
    Returns:
        Dict containing a list of weather warning objects. Each warning contains:
        - event (str): Type of weather event
        - area (str): Affected geographic area
        - level (int): Warning level from 1 (low) to 4 (extreme)
        - start_time (str): Start time in ISO 8601 format
        - end_time (str): End time in ISO 8601 format
        - details (str, optional): Additional information about the warning
        
    The function retrieves data through an external API simulation and structures it
    according to the required output schema.
    
    Raises:
        KeyError: If expected fields are missing from the API response
        Exception: For any other processing errors
    """
    try:
        api_data = call_external_api("ipma-weather-data-server-get_weather_warnings")
        
        warnings = [
            {
                "event": api_data["warning_0_event"],
                "area": api_data["warning_0_area"],
                "level": api_data["warning_0_level"],
                "start_time": api_data["warning_0_start_time"],
                "end_time": api_data["warning_0_end_time"],
                "details": api_data["warning_0_details"]
            },
            {
                "event": api_data["warning_1_event"],
                "area": api_data["warning_1_area"],
                "level": api_data["warning_1_level"],
                "start_time": api_data["warning_1_start_time"],
                "end_time": api_data["warning_1_end_time"],
                "details": api_data["warning_1_details"]
            }
        ]
        
        return {"warnings": warnings}
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise Exception(f"Error processing weather warnings: {e}")