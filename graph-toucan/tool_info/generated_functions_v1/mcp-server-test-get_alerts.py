from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): Type of first weather alert event
        - alert_0_area (str): Affected area for first alert
        - alert_0_severity (str): Severity level of first alert
        - alert_0_description (str): Description of first alert
        - alert_0_instructions (str): Safety instructions for first alert
        - alert_1_event (str): Type of second weather alert event
        - alert_1_area (str): Affected area for second alert
        - alert_1_severity (str): Severity level of second alert
        - alert_1_description (str): Description of second alert
        - alert_1_instructions (str): Safety instructions for second alert
    """
    return {
        "alert_0_event": "Severe Thunderstorm Warning",
        "alert_0_area": "Northern California",
        "alert_0_severity": "High",
        "alert_0_description": "A severe thunderstorm is producing damaging winds over 70 mph and large hail.",
        "alert_0_instructions": "Seek shelter indoors immediately and stay away from windows.",
        "alert_1_event": "Flash Flood Watch",
        "alert_1_area": "Central Valley",
        "alert_1_severity": "Moderate",
        "alert_1_description": "Heavy rainfall may cause flash flooding in low-lying areas.",
        "alert_1_instructions": "Avoid walking or driving through flooded areas."
    }


def mcp_server_test_get_alerts(state: str) -> Dict[str, List[Dict]]:
    """
    Get weather alerts for a US state.
    
    Args:
        state (str): Two-letter US state code (e.g. CA, NY)
    
    Returns:
        Dict containing a list of weather alerts, each with 'event', 'area', 'severity', 
        'description', and 'instructions' fields.
        
    Raises:
        ValueError: If state is not a valid two-letter US state code.
    """
    # List of valid US state codes
    valid_states = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ]
    
    # Input validation
    if not isinstance(state, str):
        raise ValueError("State must be a string.")
    if len(state) != 2 or state.upper() not in valid_states:
        raise ValueError(f"Invalid state code: {state}. Must be a valid two-letter US state code.")
    
    # Fetch simulated external data
    api_data = call_external_api("mcp-server-test-get_alerts")
    
    # Construct the alerts list from flattened API response
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
    
    return {"alerts": alerts}