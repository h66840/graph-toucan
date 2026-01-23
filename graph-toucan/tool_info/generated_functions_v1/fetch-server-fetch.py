from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the fetch-server-fetch tool.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Fetched content of the URL
        - error (str): Error message if fetch failed
        - status_code (int): HTTP status code from the server
        - url (str): The URL that was attempted to be fetched
        - truncated (bool): Whether the content was truncated due to max_length
        - start_index (int): The character index from which content was returned
    """
    return {
        "content": "# Welcome to Example.com\nThis is a sample markdown content fetched from a URL.\nIt includes headings, paragraphs, and other elements.",
        "error": "",
        "status_code": 200,
        "url": "https://example.com",
        "truncated": False,
        "start_index": 0
    }

def fetch_server_fetch(
    url: str,
    max_length: Optional[int] = None,
    raw: Optional[bool] = False,
    start_index: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Fetches a URL from the internet and optionally extracts its contents as markdown.
    
    This function simulates fetching content from a given URL. It can return raw HTML
    or simplified text (e.g., markdown), with optional truncation and partial content
    retrieval via start_index. Internet access is now available through this tool.
    
    Args:
        url (str): URL to fetch (required)
        max_length (Optional[int]): Maximum number of characters to return
        raw (Optional[bool]): Return raw HTML content without simplification
        start_index (Optional[int]): Start output from this character index
    
    Returns:
        Dict containing:
        - content (str): The fetched content, either raw HTML or simplified text
        - error (str): Error message if the fetch failed
        - status_code (int): HTTP status code from the fetch attempt
        - url (str): The URL that was attempted to be fetched
        - truncated (bool): Whether content was truncated due to max_length limit
        - start_index (int): The character index from which content was returned
    """
    # Input validation
    if not url:
        return {
            "content": "",
            "error": "URL is required",
            "status_code": 400,
            "url": "",
            "truncated": False,
            "start_index": 0
        }
    
    # Call external API to simulate fetching
    api_data = call_external_api("fetch-server-fetch")
    
    # Construct result based on API data and input parameters
    content = api_data["content"]
    requested_url = url  # Use the actual input URL
    error = api_data["error"]
    status_code = api_data["status_code"]
    
    # Apply start_index if specified
    actual_start_index = start_index if start_index is not None else 0
    if actual_start_index > len(content):
        content = ""
        error = f"Start index {actual_start_index} exceeds content length"
        status_code = 416
    else:
        content = content[actual_start_index:]
    
    # Apply max_length if specified
    truncated = False
    if max_length is not None and len(content) > max_length:
        content = content[:max_length]
        truncated = True
    
    # If raw is True, we would return HTML, but in this simulation we return content as-is
    # In a real implementation, different content might be returned based on `raw`
    final_content = content
    
    return {
        "content": final_content,
        "error": error,
        "status_code": status_code,
        "url": requested_url,
        "truncated": truncated,
        "start_index": actual_start_index
    }