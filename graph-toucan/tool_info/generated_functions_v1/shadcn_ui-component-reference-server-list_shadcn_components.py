from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for shadcn/ui components.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - component_0_name (str): Name of the first UI component
        - component_0_description (str): Description of the first UI component
        - component_0_url (str): URL link to the first UI component documentation
        - component_1_name (str): Name of the second UI component
        - component_1_description (str): Description of the second UI component
        - component_1_url (str): URL link to the second UI component documentation
    """
    return {
        "component_0_name": "button",
        "component_0_description": "A customizable button component with support for variants and sizes.",
        "component_0_url": "https://ui.shadcn.com/docs/components/button",
        "component_1_name": "card",
        "component_1_description": "A container component used to group related information with a consistent style.",
        "component_1_url": "https://ui.shadcn.com/docs/components/card"
    }

def shadcn_ui_component_reference_server_list_shadcn_components() -> Dict[str, Any]:
    """
    Get a list of all available shadcn/ui components.

    Returns:
        Dict containing a single key 'components' which maps to a list of dictionaries.
        Each dictionary represents a UI component with keys:
        - name (str): The name of the component
        - description (str): A brief description of the component
        - url (str): The URL to the component's documentation page
    """
    try:
        # Fetch simulated external data
        api_data = call_external_api("shadcn/ui-component-reference-server-list_shadcn_components")

        # Construct the components list from flattened API response
        components = [
            {
                "name": api_data["component_0_name"],
                "description": api_data["component_0_description"],
                "url": api_data["component_0_url"]
            },
            {
                "name": api_data["component_1_name"],
                "description": api_data["component_1_description"],
                "url": api_data["component_1_url"]
            }
        ]

        return {"components": components}

    except KeyError as e:
        # Handle missing expected fields in API response
        raise RuntimeError(f"Missing required data in API response: {e}")
    except Exception as e:
        # Handle any other unforeseen errors
        raise RuntimeError(f"An error occurred while fetching shadcn/ui components: {e}")