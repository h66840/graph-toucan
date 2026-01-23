from typing import Dict, List, Any, Optional
import json

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching node essentials data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_type (str): Full node type identifier
        - display_name (str): User-friendly name of the node
        - description (str): Brief explanation of node's purpose
        - category (str): Functional category (e.g., "trigger", "output")
        - version (float): Version number of the node
        - is_versioned (bool): Whether node supports versioning
        - required_property_0_name (str): First required property name
        - required_property_0_display_name (str): First required property display name
        - required_property_0_type (str): First required property type
        - required_property_0_description (str): First required property description
        - required_property_0_required (bool): Whether first required property is required
        - required_property_0_default (str): Default value for first required property
        - required_property_0_usage_hint (str): Usage hint for first required property
        - required_property_1_name (str): Second required property name
        - required_property_1_display_name (str): Second required property display name
        - required_property_1_type (str): Second required property type
        - required_property_1_description (str): Second required property description
        - required_property_1_required (bool): Whether second required property is required
        - common_property_0_name (str): First common property name
        - common_property_0_display_name (str): First common property display name
        - common_property_0_type (str): First common property type
        - common_property_0_description (str): First common property description
        - common_property_0_required (bool): Whether first common property is required
        - common_property_1_name (str): Second common property name
        - common_property_1_display_name (str): Second common property display name
        - common_property_1_type (str): Second common property type
        - common_property_1_description (str): Second common property description
        - operation_0_name (str): First operation name
        - operation_0_description (str): First operation description
        - operation_1_name (str): Second operation name
        - operation_1_description (str): Second operation description
        - example_minimal (str): Minimal example config as JSON string
        - example_common (str): Common example config as JSON string
        - example_advanced (str): Advanced example config as JSON string
        - total_properties (int): Total number of properties
        - is_ai_tool (bool): Whether node is an AI tool
        - is_trigger (bool): Whether node is a trigger
        - is_webhook (bool): Whether node is a webhook
        - has_credentials (bool): Whether node requires credentials
        - package (str): Package name
        - development_style (str): Development style (e.g., "standard", "express")
    """
    return {
        "node_type": "nodes-base.httpRequest",
        "display_name": "HTTP Request",
        "description": "Sends an HTTP request to a specified URL",
        "category": "output",
        "version": 1.3,
        "is_versioned": True,
        "required_property_0_name": "url",
        "required_property_0_display_name": "URL",
        "required_property_0_type": "string",
        "required_property_0_description": "The URL to send the request to",
        "required_property_0_required": True,
        "required_property_0_default": "https://api.example.com",
        "required_property_0_usage_hint": "Enter full URL including protocol",
        "required_property_1_name": "method",
        "required_property_1_display_name": "Method",
        "required_property_1_type": "options",
        "required_property_1_description": "HTTP method to use",
        "required_property_1_required": True,
        "common_property_0_name": "headers",
        "common_property_0_display_name": "Headers",
        "common_property_0_type": "object",
        "common_property_0_description": "Custom headers to send",
        "common_property_0_required": False,
        "common_property_1_name": "body",
        "common_property_1_display_name": "Body",
        "common_property_1_type": "string",
        "common_property_1_description": "Request body content",
        "common_property_1_required": False,
        "operation_0_name": "send",
        "operation_0_description": "Send the HTTP request",
        "operation_1_name": "test",
        "operation_1_description": "Test connection",
        "example_minimal": '{"url": "https://api.example.com", "method": "GET"}',
        "example_common": '{"url": "https://api.example.com/users", "method": "POST", "body": "{\\"name\\": \\"John\\"}"}',
        "example_advanced": '{"url": "https://api.example.com/users", "method": "POST", "headers": {"Authorization": "Bearer xyz"}, "body": "{\\"name\\": \\"John\\", \\"age\\": 30}"}',
        "total_properties": 25,
        "is_ai_tool": False,
        "is_trigger": False,
        "is_webhook": False,
        "has_credentials": False,
        "package": "n8n-nodes-base",
        "development_style": "standard"
    }

def ennkaheksa_get_node_essentials(nodeType: str) -> Dict[str, Any]:
    """
    Get only the 10-20 most important properties for a node (95% size reduction).
    USE THIS INSTEAD OF get_node_info for basic configuration!
    
    Args:
        nodeType (str): Full node type WITH prefix: "nodes-base.httpRequest", "nodes-base.webhook", etc.
    
    Returns:
        Dict containing:
        - nodeType (str): full node type identifier with prefix
        - displayName (str): user-friendly name of the node
        - description (str): brief explanation of the node's purpose
        - category (str): functional category of the node
        - version (float or int): version number of the node
        - isVersioned (bool): whether the node supports versioning
        - requiredProperties (List[Dict]): list of essential configuration properties
        - commonProperties (List[Dict]): list of frequently used but non-essential properties
        - operations (List[Dict]): list of available operations for the node
        - examples (Dict): sample configurations showing minimal, common, and advanced usage
        - metadata (Dict): additional metadata about the node
    """
    if not nodeType or not isinstance(nodeType, str):
        raise ValueError("nodeType must be a non-empty string")
    
    api_data = call_external_api("ennkaheksa_get_node_essentials")
    
    required_properties = [
        {
            "name": api_data["required_property_0_name"],
            "displayName": api_data["required_property_0_display_name"],
            "type": api_data["required_property_0_type"],
            "description": api_data["required_property_0_description"],
            "required": api_data["required_property_0_required"],
            "default": api_data.get("required_property_0_default"),
            "usageHint": api_data.get("required_property_0_usage_hint")
        },
        {
            "name": api_data["required_property_1_name"],
            "displayName": api_data["required_property_1_display_name"],
            "type": api_data["required_property_1_type"],
            "description": api_data["required_property_1_description"],
            "required": api_data["required_property_1_required"]
        }
    ]
    
    common_properties = [
        {
            "name": api_data["common_property_0_name"],
            "displayName": api_data["common_property_0_display_name"],
            "type": api_data["common_property_0_type"],
            "description": api_data["common_property_0_description"],
            "required": api_data["common_property_0_required"]
        },
        {
            "name": api_data["common_property_1_name"],
            "displayName": api_data["common_property_1_display_name"],
            "type": api_data["common_property_1_type"],
            "description": api_data["common_property_1_description"],
            "required": api_data["common_property_1_required"]
        }
    ]
    
    operations = [
        {
            "name": api_data["operation_0_name"],
            "description": api_data["operation_0_description"]
        },
        {
            "name": api_data["operation_1_name"],
            "description": api_data["operation_1_description"]
        }
    ]
    
    examples = {
        "minimal": json.loads(api_data["example_minimal"]),
        "common": json.loads(api_data["example_common"]),
        "advanced": json.loads(api_data["example_advanced"])
    }
    
    metadata = {
        "totalProperties": api_data["total_properties"],
        "isAITool": api_data["is_ai_tool"],
        "isTrigger": api_data["is_trigger"],
        "isWebhook": api_data["is_webhook"],
        "hasCredentials": api_data["has_credentials"],
        "package": api_data["package"],
        "developmentStyle": api_data["development_style"]
    }
    
    return {
        "nodeType": nodeType,
        "displayName": api_data["display_name"],
        "description": api_data["description"],
        "category": api_data["category"],
        "version": api_data["version"],
        "isVersioned": api_data["is_versioned"],
        "requiredProperties": required_properties,
        "commonProperties": common_properties,
        "operations": operations,
        "examples": examples,
        "metadata": metadata
    }