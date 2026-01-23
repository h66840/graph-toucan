from typing import Dict, List, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for node schema information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_schema_str (str): JSON string representation of the full node schema
        - ai_tool_capabilities_str (str): JSON string of AI tool capabilities
        - required_properties_0_name (str): First required property name
        - required_properties_0_type (str): Type of first required property
        - required_properties_0_description (str): Description of first required property
        - required_properties_1_name (str): Second required property name
        - required_properties_1_type (str): Type of second required property
        - required_properties_1_description (str): Description of second required property
        - simple_properties_0_name (str): First simple property name
        - simple_properties_0_type (str): Type of first simple property
        - simple_properties_0_description (str): Description of first simple property
        - simple_properties_1_name (str): Second simple property name
        - simple_properties_1_type (str): Type of second simple property
        - simple_properties_1_description (str): Description of second simple property
        - credentials_0_name (str): First credential name
        - credentials_0_auth_type (str): Authentication method for first credential
        - credentials_0_notes (str): Notes or scopes for first credential
        - credentials_1_name (str): Second credential name
        - credentials_1_auth_type (str): Authentication method for second credential
        - credentials_1_notes (str): Notes or scopes for second credential
        - operations_0_operation (str): Identifier of first operation
        - operations_0_label (str): Label of first operation
        - operations_0_description (str): Description of first operation
        - operations_1_operation (str): Identifier of second operation
        - operations_1_label (str): Label of second operation
        - operations_1_description (str): Description of second operation
        - version (str): Node version identifier
        - node_type (str): Full node type with prefix (e.g., "nodes-base.httpRequest")
        - has_conditional_logic (bool): Whether node has display conditionals
        - raw_size_kb (int): Approximate size of raw JSON in KB
    """
    return {
        "node_schema_str": '{"name":"httpRequest","type":"nodes-base.httpRequest","version":1,"properties":[]}',
        "ai_tool_capabilities_str": '{"enabled":true,"inputFormat":"json","outputFormat":"json"}',
        "required_properties_0_name": "url",
        "required_properties_0_type": "string",
        "required_properties_0_description": "The URL to send the request to",
        "required_properties_1_name": "method",
        "required_properties_1_type": "options",
        "required_properties_1_description": "HTTP method to use",
        "simple_properties_0_name": "timeout",
        "simple_properties_0_type": "number",
        "simple_properties_0_description": "Request timeout in seconds",
        "simple_properties_1_name": "followRedirects",
        "simple_properties_1_type": "boolean",
        "simple_properties_1_description": "Whether to follow HTTP redirects",
        "credentials_0_name": "httpBasicAuth",
        "credentials_0_auth_type": "username+password",
        "credentials_0_notes": "Basic HTTP authentication",
        "credentials_1_name": "apiKey",
        "credentials_1_auth_type": "header",
        "credentials_1_notes": "API key in header",
        "operations_0_operation": "GET",
        "operations_0_label": "GET Request",
        "operations_0_description": "Retrieve data from a URL",
        "operations_1_operation": "POST",
        "operations_1_label": "POST Request",
        "operations_1_description": "Send data to a URL",
        "version": "1.2.3",
        "node_type": "nodes-base.httpRequest",
        "has_conditional_logic": True,
        "raw_size_kb": 156
    }

def ennkaheksa_get_node_info(nodeType: str) -> Dict[str, Any]:
    """
    Get COMPLETE technical schema for a node. WARNING: Returns massive JSON (often 100KB+) 
    with all properties, operations, credentials. Contains duplicates and complex conditional logic.
    
    TIPS: 
    1) Use get_node_essentials first for common use cases
    2) Try get_node_documentation for human-readable info
    3) Look for "required":true properties
    4) Find properties without "displayOptions" for simpler versions
    
    Node type MUST include prefix: "nodes-base.httpRequest" NOT "httpRequest".
    NOW INCLUDES: aiToolCapabilities section showing how to use any node as an AI tool.
    
    Args:
        nodeType (str): FULL node type with prefix. Format: "nodes-base.{name}" or "nodes-langchain.{name}".
                       CASE SENSITIVE! Examples: "nodes-base.httpRequest", "nodes-langchain.agent"
    
    Returns:
        Dict containing:
        - nodeSchema (Dict): Complete technical schema of the node
        - aiToolCapabilities (Dict): How the node can be used as an AI tool
        - requiredProperties (List[Dict]): Subset of required properties
        - simpleProperties (List[Dict]): Properties without displayOptions (always visible)
        - credentials (List[Dict]): List of credential types required/supported
        - operations (List[Dict]): Available operations/actions
        - version (str): Version identifier
        - nodeType (str): Full node type (echoed from input)
        - hasConditionalLogic (bool): Whether schema contains complex conditional rules
        - rawSizeKB (int): Approximate size of JSON payload in KB
    """
    # Input validation
    if not nodeType:
        raise ValueError("nodeType is required")
    
    if not isinstance(nodeType, str):
        raise TypeError("nodeType must be a string")
    
    if not nodeType.startswith("nodes-base.") and not nodeType.startswith("nodes-langchain."):
        raise ValueError("nodeType must start with 'nodes-base.' or 'nodes-langchain.' prefix")
    
    # Call external API (simulated)
    api_data = call_external_api("ennkaheksa-get_node_info", **locals())
    
    # Construct requiredProperties list
    required_properties = [
        {
            "name": api_data["required_properties_0_name"],
            "type": api_data["required_properties_0_type"],
            "description": api_data["required_properties_0_description"]
        },
        {
            "name": api_data["required_properties_1_name"],
            "type": api_data["required_properties_1_type"],
            "description": api_data["required_properties_1_description"]
        }
    ]
    
    # Construct simpleProperties list
    simple_properties = [
        {
            "name": api_data["simple_properties_0_name"],
            "type": api_data["simple_properties_0_type"],
            "description": api_data["simple_properties_0_description"]
        },
        {
            "name": api_data["simple_properties_1_name"],
            "type": api_data["simple_properties_1_type"],
            "description": api_data["simple_properties_1_description"]
        }
    ]
    
    # Construct credentials list
    credentials = [
        {
            "name": api_data["credentials_0_name"],
            "authType": api_data["credentials_0_auth_type"],
            "notes": api_data["credentials_0_notes"]
        },
        {
            "name": api_data["credentials_1_name"],
            "authType": api_data["credentials_1_auth_type"],
            "notes": api_data["credentials_1_notes"]
        }
    ]
    
    # Construct operations list
    operations = [
        {
            "operation": api_data["operations_0_operation"],
            "label": api_data["operations_0_label"],
            "description": api_data["operations_0_description"]
        },
        {
            "operation": api_data["operations_1_operation"],
            "label": api_data["operations_1_label"],
            "description": api_data["operations_1_description"]
        }
    ]
    
    # Parse JSON strings into dicts
    import json
    try:
        node_schema = json.loads(api_data["node_schema_str"])
    except json.JSONDecodeError:
        node_schema = {"error": "Failed to parse node schema JSON"}
    
    try:
        ai_tool_capabilities = json.loads(api_data["ai_tool_capabilities_str"])
    except json.JSONDecodeError:
        ai_tool_capabilities = {"error": "Failed to parse AI tool capabilities JSON"}
    
    # Build final result
    result = {
        "nodeSchema": node_schema,
        "aiToolCapabilities": ai_tool_capabilities,
        "requiredProperties": required_properties,
        "simpleProperties": simple_properties,
        "credentials": credentials,
        "operations": operations,
        "version": api_data["version"],
        "nodeType": api_data["node_type"],
        "hasConditionalLogic": api_data["has_conditional_logic"],
        "rawSizeKB": api_data["raw_size_kb"]
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
