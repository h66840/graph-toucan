from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for markdown content retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - content (str): Fetched webpage content in Markdown format
        - error (str): Error message if request failed, or empty string if none
    """
    # Simulate realistic responses based on tool name
    if tool_name == "fetch-mcp-server-fetch_markdown":
        return {
            "content": "# Welcome to Example.com\n\nThis is a sample website content converted to Markdown.\n\n- List item one\n- List item two\n\nMore text content here to simulate a real webpage with approximately enough characters to test truncation and indexing features when needed.",
            "error": ""
        }
    else:
        return {
            "content": "",
            "error": "Unknown tool name"
        }

def fetch_mcp_server_fetch_markdown(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    max_length: Optional[int] = 5000,
    start_index: Optional[int] = 0
) -> Dict[str, Optional[str]]:
    """
    Fetch a website and return the content as Markdown.
    
    This function simulates fetching a webpage and converting its content to Markdown format.
    It supports optional request headers, character limit, and start index for partial content.
    
    Args:
        url (str): URL of the website to fetch (required)
        headers (Optional[Dict[str, str]]): Optional headers to include in the request
        max_length (Optional[int]): Maximum number of characters to return (default: 5000)
        start_index (Optional[int]): Start content from this character index (default: 0)
    
    Returns:
        Dict with the following keys:
        - content (Optional[str]): The fetched content of the webpage in Markdown format
        - error (Optional[str]): Error message if the request failed, otherwise None
    
    Raises:
        ValueError: If url is empty or invalid
    """
    # Input validation
    if not url or not url.strip():
        return {
            "content": None,
            "error": "URL is required and cannot be empty"
        }
    
    # Set defaults
    max_len = max_length if max_length is not None else 5000
    start_idx = start_index if start_index is not None else 0
    
    # Validate parameters
    if max_len < 0:
        return {
            "content": None,
            "error": "max_length must be non-negative"
        }
    
    if start_idx < 0:
        return {
            "content": None,
            "error": "start_index must be non-negative"
        }
    
    # Call external API to get simulated response
    api_data = call_external_api("fetch-mcp-server-fetch_markdown")
    
    # Extract content and error (already in simple scalar form)
    raw_content = api_data["content"]
    api_error = api_data["error"] if api_data["error"] else None
    
    # Handle API-level errors
    if api_error:
        return {
            "content": None,
            "error": api_error
        }
    
    # Apply start_index and max_length slicing
    end_index = start_idx + max_len
    truncated_content = raw_content[start_idx:end_index]
    
    # If no content after slicing, return empty string with no error
    if not truncated_content:
        return {
            "content": "",
            "error": None
        }
    
    return {
        "content": truncated_content,
        "error": None
    }