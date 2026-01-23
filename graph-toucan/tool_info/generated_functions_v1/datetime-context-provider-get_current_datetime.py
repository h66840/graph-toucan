from typing import Dict, Any
from datetime import datetime, timezone

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - current_datetime (str): ISO 8601 formatted date and time string in UTC
    """
    now = datetime.now(timezone.utc)
    iso_format = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return {
        "current_datetime": iso_format
    }

def datetime_context_provider_get_current_datetime() -> Dict[str, Any]:
    """
    Get the current server date and time.
    
    This function retrieves the current datetime from the external API simulation
    and returns it in ISO 8601 format in UTC.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - current_datetime (str): ISO 8601 formatted date and time string in UTC (e.g., '2025-08-10T20:45:12.566Z')
    """
    try:
        api_data = call_external_api("datetime-context-provider-get_current_datetime")
        
        result = {
            "current_datetime": api_data["current_datetime"]
        }
        
        return result
        
    except Exception as e:
        # In case of any error, return a fallback current datetime
        fallback_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        return {"current_datetime": fallback_time}