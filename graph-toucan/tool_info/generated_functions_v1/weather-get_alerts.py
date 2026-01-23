from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather alerts.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): Type of first weather alert (e.g., 'Severe Thunderstorm Warning')
        - alert_0_area (str): Affected area for first alert (e.g., 'Northern California')
        - alert_0_severity (str): Severity level of first alert (e.g., 'Severe')
        - alert_0_description (str): Description of first alert
        - alert_0_instructions (str): Safety instructions for first alert
        - alert_1_event (str): Type of second weather alert
        - alert_1_area (str): Affected area for second alert
        - alert_1_severity (str): Severity level of second alert
        - alert_1_description (str): Description of second alert
        - alert_1_instructions (str): Safety instructions for second alert
    """
    return {
        "alert_0_event": "Severe Thunderstorm Warning",
        "alert_0_area": "Northern California",
        "alert_0_severity": "Severe",
        "alert_0_description": "A severe thunderstorm is producing damaging winds over 70 mph and large hail. This storm poses a threat to life and property.",
        "alert_0_instructions": "Seek shelter immediately. Stay away from windows and avoid using electrical equipment.",
        "alert_1_event": "Flash Flood Watch",
        "alert_1_area": "Southern California",
        "alert_1_severity": "Moderate",
        "alert_1_description": "Heavy rainfall may cause flash flooding in low-lying and poor drainage areas. Be prepared to take action.",
        "alert_1_instructions": "Avoid walking or driving through flood waters. Move to higher ground if necessary."
    }

def weather_get_alerts(state: str) -> Dict[str, Any]:
    """
    Get weather alerts for a US state.
    
    Args:
        state (str): Two-letter US state code (e.g. CA, NY)
    
    Returns:
        Dict containing a list of weather alerts, each with 'event', 'area', 'severity', 'description', and 'instructions' fields.
    
    Raises:
        ValueError: If state code is not a valid two-letter string
    """
    # Input validation
    if not isinstance(state, str):
        raise ValueError("State must be a string")
    if len(state) != 2 or not state.isalpha():
        raise ValueError("State must be a two-letter US state code")
    
    # Fetch simulated external data
    api_data = call_external_api("weather-get_alerts")
    
    # Construct alerts list from flattened API response
    alerts = [
        {
            "event": api_data["alert_0_event"],
            "area": f"{api_data['alert_0_area']} ({state})",
            "severity": api_data["alert_0_severity"],
            "description": api_data["alert_0_description"],
            "instructions": api_data["alert_0_instructions"]
        },
        {
            "event": api_data["alert_1_event"],
            "area": f"{api_data['alert_1_area']} ({state})",
            "severity": api_data["alert_1_severity"],
            "description": api_data["alert_1_description"],
            "instructions": api_data["alert_1_instructions"]
        }
    ]
    
    return {"alerts": alerts}