from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugeicons platform usage.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - platform (str): Name of the platform
        - installation_core (str): Core installation command or package string
        - installation_packages_0 (str): First additional package required
        - installation_packages_1 (str): Second additional package required
        - basicUsage (str): Code example showing how to import and use icons
        - props_0_name (str): Name of the first component property
        - props_0_type (str): Type of the first component property
        - props_0_default (str): Default value of the first component property (optional)
        - props_0_description (str): Description of the first component property
        - props_1_name (str): Name of the second component property
        - props_1_type (str): Type of the second component property
        - props_1_default (str): Default value of the second component property (optional)
        - props_1_description (str): Description of the second component property
    """
    return {
        "platform": "react",
        "installation_core": "npm install hugeicons-react",
        "installation_packages_0": "hugeicons-react/core",
        "installation_packages_1": "hugeicons-react/outline",
        "basicUsage": "import { HeartIcon } from 'hugeicons-react';\n\nfunction App() {\n  return <HeartIcon />;\n}",
        "props_0_name": "size",
        "props_0_type": "string | number",
        "props_0_default": "24",
        "props_0_description": "The size of the icon in pixels",
        "props_1_name": "color",
        "props_1_type": "string",
        "props_1_default": "currentColor",
        "props_1_description": "The color of the icon"
    }

def hugeicons_mcp_server_get_platform_usage(platform: str) -> Dict[str, Any]:
    """
    Get platform-specific usage instructions for Hugeicons.

    Args:
        platform (str): Platform name (react, vue, angular, svelte, react-native, flutter)

    Returns:
        Dict containing:
        - platform (str): name of the platform for which usage instructions are provided
        - installation (Dict): contains 'core' (str) and 'packages' (List[str])
        - basicUsage (str): code example showing how to import and use the icons
        - props (List[Dict]): list of property objects with name, type, default, and description
    """
    # Validate input
    valid_platforms = ["react", "vue", "angular", "svelte", "react-native", "flutter"]
    if not platform:
        raise ValueError("Parameter 'platform' is required.")
    if platform not in valid_platforms:
        raise ValueError(f"Invalid platform '{platform}'. Must be one of {valid_platforms}.")

    # Fetch data from external API (simulated)
    api_data = call_external_api("hugeicons-mcp-server-get_platform_usage")

    # Construct nested output structure
    result = {
        "platform": api_data["platform"],
        "installation": {
            "core": api_data["installation_core"],
            "packages": [
                api_data["installation_packages_0"],
                api_data["installation_packages_1"]
            ]
        },
        "basicUsage": api_data["basicUsage"],
        "props": [
            {
                "name": api_data["props_0_name"],
                "type": api_data["props_0_type"],
                "default": api_data["props_0_default"],
                "description": api_data["props_0_description"]
            },
            {
                "name": api_data["props_1_name"],
                "type": api_data["props_1_type"],
                "default": api_data["props_1_default"],
                "description": api_data["props_1_description"]
            }
        ]
    }

    return result