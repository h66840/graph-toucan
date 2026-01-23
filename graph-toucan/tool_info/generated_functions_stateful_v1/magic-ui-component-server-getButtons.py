from typing import Dict, List, Any

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
    Simulates fetching data from external API for UI button components.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - component_0_name (str): Name of the first button component
        - component_0_type (str): Type of the first button component
        - component_0_description (str): Description of the first button component
        - component_0_install (str): Installation instructions for the first button component
        - component_0_content (str): Implementation content for the first button component
        - component_0_examples (str): Example usage for the first button component
        - component_1_name (str): Name of the second button component
        - component_1_type (str): Type of the second button component
        - component_1_description (str): Description of the second button component
        - component_1_install (str): Installation instructions for the second button component
        - component_1_content (str): Implementation content for the second button component
        - component_1_examples (str): Example usage for the second button component
    """
    return {
        "component_0_name": "rainbow-button",
        "component_0_type": "animated-gradient",
        "component_0_description": "A colorful button with smooth rainbow gradient animation on hover.",
        "component_0_install": "npm install rainbow-button",
        "component_0_content": "<button class='rainbow-button'>Click Me</button>",
        "component_0_examples": "<rainbow-button>Submit</rainbow-button>",
        "component_1_name": "shimmer-button",
        "component_1_type": "shimmer-effect",
        "component_1_description": "A sleek button with a metallic shimmer effect that moves across the surface.",
        "component_1_install": "npm install shimmer-button",
        "component_1_content": "<button class='shimmer-button'>Hover Me</button>",
        "component_1_examples": "<shimmer-button>Learn More</shimmer-button>"
    }

def magic_ui_component_server_getButtons() -> Dict[str, Any]:
    """
    Fetches implementation details for various UI button components including rainbow-button,
    shimmer-button, shiny-button, interactive-hover-button, animated-subscribe-button,
    pulsating-button, and ripple-button.

    Returns:
        Dict containing a list of UI button components, each with 'name', 'type', 'description',
        'install', 'content', and 'examples' fields.
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("magic-ui-component-server-getButtons", **locals())

        # Construct the components list from flattened API data
        components: List[Dict[str, str]] = [
            {
                "name": api_data["component_0_name"],
                "type": api_data["component_0_type"],
                "description": api_data["component_0_description"],
                "install": api_data["component_0_install"],
                "content": api_data["component_0_content"],
                "examples": api_data["component_0_examples"]
            },
            {
                "name": api_data["component_1_name"],
                "type": api_data["component_1_type"],
                "description": api_data["component_1_description"],
                "install": api_data["component_1_install"],
                "content": api_data["component_1_content"],
                "examples": api_data["component_1_examples"]
            }
        ]

        # Return the structured result
        return {
            "components": components
        }

    except KeyError as e:
        # Handle missing keys in API response
        raise ValueError(f"Missing expected data in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unforeseen errors
        raise RuntimeError(f"An error occurred while fetching button components: {str(e)}") from e

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
