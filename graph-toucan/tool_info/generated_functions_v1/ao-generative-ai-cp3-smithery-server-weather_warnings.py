from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather warnings data from external API for Portugal.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - warning_0_area (str): Area name for the first warning
        - warning_0_phenomenon (str): Weather phenomenon for the first warning
        - warning_0_level (int): Warning level (1-4) for the first warning
        - warning_0_start (str): Start time of the first warning in ISO format
        - warning_0_end (str): End time of the first warning in ISO format
        - warning_0_details (str): Additional details for the first warning
        - warning_1_area (str): Area name for the second warning
        - warning_1_phenomenon (str): Weather phenomenon for the second warning
        - warning_1_level (int): Warning level (1-4) for the second warning
        - warning_1_start (str): Start time of the second warning in ISO format
        - warning_1_end (str): End time of the second warning in ISO format
        - warning_1_details (str): Additional details for the second warning
    """
    return {
        "warning_0_area": "Lisbon",
        "warning_0_phenomenon": "Heavy Rain",
        "warning_0_level": 3,
        "warning_0_start": "2023-10-05T08:00:00",
        "warning_0_end": "2023-10-05T20:00:00",
        "warning_0_details": "Intense rainfall expected, possible urban flooding.",
        "warning_1_area": "Porto",
        "warning_1_phenomenon": "Strong Wind",
        "warning_1_level": 2,
        "warning_1_start": "2023-10-05T12:00:00",
        "warning_1_end": "2023-10-05T18:00:00",
        "warning_1_details": "Winds up to 80 km/h, caution advised for coastal areas."
    }

def ao_generative_ai_cp3_smithery_server_weather_warnings() -> Dict[str, Any]:
    """
    Retrieve and format weather warnings from IPMA for Portugal up to 3 days ahead.
    
    Returns:
        A dictionary containing a list of weather warning entries, each with:
        - area (str): Geographic area affected
        - phenomenon (str): Type of weather phenomenon
        - level (int): Warning level (1-4)
        - start (str): Start time in ISO format
        - end (str): End time in ISO format
        - details (str): Additional descriptive information
    """
    try:
        api_data = call_external_api("ao-generative-ai-cp3-smithery-server-weather_warnings")
        
        warnings = [
            {
                "area": api_data["warning_0_area"],
                "phenomenon": api_data["warning_0_phenomenon"],
                "level": api_data["warning_0_level"],
                "start": api_data["warning_0_start"],
                "end": api_data["warning_0_end"],
                "details": api_data["warning_0_details"]
            },
            {
                "area": api_data["warning_1_area"],
                "phenomenon": api_data["warning_1_phenomenon"],
                "level": api_data["warning_1_level"],
                "start": api_data["warning_1_start"],
                "end": api_data["warning_1_end"],
                "details": api_data["warning_1_details"]
            }
        ]
        
        return {"warnings": warnings}
    
    except KeyError as e:
        return {"warnings": [], "error": f"Missing data field: {str(e)}"}
    except Exception as e:
        return {"warnings": [], "error": f"Unexpected error: {str(e)}"}