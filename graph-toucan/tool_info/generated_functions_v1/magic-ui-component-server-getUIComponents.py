from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
        api_data = call_external_api("magic-ui-component-server-getUIComponents")

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