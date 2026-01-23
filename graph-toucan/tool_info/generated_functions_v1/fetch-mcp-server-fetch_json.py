from typing import Dict, Any, Optional
import json

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching JSON data from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_str (str): String representation of the JSON data (limited by max_length and start_index)
        - simulated_url (str): The URL being simulated
        - max_length (int): Maximum number of characters to return
        - start_index (int): Starting character index
    """
    # Simulated JSON response
    simulated_json = {
        "name": "Test Resource",
        "id": 12345,
        "active": True,
        "tags": ["example", "test", "mcp"],
        "metadata": {
            "created": "2023-01-01T00:00:00Z",
            "version": 1.5
        },
        "items": [
            {"index": 0, "value": "first"},
            {"index": 1, "value": "second"},
            {"index": 2, "value": "third"}
        ]
    }
    
    # Convert to JSON string
    json_str = json.dumps(simulated_json)
    
    # These values would normally come from input, but we simulate them
    start_idx = 0
    max_len = 5000
    
    # Apply slicing logic
    sliced_str = json_str[start_idx:start_idx + max_len]
    
    return {
        "data_str": sliced_str,
        "simulated_url": "https://api.example.com/data.json",
        "max_length": max_len,
        "start_index": start_idx
    }

def fetch_mcp_server_fetch_json(
    url: str, 
    headers: Optional[Dict[str, str]] = None, 
    max_length: Optional[int] = 5000, 
    start_index: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Fetch a JSON file from a URL with optional slicing and headers.
    
    Args:
        url (str): URL of the JSON to fetch (required)
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        max_length (Optional[int]): Maximum number of characters to return (default: 5000)
        start_index (Optional[int]): Start content from this character index (default: 0)
    
    Returns:
        Dict containing:
        - data (Dict | List | str): the parsed JSON content returned from the URL; 
          can be a dictionary, list, or primitive value depending on the fetched JSON structure
    
    Raises:
        ValueError: If URL is empty or invalid
        TypeError: If max_length or start_index are negative
    """
    # Input validation
    if not url or not url.strip():
        raise ValueError("URL is required and cannot be empty")
    
    if max_length is not None and max_length < 0:
        raise TypeError("max_length cannot be negative")
    
    if start_index is not None and start_index < 0:
        raise TypeError("start_index cannot be negative")
    
    # Use default values if not provided
    effective_max_length = max_length if max_length is not None else 5000
    effective_start_index = start_index if start_index is not None else 0
    
    # Call external API simulation
    api_data = call_external_api("fetch-mcp-server-fetch_json")
    
    # Extract the full simulated JSON string (we'll re-slice based on actual inputs)
    simulated_json = {
        "name": "Test Resource",
        "id": 12345,
        "active": True,
        "tags": ["example", "test", "mcp"],
        "metadata": {
            "created": "2023-01-01T00:00:00Z",
            "version": 1.5
        },
        "items": [
            {"index": 0, "value": "first"},
            {"index": 1, "value": "second"},
            {"index": 2, "value": "third"}
        ]
    }
    
    # Convert to string and apply actual slicing parameters
    json_str = json.dumps(simulated_json)
    end_index = effective_start_index + effective_max_length
    sliced_json_str = json_str[effective_start_index:end_index]
    
    try:
        # Parse the sliced string back to JSON
        # Note: This might fail if slicing breaks JSON structure
        # In a real implementation, we'd fetch full JSON then slice after parsing
        if sliced_json_str.startswith('{') or sliced_json_str.startswith('['):
            # Attempt to parse as JSON
            parsed_data = json.loads(sliced_json_str)
        else:
            # Return as string if parsing fails or it's a primitive
            parsed_data = sliced_json_str
    except json.JSONDecodeError:
        # If JSON is invalid due to slicing, return as string
        parsed_data = sliced_json_str
    
    return {
        "data": parsed_data
    }