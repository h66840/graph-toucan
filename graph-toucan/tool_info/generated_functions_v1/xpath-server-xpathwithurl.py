from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for xpath-server-xpathwithurl tool.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Detailed error message describing the failure
        - error_type (str): Type of error encountered (e.g., "McpError")
        - traceback_lines_0 (str): First line of traceback
        - traceback_lines_1 (str): Second line of traceback
        - troubleshooting_url (str): URL for troubleshooting guidance
    """
    return {
        "error_message": "Failed to fetch content from URL due to network timeout",
        "error_type": "McpError",
        "traceback_lines_0": "Traceback (most recent call last):",
        "traceback_lines_1": "  raise McpError('Request timed out')",
        "troubleshooting_url": "https://example.com/troubleshooting/xpath-server"
    }

def xpath_server_xpathwithurl(
    query: str, 
    url: str, 
    mimeType: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch content from a URL and select query it using XPath.
    
    This function simulates querying XML/HTML content from a URL using an XPath expression.
    It returns structured error information as per the tool's output schema.
    
    Args:
        query (str): The XPath query to execute (required)
        url (str): The URL to fetch XML/HTML content from (required)
        mimeType (Optional[str]): The MIME type (e.g. text/xml, application/xml, text/html, application/xhtml+xml)
    
    Returns:
        Dict containing:
        - error_message (str): detailed error message describing the failure
        - error_type (str): type of error encountered (e.g., "McpError")
        - traceback_lines (List[str]): list of traceback strings showing the call stack
        - troubleshooting_url (str): URL for troubleshooting guidance
    """
    # Input validation
    if not query:
        raise ValueError("Parameter 'query' is required")
    if not url:
        raise ValueError("Parameter 'url' is required")
    
    # Call external API simulation
    api_data = call_external_api("xpath-server-xpathwithurl")
    
    # Construct output structure matching schema exactly
    result = {
        "error_message": api_data["error_message"],
        "error_type": api_data["error_type"],
        "traceback_lines": [
            api_data["traceback_lines_0"],
            api_data["traceback_lines_1"]
        ],
        "troubleshooting_url": api_data["troubleshooting_url"]
    }
    
    return result