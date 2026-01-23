from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Plain text content extracted from the webpage
    """
    return {
        "content": "This is a sample plain text content extracted from a webpage. It contains no HTML tags or formatting. "
                   "The text is clean and readable, simulating the result of fetching and parsing a real webpage. "
                   "Additional sentences may be included to reach a reasonable length for demonstration purposes."
    }

def fetch_mcp_server_fetch_txt(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    max_length: Optional[int] = 5000,
    start_index: Optional[int] = 0
) -> Dict[str, str]:
    """
    Fetch a website and return the content as plain text with all HTML tags and formatting removed.
    
    Args:
        url (str): URL of the website to fetch (required)
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        max_length (Optional[int]): Maximum number of characters to return (default: 5000)
        start_index (Optional[int]): Start content from this character index (default: 0)
    
    Returns:
        Dict[str, str]: A dictionary containing the extracted plain text content
            - content (str): The plain text content after applying start_index and max_length constraints
    
    Raises:
        ValueError: If url is empty or invalid
        TypeError: If parameters are of incorrect type
    """
    # Input validation
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    if headers is not None and not isinstance(headers, dict):
        raise TypeError("Headers must be a dictionary or None")
    
    if max_length is not None and (not isinstance(max_length, int) or max_length <= 0):
        raise ValueError("max_length must be a positive integer")
    
    if start_index is not None and (not isinstance(start_index, int) or start_index < 0):
        raise ValueError("start_index must be a non-negative integer")
    
    # Set defaults
    effective_max_length = max_length if max_length is not None else 5000
    effective_start_index = start_index if start_index is not None else 0
    
    # Fetch simulated content from external API
    api_data = call_external_api("fetch-mcp-server-fetch_txt")
    
    # Extract and process content
    raw_content = api_data["content"]
    
    # Apply start_index and max_length constraints
    end_index = effective_start_index + effective_max_length
    processed_content = raw_content[effective_start_index:end_index]
    
    return {
        "content": processed_content
    }