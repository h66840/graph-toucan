from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for icon search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_name (str): Name of the first icon result
        - result_0_tags (str): Comma-separated tags for the first icon
        - result_0_category (str): Category of the first icon
        - result_0_featured (bool): Whether the first icon is featured
        - result_0_version (str): Version of the first icon
        - result_1_name (str): Name of the second icon result
        - result_1_tags (str): Comma-separated tags for the second icon
        - result_1_category (str): Category of the second icon
        - result_1_featured (bool): Whether the second icon is featured
        - result_1_version (str): Version of the second icon
    """
    return {
        "result_0_name": "home",
        "result_0_tags": "house, building, residence, dwelling",
        "result_0_category": "real-estate",
        "result_0_featured": True,
        "result_0_version": "1.0.0",
        "result_1_name": "notification",
        "result_1_tags": "alert, message, bell, reminder",
        "result_1_category": "communication",
        "result_1_featured": False,
        "result_1_version": "1.1.0"
    }

def hugeicons_mcp_server_search_icons(query: str) -> Dict[str, Any]:
    """
    Search for icons by name or tags. Use commas to search for multiple icons.
    
    Args:
        query (str): Search query to find relevant icons. Separate multiple searches with commas.
        
    Returns:
        Dict containing a list of icon objects with keys:
        - results (List[Dict]): List of icon dictionaries, each containing:
            - name (str): Icon name
            - tags (List[str]): List of tag strings
            - category (str): Icon category
            - featured (bool): Whether the icon is featured
            - version (str): Version string of the icon
            
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    # Call the external API to get flat data
    api_data = call_external_api("hugeicons-mcp-server-search_icons")
    
    # Construct the results list from flattened API response
    results = [
        {
            "name": api_data["result_0_name"],
            "tags": [tag.strip() for tag in api_data["result_0_tags"].split(",")],
            "category": api_data["result_0_category"],
            "featured": api_data["result_0_featured"],
            "version": api_data["result_0_version"]
        },
        {
            "name": api_data["result_1_name"],
            "tags": [tag.strip() for tag in api_data["result_1_tags"].split(",")],
            "category": api_data["result_1_category"],
            "featured": api_data["result_1_featured"],
            "version": api_data["result_1_version"]
        }
    ]
    
    return {"results": results}