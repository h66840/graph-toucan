from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for fetching HTML content.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - html_content (str): Simulated HTML source code of the fetched webpage
    """
    return {
        "html_content": "<!DOCTYPE html><html><head><title>Sample Page</title></head><body><h1>Welcome to the Sample Website</h1><p>This is a simulated HTML content fetched from a remote server.</p></body></html>"
    }

def fetch_server_fetch_html(headers: Optional[Dict[str, str]] = None, url: str = "") -> Dict[str, Any]:
    """
    Fetch a website and return the content as HTML.
    
    This function simulates fetching a webpage's HTML content by calling an external API.
    It returns a dictionary containing the full HTML source code of the fetched webpage.
    
    Args:
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        url (str): URL of the website to fetch (required)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - html_content (str): The full HTML source code of the fetched webpage
    
    Raises:
        ValueError: If url is not provided or is empty
    """
    # Input validation
    if not url:
        raise ValueError("URL is required and cannot be empty")
    
    # Call external API to get the data
    api_data = call_external_api("fetch-server-fetch_html")
    
    # Construct result matching output schema
    result = {
        "html_content": api_data["html_content"]
    }
    
    return result