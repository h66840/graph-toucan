from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather alerts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): Type of first weather event (e.g., 'Thunderstorm Warning')
        - alert_0_area (str): Affected area for first alert
        - alert_0_severity (str): Severity level of first alert (e.g., 'Severe')
        - alert_0_status (str): Status of first alert (e.g., 'Active')
        - alert_0_headline (str): Headline message for first alert
        - alert_1_event (str): Type of second weather event
        - alert_1_area (str): Affected area for second alert
        - alert_1_severity (str): Severity level of second alert
        - alert_1_status (str): Status of second alert
        - alert_1_headline (str): Headline message for second alert
    """
    # Simulate different responses based on state
    if tool_name == "weather-server-get-alerts":
        return {
            "alert_0_event": "Severe Thunderstorm Warning",
            "alert_0_area": "Northern California",
            "alert_0_severity": "Severe",
            "alert_0_status": "Active",
            "alert_0_headline": "Severe thunderstorms expected in northern CA with damaging winds and heavy rain.",
            "alert_1_event": "Flash Flood Watch",
            "alert_1_area": "Sierra Nevada Foothills",
            "alert_1_severity": "Moderate",
            "alert_1_status": "Active",
            "alert_1_headline": "Flash flooding possible in foothill regions due to intense rainfall."
        }
    return {}

def weather_server_get_alerts(state: str) -> Dict[str, Any]:
    """
    Get weather alerts for a given state.

    Args:
        state (str): Two-letter state code (e.g., 'CA', 'NY')

    Returns:
        Dict containing a list of weather alerts. Each alert is a dictionary with:
        - event (str): Type of weather event
        - area (str): Affected geographic area
        - severity (str): Severity level of the alert
        - status (str): Current status of the alert
        - headline (str): Brief description of the alert

    Raises:
        ValueError: If state is not a valid two-letter uppercase code
    """
    # Input validation
    if not state or not isinstance(state, str):
        raise ValueError("State must be a non-empty string")
    if len(state) != 2 or not state.isalpha() or not state.isupper():
        raise ValueError("State must be a two-letter uppercase code (e.g., 'CA', 'NY')")

    # Fetch simulated data from external API
    api_data = call_external_api("weather-server-get-alerts")

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

    return {"alerts": alerts}