from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather alerts.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): Type of first weather event
        - alert_0_area (str): Affected area for first alert
        - alert_0_severity (str): Severity level of first alert
        - alert_0_status (str): Status of first alert
        - alert_0_headline (str): Headline description of first alert
        - alert_1_event (str): Type of second weather event
        - alert_1_area (str): Affected area for second alert
        - alert_1_severity (str): Severity level of second alert
        - alert_1_status (str): Status of second alert
        - alert_1_headline (str): Headline description of second alert
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

def weather_mcp_server_get_alerts(state: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Get weather alerts for a given state.
    
    This function retrieves weather alerts for the specified two-letter state code.
    It simulates calling an external weather alert service and returns a list of
    current weather alerts with details about event type, affected area, severity,
    status, and headline description.
    
    Args:
        state (str): Two-letter state code (e.g. CA, NY). Required.
        
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
    # Input validation
    if not state:
        raise ValueError("State code is required")
    
    if not isinstance(state, str) or len(state) != 2 or not state.isalpha():
        raise ValueError("State must be a two-letter alphabetic code")
    
    # Convert to uppercase for consistency
    state = state.upper()
    
    # Call external API to get data (simulated)
    api_data = call_external_api("weather-mcp-server-get-alerts")
    
    # Construct the nested structure matching output schema
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