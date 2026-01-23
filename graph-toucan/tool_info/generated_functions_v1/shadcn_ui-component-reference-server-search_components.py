from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for shadcn/ui component search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching component
        - result_0_description (str): Description of the first component
        - result_0_url (str): URL of the first component documentation
        - result_1_name (str): Name of the second matching component
        - result_1_description (str): Description of the second component
        - result_1_url (str): URL of the second component documentation
    """
    return {
        "result_0_name": "button",
        "result_0_description": "A customizable button component with multiple variants and sizes.",
        "result_0_url": "https://ui.shadcn.com/docs/components/button",
        "result_1_name": "card",
        "result_1_description": "A container component for displaying content in a card layout with header, content, and footer sections.",
        "result_1_url": "https://ui.shadcn.com/docs/components/card"
    }

def shadcn_ui_component_reference_server_search_components(query: str) -> Dict[str, Any]:
    """
    Search for shadcn/ui components by keyword.
    
    Args:
        query (str): Search query to find relevant components
        
    Returns:
        Dict containing a list of component objects with name, description, and url fields:
        - results (List[Dict]): List of dictionaries, each containing:
            - name (str): Component name
            - description (str): Component description
            - url (str): URL to component documentation
            
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query:
        raise ValueError("Query parameter is required")
    
    if not isinstance(query, str):
        raise ValueError("Query must be a string")
    
    # Call external API to get flattened data
    api_data = call_external_api("shadcn/ui-component-reference-server-search_components")
    
    # Construct the nested structure as per output schema
    results = [
        {
            "name": api_data["result_0_name"],
            "description": api_data["result_0_description"],
            "url": api_data["result_0_url"]
        },
        {
            "name": api_data["result_1_name"],
            "description": api_data["result_1_description"],
            "url": api_data["result_1_url"]
        }
    ]
    
    return {"results": results}