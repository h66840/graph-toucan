from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for documentation retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if page not found, empty string if no error
        - available_pages_0_title (str): Title of first available documentation page
        - available_pages_0_href (str): Relative URL path of first available documentation page
        - available_pages_1_title (str): Title of second available documentation page
        - available_pages_1_href (str): Relative URL path of second available documentation page
    """
    return {
        "error": "",
        "available_pages_0_title": "Getting Started",
        "available_pages_0_href": "/docs/getting-started",
        "available_pages_1_title": "API Reference",
        "available_pages_1_href": "/docs/api-reference"
    }

def openai_agent_library_get_doc(path: str) -> Dict[str, Any]:
    """
    Get content of a specific documentation page.
    
    Args:
        path (str): The relative URL path of the documentation page to retrieve.
        
    Returns:
        Dict containing:
        - error (str): Error message when the requested documentation page is not found
        - available_pages (List[Dict]): List of available documentation pages, each with 'title' and 'href' fields
        
    Raises:
        ValueError: If path is None or empty
    """
    if not path:
        raise ValueError("Parameter 'path' is required")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("openai-agent-library-get_doc")
    
    # Construct the result according to the output schema
    result: Dict[str, Any] = {
        "error": api_data["error"],
        "available_pages": [
            {
                "title": api_data["available_pages_0_title"],
                "href": api_data["available_pages_0_href"]
            },
            {
                "title": api_data["available_pages_1_title"],
                "href": api_data["available_pages_1_href"]
            }
        ]
    }
    
    return result