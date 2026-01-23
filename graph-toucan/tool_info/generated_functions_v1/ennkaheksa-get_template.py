from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for template retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - template_nodes_0_name (str): Name of the first node in the workflow
        - template_nodes_0_type (str): Type of the first node
        - template_nodes_0_position_0 (int): X coordinate of first node position
        - template_nodes_0_position_1 (int): Y coordinate of first node position
        - template_nodes_1_name (str): Name of the second node in the workflow
        - template_nodes_1_type (str): Type of the second node
        - template_nodes_1_position_0 (int): X coordinate of second node position
        - template_nodes_1_position_1 (int): Y coordinate of second node position
        - template_connections_node_0_source (str): Source node name for first connection
        - template_connections_node_0_destination (str): Destination node name for first connection
        - template_name (str): Name of the workflow template
        - template_version (str): Version of the template
        - template_createdAt (str): Creation timestamp in ISO format
        - templateId (int): Unique identifier of the template
        - success (bool): Whether retrieval was successful
        - error (str): Error message if any, otherwise null
        - metadata_category (str): Category of the template
        - metadata_author (str): Author of the template
        - metadata_description (str): Description of the template
        - metadata_compatibilityVersion (str): Compatible n8n version
        - metadata_tags_0 (str): First tag
        - metadata_tags_1 (str): Second tag
        - metadata_favoriteCount (int): Number of favorites
    """
    return {
        "template_nodes_0_name": "Start",
        "template_nodes_0_type": "n8n-nodes-base.start",
        "template_nodes_0_position_0": -200,
        "template_nodes_0_position_1": 0,
        "template_nodes_1_name": "HTTP Request",
        "template_nodes_1_type": "n8n-nodes-base.httpRequest",
        "template_nodes_1_position_0": 0,
        "template_nodes_1_position_1": 0,
        "template_connections_node_0_source": "Start",
        "template_connections_node_0_destination": "HTTP Request",
        "template_name": "Basic HTTP Workflow",
        "template_version": "1.0",
        "template_createdAt": "2023-10-05T14:48:00Z",
        "templateId": 12345,
        "success": True,
        "error": None,
        "metadata_category": "API",
        "metadata_author": "John Doe",
        "metadata_description": "A simple workflow that triggers an HTTP request.",
        "metadata_compatibilityVersion": "0.200.0",
        "metadata_tags_0": "http",
        "metadata_tags_1": "request",
        "metadata_favoriteCount": 42
    }

def ennkaheksa_get_template(templateId: int) -> Dict[str, Any]:
    """
    Retrieve a specific workflow template by its ID with complete JSON definition.
    
    This function simulates retrieving a full n8n workflow template including nodes,
    connections, metadata, and other properties. It returns a structured dictionary
    matching the expected output schema.
    
    Args:
        templateId (int): The unique identifier of the template to retrieve. Must be a positive integer.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - template (Dict): Full workflow definition with nodes, connections, name, version, createdAt
            - templateId (int): The requested template ID
            - success (bool): Whether the retrieval was successful
            - error (Optional[str]): Error message if failed, None otherwise
            - metadata (Dict): Additional info including category, author, description, compatibility version, tags, favoriteCount
    
    Raises:
        ValueError: If templateId is not a positive integer
    """
    # Input validation
    if not isinstance(templateId, int) or templateId <= 0:
        return {
            "template": {"nodes": [], "connections": {}, "name": "", "version": "", "createdAt": ""},
            "templateId": templateId,
            "success": False,
            "error": "Invalid templateId: must be a positive integer",
            "metadata": {}
        }

    try:
        # Fetch simulated external data
        api_data = call_external_api("ennkaheksa-get_template")
        
        # Construct nodes list
        nodes = [
            {
                "name": api_data["template_nodes_0_name"],
                "type": api_data["template_nodes_0_type"],
                "position": [
                    api_data["template_nodes_0_position_0"],
                    api_data["template_nodes_0_position_1"]
                ]
            },
            {
                "name": api_data["template_nodes_1_name"],
                "type": api_data["template_nodes_1_type"],
                "position": [
                    api_data["template_nodes_1_position_0"],
                    api_data["template_nodes_1_position_1"]
                ]
            }
        ]
        
        # Construct connections dictionary
        connections = {
            api_data["template_connections_node_0_source"]: {
                "main": [
                    [
                        {
                            "node": api_data["template_connections_node_0_destination"],
                            "type": "main"
                        }
                    ]
                ]
            }
        }
        
        # Construct metadata
        metadata = {
            "category": api_data["metadata_category"],
            "author": api_data["metadata_author"],
            "description": api_data["metadata_description"],
            "compatibilityVersion": api_data["metadata_compatibilityVersion"],
            "tags": [
                api_data["metadata_tags_0"],
                api_data["metadata_tags_1"]
            ],
            "favoriteCount": api_data["metadata_favoriteCount"]
        }
        
        # Construct final template object
        template = {
            "nodes": nodes,
            "connections": connections,
            "name": api_data["template_name"],
            "version": api_data["template_version"],
            "createdAt": api_data["template_createdAt"]
        }
        
        return {
            "template": template,
            "templateId": api_data["templateId"],
            "success": api_data["success"],
            "error": api_data["error"],
            "metadata": metadata
        }
        
    except Exception as e:
        return {
            "template": {"nodes": [], "connections": {}, "name": "", "version": "", "createdAt": ""},
            "templateId": templateId,
            "success": False,
            "error": f"Failed to retrieve template: {str(e)}",
            "metadata": {}
        }