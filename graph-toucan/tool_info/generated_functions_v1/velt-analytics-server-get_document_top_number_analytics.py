from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for document analytics.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Error message returned when the API request fails
    """
    return {
        "error_message": ""
    }

def velt_analytics_server_get_document_top_number_analytics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get document analytics from Velt.

    Args:
        data (Dict[str, Any]): Input data object containing parameters for the analytics request.

    Returns:
        Dict[str, Any]: A dictionary containing the following fields:
            - error_message (str): Error message returned when the API request fails, such as missing environment variables or authentication issues.
    """
    # Validate input
    if not isinstance(data, dict):
        return {"error_message": "Input data must be a dictionary."}

    # Call external API simulation
    api_data = call_external_api("velt_analytics_server_get_document_top_number_analytics")

    # Construct result with proper schema
    result = {
        "error_message": api_data.get("error_message", "")
    }

    return result