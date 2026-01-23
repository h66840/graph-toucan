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
    Simulates fetching data from external API for Magic UI components.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - component_0_name (str): Name of the first UI component
        - component_0_type (str): Type of the first UI component
        - component_0_description (str): Description of the first UI component
        - component_1_name (str): Name of the second UI component
        - component_1_type (str): Type of the second UI component
        - component_1_description (str): Description of the second UI component
    """
    return {
        "component_0_name": "Button",
        "component_0_type": "interactive",
        "component_0_description": "A clickable button component for triggering actions.",
        "component_1_name": "Card",
        "component_1_type": "container",
        "component_1_description": "A container component for grouping related content."
    }

def magic_ui_component_server_getUIComponents() -> List[Dict[str, Optional[str]]]:
    """
    Provides a comprehensive list of all Magic UI components by querying an external API.

    Returns:
        List[Dict]: A list of UI components, each containing 'name', 'type', and optional 'description' fields.
                   Example:
                   [
                       {
                           "name": "Button",
                           "type": "interactive",
                           "description": "A clickable button component for triggering actions."
                       },
                       {
                           "name": "Card",
                           "type": "container",
                           "description": "A container component for grouping related content."
                       }
                   ]

    Raises:
        Exception: If there is an issue fetching data from the external API.
    """
    try:
        api_data = call_external_api("magic-ui-component-server-getUIComponents", **locals())

        components: List[Dict[str, Optional[str]]] = [
            {
                "name": api_data["component_0_name"],
                "type": api_data["component_0_type"],
                "description": api_data.get("component_0_description")
            },
            {
                "name": api_data["component_1_name"],
                "type": api_data["component_1_type"],
                "description": api_data.get("component_1_description")
            }
        ]

        return components

    except KeyError as e:
        raise Exception(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise Exception(f"Failed to retrieve UI components: {e}")

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
