from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for UI effects.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - effect_0_name (str): Name of the first effect
        - effect_0_type (str): Type of the first effect
        - effect_0_config_options (str): Configuration options for the first effect as JSON string
        - effect_0_code_snippet (str): Code snippet for the first effect
        - effect_0_supported_parameters (str): Supported parameters for the first effect as JSON string
        - effect_1_name (str): Name of the second effect
        - effect_1_type (str): Type of the second effect
        - effect_1_config_options (str): Configuration options for the second effect as JSON string
        - effect_1_code_snippet (str): Code snippet for the second effect
        - effect_1_supported_parameters (str): Supported parameters for the second effect as JSON string
        - total_effects (int): Total number of available effects
        - metadata_version (str): Version of the component server
        - metadata_documentation_url (str): URL to documentation
        - metadata_compatibility_notes (str): Compatibility notes for components
    """
    return {
        "effect_0_name": "animated-beam",
        "effect_0_type": "animation",
        "effect_0_config_options": '{"color": "#00ff00", "speed": 2, "thickness": 2}',
        "effect_0_code_snippet": '<AnimatedBeam color="#00ff00" speed={2} />',
        "effect_0_supported_parameters": '["color", "speed", "thickness", "duration"]',
        "effect_1_name": "border-beam",
        "effect_1_type": "decoration",
        "effect_1_config_options": '{"borderWidth": 3, "glowStrength": 0.8, "pulse": true}',
        "effect_1_code_snippet": '<BorderBeam borderWidth={3} glowStrength={0.8} pulse />',
        "effect_1_supported_parameters": '["borderWidth", "glowStrength", "pulse", "color"]',
        "total_effects": 8,
        "metadata_version": "1.5.2",
        "metadata_documentation_url": "https://magic-ui.dev/docs/components/effects",
        "metadata_compatibility_notes": "Compatible with React 18+ and Tailwind CSS"
    }

def magic_ui_component_server_getEffects() -> Dict[str, Any]:
    """
    Fetches implementation details for various magic UI component effects.

    Returns:
        Dict containing:
        - effects (List[Dict]): List of effect objects with name, type, config options,
          code snippets, and supported parameters
        - total_effects (int): Total number of available effects
        - metadata (Dict): Additional contextual information including version,
          documentation links, and compatibility notes
    """
    try:
        # Call simulated external API
        api_data = call_external_api("magic-ui-component-server-getEffects")

        # Construct effects list from indexed flat fields
        effects = [
            {
                "name": api_data["effect_0_name"],
                "type": api_data["effect_0_type"],
                "config_options": api_data["effect_0_config_options"],
                "code_snippet": api_data["effect_0_code_snippet"],
                "supported_parameters": api_data["effect_0_supported_parameters"]
            },
            {
                "name": api_data["effect_1_name"],
                "type": api_data["effect_1_type"],
                "config_options": api_data["effect_1_config_options"],
                "code_snippet": api_data["effect_1_code_snippet"],
                "supported_parameters": api_data["effect_1_supported_parameters"]
            }
        ]

        # Construct metadata
        metadata = {
            "version": api_data["metadata_version"],
            "documentation_url": api_data["metadata_documentation_url"],
            "compatibility_notes": api_data["metadata_compatibility_notes"]
        }

        # Build final result
        result = {
            "effects": effects,
            "total_effects": api_data["total_effects"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve effects data: {str(e)}") from e