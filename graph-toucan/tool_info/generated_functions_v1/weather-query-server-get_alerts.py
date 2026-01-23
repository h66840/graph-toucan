from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for weather alerts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the alert retrieval process, e.g., 'success' or 'error'
        - message (str): Human-readable description of the result
    """
    return {
        "status": "success",
        "message": "Alerts retrieved successfully."
    }

def weather_query_server_get_alerts(state: str) -> Dict[str, Any]:
    """
    Retrieves weather alerts for a given state by querying an external API.

    Args:
        state (str): The state for which to retrieve weather alerts. Required.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): Status of the alert retrieval process ('success' or 'error')
            - message (str): Human-readable message describing the result
    """
    # Input validation
    if not state or not isinstance(state, str):
        return {
            "status": "error",
            "message": "Invalid input: 'state' must be a non-empty string."
        }

    try:
        # Call external API to get data (simulated)
        api_data = call_external_api("weather-query-server-get_alerts")

        # Construct result matching output schema
        result = {
            "status": api_data["status"],
            "message": api_data["message"]
        }

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }