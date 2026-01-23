from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for node documentation.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_type (str): Full node type identifier with prefix
        - display_name (str): Human-readable name of the node
        - documentation (str): Markdown-formatted documentation content
        - has_documentation (bool): Whether documentation is available
    """
    return {
        "node_type": "nodes-base.httpRequest",
        "display_name": "HTTP Request",
        "documentation": (
            "# HTTP Request Node\n\n"
            "## Description\n"
            "Sends HTTP requests to external APIs.\n\n"
            "## Setup\n"
            "- Configure method, URL, headers, and body\n"
            "- Supports authentication via headers or credentials\n\n"
            "## Examples\n"
            "```json\n"
            "{\n"
            "  \"method\": \"GET\",\n"
            "  \"url\": \"https://api.example.com/data\"\n"
            "}\n"
            "```\n\n"
            "## Common Patterns\n"
            "- Use with JSON parsing nodes\n"
            "- Chain multiple requests using workflows\n"
        ),
        "has_documentation": True
    }

def ennkaheksa_get_node_documentation(nodeType: str) -> Dict[str, Any]:
    """
    Get human-readable documentation for a node. USE THIS BEFORE get_node_info!
    Returns markdown with explanations, examples, auth setup, and common patterns.
    Much easier to understand than raw schema. 87% of nodes have docs (returns 
    "No documentation available" otherwise). Same nodeType format as get_node_info.
    Best for understanding what a node does and how to use it.

    Args:
        nodeType (str): Full node type WITH prefix (same as get_node_info): 
                       "nodes-base.slack", "nodes-base.httpRequest", etc. CASE SENSITIVE!

    Returns:
        Dict[str, Any]: Dictionary containing:
            - nodeType (str): Full node type identifier with prefix
            - displayName (str): Human-readable name of the node
            - documentation (str): Full markdown-formatted documentation
            - hasDocumentation (bool): Whether documentation is available
    """
    if not nodeType or not isinstance(nodeType, str):
        raise ValueError("nodeType must be a non-empty string")

    api_data = call_external_api("ennkaheksa-get_node_documentation")
    
    # Construct result matching output schema
    result = {
        "nodeType": api_data["node_type"],
        "displayName": api_data["display_name"],
        "documentation": api_data["documentation"],
        "hasDocumentation": api_data["has_documentation"]
    }
    
    return result