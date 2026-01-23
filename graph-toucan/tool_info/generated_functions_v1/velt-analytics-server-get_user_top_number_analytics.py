from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Velt analytics.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Error message returned when the API request fails
    """
    return {
        "error_message": ""
    }

def velt_analytics_server_get_user_top_number_analytics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get user analytics from Velt.

    This function retrieves user analytics data by calling an external API.
    It processes the input parameters and returns the corresponding analytics,
    including an error message if the request fails.

    Args:
        data (Dict[str, Any]): Input data containing parameters for the analytics request.
                              Expected to include user identification and query parameters.

    Returns:
        Dict[str, Any]: A dictionary containing the following fields:
            - error_message (str): Error message if the API request fails, otherwise empty string.
    """
    # Validate input
    if not isinstance(data, dict):
        return {"error_message": "Invalid input: 'data' must be a dictionary."}

    try:
        # Call external API to get flattened response
        api_data = call_external_api("velt_analytics_server_get_user_top_number_analytics")

        # Construct result matching output schema
        result = {
            "error_message": api_data.get("error_message", "")
        }

        return result

    except Exception as e:
        return {"error_message": f"An unexpected error occurred: {str(e)}"}