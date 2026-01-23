from typing import Dict, Any, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching weather alert data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - alert_0_event (str): Type of first active weather alert
        - alert_0_severity (str): Severity level of first alert
        - alert_0_urgency (str): Urgency level of first alert
        - alert_0_areas (str): Affected areas for first alert
        - alert_0_effective (str): Effective timestamp for first alert
        - alert_0_expires (str): Expiration timestamp for first alert
        - alert_0_description (str): Description of first alert
        - alert_0_instructions (str): Safety instructions for first alert
        - alert_1_event (str): Type of second active weather alert
        - alert_1_severity (str): Severity level of second alert
        - alert_1_urgency (str): Urgency level of second alert
        - alert_1_areas (str): Affected areas for second alert
        - alert_1_effective (str): Effective timestamp for second alert
        - alert_1_expires (str): Expiration timestamp for second alert
        - alert_1_description (str): Description of second alert
        - alert_1_instructions (str): Safety instructions for second alert
        - location (str): The location identifier used in the query
        - alert_count (int): Number of active alerts returned
    """
    return {
        "alert_0_event": "Severe Thunderstorm Warning",
        "alert_0_severity": "severe",
        "alert_0_urgency": "immediate",
        "alert_0_areas": "Central Miami-Dade County",
        "alert_0_effective": "2023-08-15T14:30:00Z",
        "alert_0_expires": "2023-08-15T18:45:00Z",
        "alert_0_description": "A severe thunderstorm is producing quarter-size hail and damaging winds in excess of 60 mph. This storm will impact central Miami-Dade County between 14:30 and 18:45 UTC.",
        "alert_0_instructions": "Seek shelter immediately. Stay away from windows. Avoid flooded roadways.",
        "alert_1_event": "Flash Flood Watch",
        "alert_1_severity": "moderate",
        "alert_1_urgency": "expected",
        "alert_1_areas": "Southern Florida Peninsula",
        "alert_1_effective": "2023-08-15T12:00:00Z",
        "alert_1_expires": "2023-08-16T06:00:00Z",
        "alert_1_description": "Heavy rainfall from slow-moving storms may cause flash flooding across low-lying and poor drainage areas in southern Florida peninsula.",
        "alert_1_instructions": "Be prepared to take action. Monitor local weather reports. Avoid walking or driving through flood waters.",
        "location": "FL",
        "alert_count": 2
    }

def united_states_weather_get_weather_alerts(location: str, severity: str = "all") -> Dict[str, Any]:
    """
    Get active weather alerts, warnings, watches, and advisories for locations in the United States.
    
    Args:
        location (str): US location as coordinates (lat,lng) in decimal degrees OR 2-letter state/territory code.
                       Examples: '40.7128,-74.0060' for New York City, 'CA' for California, 'PR' for Puerto Rico.
                       Valid state codes: AL, AK, AS, AR, AZ, CA, CO, CT, DE, DC, FL, GA, GU, HI, ID, IL,
                       IN, IA, KS, KY, LA, ME, MD, MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND,
                       OH, OK, OR, PA, PR, RI, SC, SD, TN, TX, UT, VT, VI, VA, WA, WV, WI, WY, MP, PW, FM, MH.
        severity (str, optional): Filter by alert severity: 'extreme', 'severe', 'moderate', 'minor', or 'all' (default).
    
    Returns:
        Dict containing:
        - alerts (List[Dict]): list of active weather alerts, each containing 'event', 'severity', 'urgency',
          'areas', 'effective', 'expires', 'description', and 'instructions' fields
        - location (str): the location identifier used in the query, either coordinates or state code
        - alert_count (int): number of active alerts returned for the location
    
    Raises:
        ValueError: If location is empty or invalid format, or if severity has invalid value
    """
    # Input validation
    if not location or not location.strip():
        raise ValueError("Location parameter is required")
    
    location = location.strip().upper()
    
    # Validate state codes and coordinate format
    valid_state_codes = {
        "AL", "AK", "AS", "AR", "AZ", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "GU", 
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", 
        "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", 
        "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VI", "VA", "WA", 
        "WV", "WI", "WY", "MP", "PW", "FM", "MH"
    }
    
    if len(location) == 2 and "," not in location:
        if location not in valid_state_codes:
            raise ValueError(f"Invalid state/territory code: {location}")
    else:
        # Assume coordinates
        try:
            lat_str, lng_str = location.split(",")
            lat = float(lat_str.strip())
            lng = float(lng_str.strip())
            if not (-90 <= lat <= 90):
                raise ValueError("Latitude must be between -90 and 90")
            if not (-180 <= lng <= 180):
                raise ValueError("Longitude must be between -180 and 180")
        except ValueError as e:
            if "could not convert" in str(e) or "invalid literal" in str(e):
                raise ValueError("Coordinates must be in format 'lat,lng' with numeric values")
            else:
                raise e
        except Exception:
            raise ValueError("Location must be either a valid 2-letter state code or coordinates in 'lat,lng' format")
    
    # Validate severity
    valid_severities = {"extreme", "severe", "moderate", "minor", "all"}
    if severity not in valid_severities:
        raise ValueError(f"Invalid severity value: {severity}. Must be one of {valid_severities}")
    
    # Call external API to get data
    api_data = call_external_api("united-states-weather-get_weather_alerts")
    
    # Construct alerts list from flattened API response
    alerts = []
    
    # Process first alert if it exists
    if api_data["alert_count"] > 0:
        alert_0 = {
            "event": api_data["alert_0_event"],
            "severity": api_data["alert_0_severity"],
            "urgency": api_data["alert_0_urgency"],
            "areas": api_data["alert_0_areas"],
            "effective": api_data["alert_0_effective"],
            "expires": api_data["alert_0_expires"],
            "description": api_data["alert_0_description"],
            "instructions": api_data["alert_0_instructions"]
        }
        # Apply severity filter if not 'all'
        if severity == "all" or alert_0["severity"] == severity:
            alerts.append(alert_0)
    
    # Process second alert if it exists
    if api_data["alert_count"] > 1:
        alert_1 = {
            "event": api_data["alert_1_event"],
            "severity": api_data["alert_1_severity"],
            "urgency": api_data["alert_1_urgency"],
            "areas": api_data["alert_1_areas"],
            "effective": api_data["alert_1_effective"],
            "expires": api_data["alert_1_expires"],
            "description": api_data["alert_1_description"],
            "instructions": api_data["alert_1_instructions"]
        }
        # Apply severity filter if not 'all'
        if severity == "all" or alert_1["severity"] == severity:
            alerts.append(alert_1)
    
    # Return structured result matching output schema
    return {
        "alerts": alerts,
        "location": api_data["location"],
        "alert_count": len(alerts)
    }