from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather alerts.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): Event name of the first weather alert
        - alert_0_area (str): Affected area of the first weather alert
        - alert_0_severity (str): Severity level of the first weather alert
        - alert_0_status (str): Status of the first weather alert
        - alert_0_headline (str): Headline description of the first weather alert
        - alert_1_event (str): Event name of the second weather alert
        - alert_1_area (str): Affected area of the second weather alert
        - alert_1_severity (str): Severity level of the second weather alert
        - alert_1_status (str): Status of the second weather alert
        - alert_1_headline (str): Headline description of the second weather alert
    """
    return {
        "alert_0_event": "Severe Thunderstorm Warning",
        "alert_0_area": "Northern California",
        "alert_0_severity": "Severe",
        "alert_0_status": "Active",
        "alert_0_headline": "Severe thunderstorms expected in Northern California with damaging winds and heavy rain.",
        "alert_1_event": "Flood Watch",
        "alert_1_area": "Southern California",
        "alert_1_severity": "Moderate",
        "alert_1_status": "Active",
        "alert_1_headline": "Flood watch issued for Southern California due to prolonged rainfall."
    }

def weather_get_alerts(state: str) -> Dict[str, Any]:
    """
    Get weather alerts for a given U.S. state using its two-letter state code.
    
    Args:
        state (str): Two-letter state code (e.g., CA, NY). Required.
    
    Returns:
        Dict containing a list of weather alerts. Each alert is a dictionary with:
        - event (str): Type of weather event
        - area (str): Geographic area affected
        - severity (str): Severity level of the alert
        - status (str): Current status of the alert
        - headline (str): Brief description of the alert
    
    Raises:
        ValueError: If state is not provided or not a valid two-letter code
    """
    if not state:
        raise ValueError("State code is required")
    
    if not isinstance(state, str) or len(state) != 2 or not state.isalpha():
        raise ValueError("State must be a two-letter alphabetic code")
    
    # Fetch simulated external data
    api_data = call_external_api("weather-get-alerts")
    
    # Construct list of alerts from flattened API response
    alerts = [
        {
            "event": api_data["alert_0_event"],
            "area": api_data["alert_0_area"],
            "severity": api_data["alert_0_severity"],
            "status": api_data["alert_0_status"],
            "headline": api_data["alert_0_headline"]
        },
        {
            "event": api_data["alert_1_event"],
            "area": api_data["alert_1_area"],
            "severity": api_data["alert_1_severity"],
            "status": api_data["alert_1_status"],
            "headline": api_data["alert_1_headline"]
        }
    ]
    
    return {"alerts": alerts}