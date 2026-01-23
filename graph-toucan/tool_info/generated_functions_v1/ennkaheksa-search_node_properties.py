from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for node property search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - match_0_name (str): Name of the first matching property
        - match_0_displayName (str): Display name of the first match
        - match_0_type (str): Data type of the first match
        - match_0_description (str): Description of the first match
        - match_0_path (str): Path to the first match in the schema
        - match_0_required (bool): Whether the first match is required
        - match_0_default (str): Default value of the first match, if any
        - match_0_options (str): Options for the first match as comma-separated string
        - match_0_showWhen (str): Condition when the first match should be shown
        - match_1_name (str): Name of the second matching property
        - match_1_displayName (str): Display name of the second match
        - match_1_type (str): Data type of the second match
        - match_1_description (str): Description of the second match
        - match_1_path (str): Path to the second match in the schema
        - match_1_required (bool): Whether the second match is required
        - match_1_default (str): Default value of the second match, if any
        - match_1_options (str): Options for the second match as comma-separated string
        - match_1_showWhen (str): Condition when the second match should be shown
        - totalMatches (int): Total number of matched properties found
        - searchedIn (str): Description of the scope searched, e.g., "42 properties"
    """
    return {
        "match_0_name": "authType",
        "match_0_displayName": "Authentication Type",
        "match_0_type": "string",
        "match_0_description": "Type of authentication to use",
        "match_0_path": "node.parameters.auth.authType",
        "match_0_required": True,
        "match_0_default": "basic",
        "match_0_options": "basic,digest,bearer",
        "match_0_showWhen": "auth.enabled=true",
        "match_1_name": "authToken",
        "match_1_displayName": "Authentication Token",
        "match_1_type": "string",
        "match_1_description": "Token used for authentication",
        "match_1_path": "node.parameters.auth.authToken",
        "match_1_required": False,
        "match_1_default": "",
        "match_1_options": "",
        "match_1_showWhen": "auth.authType=bearer",
        "totalMatches": 2,
        "searchedIn": "42 properties"
    }

def ennkaheksa_search_node_properties(nodeType: str, query: str, maxResults: Optional[int] = 20) -> Dict[str, Any]:
    """
    Search for specific properties within a node. Find authentication options, body parameters,
    headers, etc. without parsing the entire schema. Returns matching properties with their
    paths and descriptions.

    Args:
        nodeType (str): Full node type WITH prefix (same as get_node_info).
        query (str): Property name or keyword to search for. Examples: "auth", "header", "body", "json", "timeout".
        maxResults (Optional[int]): Maximum number of results to return. Default is 20.

    Returns:
        Dict containing:
        - matches (List[Dict]): List of matching properties with their configuration details,
          each containing 'name', 'displayName', 'type', 'description', 'path', 'required',
          'default', 'options', and 'showWhen' fields.
        - totalMatches (int): Total number of matched properties found.
        - searchedIn (str): Description of the scope or number of properties searched.

    Raises:
        ValueError: If nodeType or query is empty.
    """
    if not nodeType:
        raise ValueError("nodeType is required")
    if not query:
        raise ValueError("query is required")
    if maxResults is not None and maxResults <= 0:
        raise ValueError("maxResults must be a positive integer")

    # Call external API to get flat data
    api_data = call_external_api("ennkaheksa-search_node_properties")

    # Construct matches list from indexed flat fields
    matches: List[Dict[str, Any]] = []
    for i in range(2):  # We expect 2 items from the API
        name_key = f"match_{i}_name"
        if name_key not in api_data or api_data[name_key] is None:
            continue

        match = {
            "name": api_data[f"match_{i}_name"],
            "displayName": api_data[f"match_{i}_displayName"],
            "type": api_data[f"match_{i}_type"],
            "description": api_data[f"match_{i}_description"],
            "path": api_data[f"match_{i}_path"],
            "required": api_data[f"match_{i}_required"],
            "default": api_data[f"match_{i}_default"] if api_data[f"match_{i}_default"] != "" else None,
            "options": api_data[f"match_{i}_options"].split(",") if api_data[f"match_{i}_options"] else [],
            "showWhen": api_data[f"match_{i}_showWhen"] if api_data[f"match_{i}_showWhen"] else None
        }
        matches.append(match)

        # Respect maxResults limit
        if maxResults and len(matches) >= maxResults:
            break

    # Return final structured result
    return {
        "matches": matches,
        "totalMatches": api_data["totalMatches"],
        "searchedIn": api_data["searchedIn"]
    }