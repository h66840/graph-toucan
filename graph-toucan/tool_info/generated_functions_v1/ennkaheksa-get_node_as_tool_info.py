from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for node tool information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_type (str): Full node type identifier with prefix
        - display_name (str): Display name of the node
        - description (str): Brief description of the node's purpose
        - package (str): Name of the package providing the node
        - is_marked_as_ai_tool (bool): Whether the node is explicitly marked as an AI tool
        - ai_tool_capabilities_can_be_used_as_tool (bool): Can the node be used as an AI tool
        - ai_tool_capabilities_has_usable_as_tool_property (bool): Has 'usableAsTool' property
        - ai_tool_capabilities_requires_environment_variable (bool): Requires env vars
        - ai_tool_capabilities_connection_type (str): Required connection type
        - ai_tool_capabilities_common_use_cases_0 (str): First common use case
        - ai_tool_capabilities_common_use_cases_1 (str): Second common use case
        - ai_tool_capabilities_requirements_connection (str): Connection requirement
        - ai_tool_capabilities_requirements_environment (str): Environment requirement
        - ai_tool_capabilities_examples_tool_name (str): Suggested tool name
        - ai_tool_capabilities_examples_tool_description (str): Tool description for AI
        - ai_tool_capabilities_examples_node_config_resource (str): Example resource
        - ai_tool_capabilities_examples_node_config_operation (str): Example operation
        - ai_tool_capabilities_tips_0 (str): First tip
        - ai_tool_capabilities_tips_1 (str): Second tip
    """
    return {
        "node_type": "nodes-base.slack",
        "display_name": "Slack",
        "description": "Send and receive messages from Slack channels and users",
        "package": "n8n-nodes-base",
        "is_marked_as_ai_tool": True,
        "ai_tool_capabilities_can_be_used_as_tool": True,
        "ai_tool_capabilities_has_usable_as_tool_property": True,
        "ai_tool_capabilities_requires_environment_variable": False,
        "ai_tool_capabilities_connection_type": "ai_tool",
        "ai_tool_capabilities_common_use_cases_0": "Notify team members about important events",
        "ai_tool_capabilities_common_use_cases_1": "Retrieve recent messages from a channel",
        "ai_tool_capabilities_requirements_connection": "Must have a valid Slack app credential with appropriate scopes",
        "ai_tool_capabilities_requirements_environment": "Slack app must be installed in the workspace",
        "ai_tool_capabilities_examples_tool_name": "send_slack_message",
        "ai_tool_capabilities_examples_tool_description": "Use this tool to send a message to a Slack channel or user when updates or alerts are needed",
        "ai_tool_capabilities_examples_node_config_resource": "message",
        "ai_tool_capabilities_examples_node_config_operation": "send",
        "ai_tool_capabilities_tips_0": "Use clear and concise messages that include context for recipients",
        "ai_tool_capabilities_tips_1": "Ensure the Slack app has necessary permissions for the target channels"
    }

def ennkaheksa_get_node_as_tool_info(nodeType: str) -> Dict[str, Any]:
    """
    Get specific information about using a node as an AI tool.
    
    This function retrieves detailed information about how a given node can be used
    as an AI tool, including capabilities, requirements, use cases, and configuration examples.
    It works for any node type, regardless of whether it's explicitly marked as an AI tool.
    
    Args:
        nodeType (str): Full node type WITH prefix: "nodes-base.slack", "nodes-base.googleSheets", etc.
    
    Returns:
        Dict containing comprehensive information about using the node as an AI tool:
        - nodeType (str): full node type identifier with prefix
        - displayName (str): display name of the node
        - description (str): brief description of the node's purpose
        - package (str): name of the package providing the node
        - isMarkedAsAITool (bool): whether the node is explicitly marked as an AI tool
        - aiToolCapabilities (Dict): contains all AI-related capabilities and usage details
          - canBeUsedAsTool (bool): indicates if the node can be used as an AI tool
          - hasUsableAsToolProperty (bool): whether the node has the 'usableAsTool' property defined
          - requiresEnvironmentVariable (bool): whether using this node as a tool requires environment variables
          - connectionType (str): required connection type for AI Agent integration
          - commonUseCases (List[str]): list of typical use cases when using this node as an AI tool
          - requirements (Dict): specifies setup requirements with 'connection' and 'environment' keys
          - examples (Dict): example configuration showing how to set up the tool
            - toolName (str): suggested name for the tool in AI Agent settings
            - toolDescription (str): natural language description for AI understanding
            - nodeConfig (Dict): sample node configuration with dynamic input mapping
          - tips (List[str]): best practice suggestions for configuring and using the node
    """
    # Input validation
    if not nodeType or not isinstance(nodeType, str) or "." not in nodeType:
        raise ValueError("nodeType must be a non-empty string with format 'package.node'")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("ennkaheksa-get_node_as_tool_info")
    
    # Construct nested structure matching output schema
    result = {
        "nodeType": api_data["node_type"],
        "displayName": api_data["display_name"],
        "description": api_data["description"],
        "package": api_data["package"],
        "isMarkedAsAITool": api_data["is_marked_as_ai_tool"],
        "aiToolCapabilities": {
            "canBeUsedAsTool": api_data["ai_tool_capabilities_can_be_used_as_tool"],
            "hasUsableAsToolProperty": api_data["ai_tool_capabilities_has_usable_as_tool_property"],
            "requiresEnvironmentVariable": api_data["ai_tool_capabilities_requires_environment_variable"],
            "connectionType": api_data["ai_tool_capabilities_connection_type"],
            "commonUseCases": [
                api_data["ai_tool_capabilities_common_use_cases_0"],
                api_data["ai_tool_capabilities_common_use_cases_1"]
            ],
            "requirements": {
                "connection": api_data["ai_tool_capabilities_requirements_connection"],
                "environment": api_data["ai_tool_capabilities_requirements_environment"]
            },
            "examples": {
                "toolName": api_data["ai_tool_capabilities_examples_tool_name"],
                "toolDescription": api_data["ai_tool_capabilities_examples_tool_description"],
                "nodeConfig": {
                    "resource": api_data["ai_tool_capabilities_examples_node_config_resource"],
                    "operation": api_data["ai_tool_capabilities_examples_node_config_operation"]
                }
            },
            "tips": [
                api_data["ai_tool_capabilities_tips_0"],
                api_data["ai_tool_capabilities_tips_1"]
            ]
        }
    }
    
    return result