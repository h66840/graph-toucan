from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather alerts data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): First alert event type
        - alert_0_area (str): First alert affected area
        - alert_0_severity (str): First alert severity level
        - alert_0_status (str): First alert status
        - alert_0_headline (str): First alert headline
        - alert_1_event (str): Second alert event type
        - alert_1_area (str): Second alert affected area
        - alert_1_severity (str): Second alert severity level
        - alert_1_status (str): Second alert status
        - alert_1_headline (str): Second alert headline
    """
    return {
        "alert_0_event": "Severe Thunderstorm Warning",
        "alert_0_area": "Northern California",
        "alert_0_severity": "Severe",
        "alert_0_status": "Active",
        "alert_0_headline": "Severe thunderstorms expected in Northern California with damaging winds and large hail.",
        "alert_1_event": "Flood Watch",
        "alert_1_area": "Central Valley",
        "alert_1_severity": "Moderate",
        "alert_1_status": "Active",
        "alert_1_headline": "Flood watch issued for Central Valley due to heavy rainfall over the next 24 hours."
    }

def endless_get_alerts(state: str) -> Dict[str, Any]:
    """
    Get weather alerts for a specified state.
    
    Args:
        state (str): Two-letter state code (e.g. CA, NY)
    
    Returns:
        Dict containing a list of weather alerts, each with event, area, severity, status, and headline fields.
    
    Raises:
        ValueError: If state is not a valid two-letter code
    """
    # Input validation
    if not state or not isinstance(state, str) or len(state.strip()) != 2 or not state.isalpha():
        raise ValueError("State must be a valid two-letter code (e.g. CA, NY)")
    
    state = state.strip().upper()
    
    # Call external API to get data
    api_data = call_external_api("endless-get-alerts")
    
    # Construct the alerts list from flattened API response
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
    
    # Add state context to area fields
    for alert in alerts:
        if state == "CA" and "California" not in alert["area"]:
            alert["area"] = f"{alert['area']} ({state})"
    
    return {"alerts": alerts}