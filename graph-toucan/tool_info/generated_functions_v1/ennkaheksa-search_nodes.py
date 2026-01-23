from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for node search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_nodeType (str): Node type of first matching node
        - result_0_displayName (str): Display name of first node
        - result_0_description (str): Description of first node
        - result_0_category (str): Category of first node
        - result_0_package (str): Package name of first node
        - result_1_nodeType (str): Node type of second matching node
        - result_1_displayName (str): Display name of second node
        - result_1_description (str): Description of second node
        - result_1_category (str): Category of second node
        - result_1_package (str): Package name of second node
        - totalCount (int): Total number of nodes returned by search
    """
    return {
        "result_0_nodeType": "n8n-nodes-base.slack",
        "result_0_displayName": "Slack",
        "result_0_description": "Send messages to Slack channels or users",
        "result_0_category": "Communication",
        "result_0_package": "n8n-nodes-base",
        "result_1_nodeType": "n8n-nodes-base.emailSend",
        "result_1_displayName": "Email Send",
        "result_1_description": "Send emails via SMTP or email services",
        "result_1_category": "Communication",
        "result_1_package": "n8n-nodes-base",
        "totalCount": 2
    }

def ennkaheksa_search_nodes(limit: Optional[int] = 20, query: str = "") -> Dict[str, Any]:
    """
    Search nodes by keywords. Returns nodes containing ANY of the search words (OR logic).
    
    Best practice: Use single words for precise results, multiple words for broader search.
    Searches in node names and descriptions. If no results, try shorter words or use list_nodes by category.
    
    Args:
        limit (Optional[int]): Max results. Default 20 is usually enough. Increase if needed.
        query (str): Search term - MUST BE SINGLE WORD for best results! Case-insensitive.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of node objects with keys 'nodeType', 'displayName', 
          'description', 'category', and 'package'
        - totalCount (int): Total number of nodes returned by the search
    
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query parameter is required and must be a non-empty string.")
    
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("Limit must be a positive integer.")
    
    # Call external API to get flattened data
    api_data = call_external_api("ennkaheksa-search_nodes")
    
    # Construct results list from indexed fields
    results: List[Dict[str, Any]] = []
    
    # Extract up to 2 results based on available indexed data
    for i in range(2):
        node_type_key = f"result_{i}_nodeType"
        if node_type_key not in api_data:
            break
            
        node = {
            "nodeType": api_data[f"result_{i}_nodeType"],
            "displayName": api_data[f"result_{i}_displayName"],
            "description": api_data[f"result_{i}_description"],
            "category": api_data[f"result_{i}_category"],
            "package": api_data[f"result_{i}_package"]
        }
        results.append(node)
    
    # Apply limit
    if limit is not None:
        results = results[:limit]
    
    return {
        "results": results,
        "totalCount": api_data["totalCount"]
    }