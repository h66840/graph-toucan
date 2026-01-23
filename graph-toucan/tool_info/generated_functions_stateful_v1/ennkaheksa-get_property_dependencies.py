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
    Simulates fetching data from external API for property dependency analysis.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - node_type (str): Node type identifier
        - display_name (str): User-friendly name of the node
        - total_properties (int): Total number of properties
        - properties_with_dependencies (int): Number of properties with visibility dependencies
        - dependency_0_property (str): Dependent property name
        - dependency_0_display_name (str): Display name of dependent property
        - dependency_0_depends_on (str): Property it depends on
        - dependency_0_show_when (str): Condition to show (e.g., "true")
        - dependency_0_hide_when (str): Condition to hide (optional)
        - dependency_0_notes (str): Additional notes
        - dependency_0_enables_properties (str): Comma-separated list of enabled properties
        - dependency_1_property (str): Second dependent property name
        - dependency_1_display_name (str): Display name of second dependent property
        - dependency_1_depends_on (str): Property it depends on
        - dependency_1_show_when (str): Condition to show
        - dependency_1_hide_when (str): Condition to hide (optional)
        - dependency_1_notes (str): Additional notes
        - dependency_1_enables_properties (str): Comma-separated list of enabled properties
        - dependency_graph_control_0 (str): Controlling property
        - dependency_graph_dependent_0 (str): First property it controls
        - dependency_graph_dependent_1 (str): Second property it controls
        - suggestion_0 (str): First suggestion
        - suggestion_1 (str): Second suggestion
    """
    return {
        "node_type": "nodes-base.httpRequest",
        "display_name": "HTTP Request",
        "total_properties": 24,
        "properties_with_dependencies": 8,
        "dependency_0_property": "bodyContent",
        "dependency_0_display_name": "Body Content",
        "dependency_0_depends_on": "sendBody",
        "dependency_0_show_when": "true",
        "dependency_0_hide_when": "false",
        "dependency_0_notes": "Only shown when sendBody is enabled",
        "dependency_0_enables_properties": "contentType,headers",
        "dependency_1_property": "timeout",
        "dependency_1_display_name": "Timeout (ms)",
        "dependency_1_depends_on": "useCustomTimeout",
        "dependency_1_show_when": "true",
        "dependency_1_hide_when": "false",
        "dependency_1_notes": "Appears when custom timeout is selected",
        "dependency_1_enables_properties": "",
        "dependency_graph_control_0": "sendBody",
        "dependency_graph_dependent_0": "bodyContent",
        "dependency_graph_dependent_1": "contentType",
        "suggestion_0": "Set 'sendBody' early to reveal body configuration options",
        "suggestion_1": "Consider default timeout unless specific needs exist"
    }

def ennkaheksa_get_property_dependencies(nodeType: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Analyzes property visibility dependencies for a given node type.
    
    Args:
        nodeType (str): The node type to analyze (e.g., "nodes-base.httpRequest")
        config (Optional[Dict[str, Any]]): Optional partial configuration to check visibility impact
        
    Returns:
        Dict containing:
        - nodeType (str): the node type identifier
        - displayName (str): user-friendly name of the node
        - totalProperties (int): total number of properties
        - propertiesWithDependencies (int): number of properties with dependencies
        - dependencies (List[Dict]): list of dependency objects with property, displayName, 
          dependsOn, showWhen, hideWhen, notes, and enablesProperties
        - dependencyGraph (Dict): mapping from controlling properties to lists of dependent properties
        - suggestions (List[str]): helpful suggestions about configuration
        
    Example:
        >>> result = ennkaheksa_get_property_dependencies("nodes-base.httpRequest")
        >>> print(result["dependencies"][0]["property"])
        'bodyContent'
    """
    if not nodeType:
        raise ValueError("nodeType is required")
    
    # Fetch data from simulated external API
    api_data = call_external_api("ennkaheksa-get_property_dependencies", **locals())
    
    # Construct dependencies list from indexed fields
    dependencies = [
        {
            "property": api_data["dependency_0_property"],
            "displayName": api_data["dependency_0_display_name"],
            "dependsOn": api_data["dependency_0_depends_on"],
            "showWhen": api_data["dependency_0_show_when"],
            "hideWhen": api_data.get("dependency_0_hide_when"),
            "notes": api_data["dependency_0_notes"],
            "enablesProperties": [
                p.strip() for p in api_data["dependency_0_enables_properties"].split(",") 
                if p.strip()
            ]
        },
        {
            "property": api_data["dependency_1_property"],
            "displayName": api_data["dependency_1_display_name"],
            "dependsOn": api_data["dependency_1_depends_on"],
            "showWhen": api_data["dependency_1_show_when"],
            "hideWhen": api_data.get("dependency_1_hide_when"),
            "notes": api_data["dependency_1_notes"],
            "enablesProperties": [
                p.strip() for p in api_data["dependency_1_enables_properties"].split(",") 
                if p.strip()
            ]
        }
    ]
    
    # Construct dependency graph
    control_prop = api_data["dependency_graph_control_0"]
    dependency_graph = {
        control_prop: [
            api_data["dependency_graph_dependent_0"],
            api_data["dependency_graph_dependent_1"]
        ]
    }
    
    # Construct suggestions list
    suggestions = [
        api_data["suggestion_0"],
        api_data["suggestion_1"]
    ]
    
    # Build final result matching output schema
    result = {
        "nodeType": api_data["node_type"],
        "displayName": api_data["display_name"],
        "totalProperties": api_data["total_properties"],
        "propertiesWithDependencies": api_data["properties_with_dependencies"],
        "dependencies": dependencies,
        "dependencyGraph": dependency_graph,
        "suggestions": suggestions
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
