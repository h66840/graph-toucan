from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching fire risk forecast data from external API for Portugal.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Message indicating failure to retrieve data, if applicable
    """
    # Simulate realistic response based on tool name
    if tool_name == "ao-generative-ai-cp3-smithery-server-get_fire_risk_forecast":
        return {
            "error_message": ""  # Assume success; no error
        }
    else:
        return {
            "error_message": "Unknown tool requested"
        }

def ao_generative_ai_cp3_smithery_server_get_fire_risk_forecast(day: Optional[int] = 1) -> Dict[str, Any]:
    """
    Get fire risk forecast for Portugal (today or tomorrow).
    
    Args:
        day (int, optional): 1 for today, 2 for tomorrow. Defaults to 1.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error_message (str): message indicating failure to retrieve fire risk data, 
              such as "Unable to fetch fire risk data."
    
    Raises:
        ValueError: If day is not 1 or 2.
    """
    # Input validation
    if day not in [1, 2]:
        return {
            "error_message": "Invalid day value. Use 1 for today or 2 for tomorrow."
        }
    
    # Fetch simulated external data
    api_data = call_external_api("ao-generative-ai-cp3-smithery-server-get_fire_risk_forecast")
    
    # Construct result using flat fields from API response
    result: Dict[str, Any] = {
        "error_message": api_data["error_message"]
    }
    
    return result