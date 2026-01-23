from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_key_0 (str): First key name in the JSON data
        - data_value_0 (str): Value corresponding to first key
        - data_key_1 (str): Second key name in the JSON data
        - data_value_1 (str): Value corresponding to second key
    """
    return {
        "data_key_0": "message",
        "data_value_0": "success",
        "data_key_1": "status",
        "data_value_1": "ok"
    }

def fetch_server_fetch_json(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Fetch a JSON file from a URL.

    Args:
        url (str): URL of the JSON to fetch
        headers (Optional[Dict[str, str]]): Optional headers to include in the request

    Returns:
        Dict: JSON content fetched from the URL, preserving all key-value pairs returned by the server

    Raises:
        ValueError: If URL is empty or invalid
    """
    if not url or not url.strip():
        raise ValueError("URL is required and cannot be empty")

    # Simulate calling external API which returns only flat scalar values
    api_data = call_external_api("fetch-server-fetch_json")

    # Construct the nested 'data' dictionary from flattened API response
    data = {
        api_data["data_key_0"]: api_data["data_value_0"],
        api_data["data_key_1"]: api_data["data_value_1"]
    }

    return {
        "data": data
    }