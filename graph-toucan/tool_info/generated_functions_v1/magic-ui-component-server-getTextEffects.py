from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for text effect components.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - component_0_name (str): Name of the first UI text effect component
        - component_0_type (str): Type/category of the first component
        - component_0_description (str): Description of the first component
        - component_0_install (str): Installation instructions for the first component
        - component_0_content (str): Code/content example for the first component
        - component_0_examples (str): Example usage for the first component
        - component_1_name (str): Name of the second UI text effect component
        - component_1_type (str): Type/category of the second component
        - component_1_description (str): Description of the second component
        - component_1_install (str): Installation instructions for the second component
        - component_1_content (str): Code/content example for the second component
        - component_1_examples (str): Example usage for the second component
    """
    return {
        "component_0_name": "word-rotate",
        "component_0_type": "text-animation",
        "component_0_description": "Rotates through a list of words with smooth transitions.",
        "component_0_install": "npm install word-rotate-component",
        "component_0_content": "<WordRotate words={['Hello', 'World', 'Magic']} />",
        "component_0_examples": "Used in hero sections to highlight multiple features dynamically.",
        "component_1_name": "flip-text",
        "component_1_type": "text-effect",
        "component_1_description": "Flips text vertically like a card to reveal new content.",
        "component_1_install": "npm install flip-text-effect",
        "component_1_content": "<FlipText text='Amazing' />",
        "component_1_examples": "Ideal for interactive buttons and dynamic headlines."
    }

def magic_ui_component_server_getTextEffects() -> List[Dict[str, str]]:
    """
    Fetches and returns a list of UI text effect components with their implementation details.

    Returns:
        List[Dict]: A list of dictionaries, each representing a UI text effect component.
        Each dictionary contains the following keys:
        - name (str): Name of the component
        - type (str): Type/category of the component
        - description (str): Description of the component
        - install (str): Installation command or instructions
        - content (str): Sample code or content usage
        - examples (str): Example use cases or scenarios
    """
    try:
        api_data = call_external_api("magic-ui-component-server-getTextEffects")

        components = [
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

        return components

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing text effect components: {e}")