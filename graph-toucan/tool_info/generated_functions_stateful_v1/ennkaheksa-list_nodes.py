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
    Simulates fetching data from external API for n8n nodes.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_0_nodeType (str): Node type identifier
        - node_0_displayName (str): Display name of the node
        - node_0_description (str): Description of the node
        - node_0_category (str): Category of the node (e.g., trigger, transform)
        - node_0_package (str): Package name (e.g., n8n-nodes-base)
        - node_0_developmentStyle (str): Implementation style (e.g., programmatic)
        - node_0_isAITool (bool): Whether the node can be used as an AI tool
        - node_0_isTrigger (bool): Whether the node is a trigger
        - node_0_isVersioned (bool): Whether the node supports versioning
        - node_1_nodeType (str): Second node's type identifier
        - node_1_displayName (str): Second node's display name
        - node_1_description (str): Second node's description
        - node_1_category (str): Second node's category
        - node_1_package (str): Second node's package name
        - node_1_developmentStyle (str): Second node's development style
        - node_1_isAITool (bool): Whether second node is usable as AI tool
        - node_1_isTrigger (bool): Whether second node is a trigger
        - node_1_isVersioned (bool): Whether second node is versioned
        - totalCount (int): Total number of nodes returned
    """
    return {
        "node_0_nodeType": "n8n-nodes-base.httpRequest",
        "node_0_displayName": "HTTP Request",
        "node_0_description": "Sends HTTP requests to any API",
        "node_0_category": "input",
        "node_0_package": "n8n-nodes-base",
        "node_0_developmentStyle": "programmatic",
        "node_0_isAITool": False,
        "node_0_isTrigger": False,
        "node_0_isVersioned": True,
        "node_1_nodeType": "n8n-nodes-base.manualTrigger",
        "node_1_displayName": "Manual Trigger",
        "node_1_description": "Triggers workflow manually",
        "node_1_category": "trigger",
        "node_1_package": "n8n-nodes-base",
        "node_1_developmentStyle": "programmatic",
        "node_1_isAITool": True,
        "node_1_isTrigger": True,
        "node_1_isVersioned": True,
        "totalCount": 2
    }

def ennkaheksa_list_nodes(
    category: Optional[str] = None,
    developmentStyle: Optional[str] = None,
    isAITool: Optional[bool] = None,
    limit: Optional[int] = 50,
    package: Optional[str] = None
) -> Dict[str, Any]:
    """
    List n8n nodes with optional filters.

    Args:
        category (Optional[str]): Filter by single category: "trigger", "transform", "output", "input", or "AI".
        developmentStyle (Optional[str]): Filter by implementation type (e.g., "programmatic").
        isAITool (Optional[bool]): Filter by whether node is usable as AI tool.
        limit (Optional[int]): Limit number of results (default 50, max 500).
        package (Optional[str]): Filter by exact package name (e.g., "n8n-nodes-base").

    Returns:
        Dict containing:
        - nodes (List[Dict]): List of node objects with fields: nodeType, displayName, description,
          category, package, developmentStyle, isAITool, isTrigger, isVersioned
        - totalCount (int): Total number of nodes returned

    Note:
        Use limit >= 200 for more complete results. Default 50 may miss nodes.
        Use exact package names: 'n8n-nodes-base' not '@n8n/n8n-nodes-base'.
    """
    # Validate inputs
    if limit is not None and (limit < 1 or limit > 500):
        raise ValueError("limit must be between 1 and 500")

    if category is not None and category not in ["trigger", "transform", "output", "input", "AI"]:
        raise ValueError("category must be one of: trigger, transform, output, input, AI")

    if package is not None and package not in ["n8n-nodes-base", "@n8n/n8n-nodes-langchain"]:
        raise ValueError("package must be 'n8n-nodes-base' or '@n8n/n8n-nodes-langchain'")

    # Fetch simulated external data
    api_data = call_external_api("ennkaheksa-list_nodes", **locals())

    # Construct nodes list from flattened API response
    nodes = []
    for i in range(2):  # We have two simulated nodes
        node_key_prefix = f"node_{i}"
        node = {
            "nodeType": api_data.get(f"{node_key_prefix}_nodeType"),
            "displayName": api_data.get(f"{node_key_prefix}_displayName"),
            "description": api_data.get(f"{node_key_prefix}_description"),
            "category": api_data.get(f"{node_key_prefix}_category"),
            "package": api_data.get(f"{node_key_prefix}_package"),
            "developmentStyle": api_data.get(f"{node_key_prefix}_developmentStyle"),
            "isAITool": api_data.get(f"{node_key_prefix}_isAITool"),
            "isTrigger": api_data.get(f"{node_key_prefix}_isTrigger"),
            "isVersioned": api_data.get(f"{node_key_prefix}_isVersioned")
        }
        # Apply filtering
        if category is not None and node["category"] != category:
            continue
        if developmentStyle is not None and node["developmentStyle"] != developmentStyle:
            continue
        if isAITool is not None and node["isAITool"] != isAITool:
            continue
        if package is not None and node["package"] != package:
            continue
        nodes.append(node)
        if limit is not None and len(nodes) >= limit:
            break

    return {
        "nodes": nodes,
        "totalCount": len(nodes)
    }

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
