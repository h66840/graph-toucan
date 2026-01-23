from typing import Dict, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for HTML content fetching.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): The HTML content of the fetched webpage
        - status_code (int): HTTP status code returned by the server
        - success (bool): Indicates whether the request was completed successfully
        - url_resolved (str): The final URL after any redirects
        - headers_content_type (str): Content-Type from response headers
        - headers_server (str): Server information from response headers
        - headers_date (str): Date header from response
        - fetch_timestamp (str): ISO 8601 timestamp of the request
        - error_message (str): Error message if request failed, otherwise empty
        - charset (str): Character encoding detected or specified
    """
    return {
        "content": "<html><head><title>Test Page</title></head><body><h1>Hello World</h1><p>This is a test page.</p></body></html>",
        "status_code": 200,
        "success": True,
        "url_resolved": "https://example.com",
        "headers_content_type": "text/html; charset=utf-8",
        "headers_server": "Apache/2.4.41",
        "headers_date": "Mon, 15 Jan 2024 12:00:00 GMT",
        "fetch_timestamp": "2024-01-15T12:00:00.000Z",
        "error_message": "",
        "charset": "utf-8"
    }

def fetch_mcp_server_fetch_html(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    max_length: Optional[int] = 5000,
    start_index: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Fetch a website and return the content as HTML.
    
    Args:
        url (str): URL of the website to fetch (required)
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        max_length (Optional[int]): Maximum number of characters to return (default: 5000)
        start_index (Optional[int]): Start content from this character index (default: 0)
    
    Returns:
        Dict containing:
        - content (str): The HTML content of the fetched webpage, truncated or sliced
        - status_code (int): HTTP status code returned by the server
        - success (bool): Indicates whether the request was completed successfully
        - url_resolved (str): The final URL after any redirects
        - headers (Dict): Response headers from the server
        - fetch_timestamp (str): ISO 8601 timestamp indicating when the request was made
        - error_message (str): Descriptive error message if request failed, otherwise empty
        - charset (str): Character encoding detected or specified in the response
    
    Raises:
        ValueError: If url is empty or invalid
    """
    # Input validation
    if not url or not url.strip():
        return {
            "content": "",
            "status_code": 0,
            "success": False,
            "url_resolved": "",
            "headers": {},
            "fetch_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "error_message": "URL is required and cannot be empty",
            "charset": ""
        }
    
    try:
        # Call external API to get the data
        api_data = call_external_api("fetch-mcp-server-fetch_html")
        
        # Apply start_index and max_length slicing
        raw_content = api_data["content"]
        start = start_index or 0
        max_len = max_length or 5000
        
        # Ensure start_index is not negative
        start = max(0, start)
        
        # Extract content based on start_index and max_length
        end_index = start + max_len
        content = raw_content[start:end_index]
        
        # Construct response headers dict from flattened fields
        headers_dict = {
            "Content-Type": api_data["headers_content_type"],
            "Server": api_data["headers_server"],
            "Date": api_data["headers_date"]
        }
        
        # Return the complete response structure
        return {
            "content": content,
            "status_code": api_data["status_code"],
            "success": api_data["success"],
            "url_resolved": api_data["url_resolved"],
            "headers": headers_dict,
            "fetch_timestamp": api_data["fetch_timestamp"],
            "error_message": api_data["error_message"],
            "charset": api_data["charset"]
        }
        
    except Exception as e:
        # Handle any unexpected errors
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        return {
            "content": "",
            "status_code": 0,
            "success": False,
            "url_resolved": url,
            "headers": {},
            "fetch_timestamp": timestamp,
            "error_message": f"Unexpected error occurred: {str(e)}",
            "charset": ""
        }