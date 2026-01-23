from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for resource reference.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - uri (str): URI reference for accessing the resource
        - resource_description (str): Description or label of the referenced resource
    """
    # Simulate realistic URI and description based on tool name and static logic
    return {
        "uri": "https://mcp-server.example.com/resources/1",
        "resource_description": "Resource 1"
    }

def model_context_protocol_servers_getResourceReference(resourceId: int) -> Dict[str, Any]:
    """
    Returns a resource reference that can be used by MCP clients.

    Args:
        resourceId (int): ID of the resource to reference (1-100)

    Returns:
        Dict[str, Any]: A dictionary containing:
            - uri (str): URI reference for accessing the resource
            - resource_description (str): Description or label of the referenced resource

    Raises:
        ValueError: If resourceId is not in the valid range (1-100)
    """
    # Input validation
    if not isinstance(resourceId, int):
        raise ValueError("resourceId must be an integer")
    if resourceId < 1 or resourceId > 100:
        raise ValueError("resourceId must be between 1 and 100 inclusive")

    # Call external API (simulated) to get flat data
    api_data = call_external_api("model-context-protocol-servers-getResourceReference")

    # Construct the result using the resourceId to generate realistic values
    uri = f"https://mcp-server.example.com/resources/{resourceId}"
    resource_description = f"Resource {resourceId}"

    result = {
        "uri": uri,
        "resource_description": resource_description
    }

    return result