from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather alerts.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - alert_0_event (str): Event type of first alert
        - alert_0_area (str): Affected area of first alert
        - alert_0_severity (str): Severity level of first alert
        - alert_0_description (str): Description of first alert
        - alert_0_instructions (str): Safety instructions for first alert
        - alert_1_event (str): Event type of second alert
        - alert_1_area (str): Affected area of second alert
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
        "alert_1_area": "Central Valley",
        "alert_1_severity": "Moderate",
        "alert_1_description": "Heavy rainfall may cause flash flooding in low-lying and poor drainage areas. Be prepared to take action.",
        "alert_1_instructions": "Avoid walking or driving through flooded areas. Move to higher ground if necessary."
    }

def weather_mcp_server_get_alerts(state: str) -> Dict[str, Any]:
    """
    Get weather alerts for a US state.

    Args:
        state (str): Two-letter US state code (e.g. CA, NY)

    Returns:
        Dict containing a list of weather alerts. Each alert contains:
        - event (str): Type of weather event
        - area (str): Geographic area affected
        - severity (str): Severity level of the alert
        - description (str): Detailed description of the alert
        - instructions (str): Recommended safety actions

    Raises:
        ValueError: If state code is not provided or invalid
    """
    if not state:
        raise ValueError("State code is required")
    
    if not isinstance(state, str) or len(state.strip()) != 2 or not state.isalpha():
        raise ValueError("State must be a two-letter alphabetic code")
    
    state = state.strip().upper()
    
    # Validate US state code (partial list for demonstration)
    valid_states = {
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
    }
    
    if state not in valid_states:
        raise ValueError(f"Invalid US state code: {state}")
    
    # Fetch simulated external data
    api_data = call_external_api("weather-mcp-server-get_alerts")
    
    # Construct alerts list from flattened API response
    alerts = [
        {
            "event": api_data["alert_0_event"],
            "area": api_data["alert_0_area"],
            "severity": api_data["alert_0_severity"],
            "description": api_data["alert_0_description"],
            "instructions": api_data["alert_0_instructions"]
        },
        {
            "event": api_data["alert_1_event"],
            "area": api_data["alert_1_area"],
            "severity": api_data["alert_1_severity"],
            "description": api_data["alert_1_description"],
            "instructions": api_data["alert_1_instructions"]
        }
    ]
    
    # Optionally filter or modify alerts based on state (simulated logic)
    # For example, append state code to area names
    for alert in alerts:
        if state == "CA":
            alert["area"] = alert["area"].replace("California", "California").replace("CA", "CA")
        elif state == "NY":
            alert["area"] = alert["area"].replace("California", "New York").replace("CA", "NY")
    
    return {"alerts": alerts}