from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for UI text reveal components.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - component_0_name (str): Name of the first UI component
        - component_0_type (str): Type of the first UI component
        - component_0_description (str): Description of the first UI component
        - component_0_install (str): Installation command for the first component
        - component_0_content (str): Code content for the first component
        - component_0_examples (str): Example usage for the first component
        - component_1_name (str): Name of the second UI component
        - component_1_type (str): Type of the second UI component
        - component_1_description (str): Description of the second UI component
        - component_1_install (str): Installation command for the second component
        - component_1_content (str): Code content for the second component
        - component_1_examples (str): Example usage for the second component
    """
    return {
        "component_0_name": "text-reveal",
        "component_0_type": "animation",
        "component_0_description": "A smooth text reveal animation that appears on scroll or mount.",
        "component_0_install": "npm install @ui/text-reveal",
        "component_0_content": "<div class=\"text-reveal\"><span>Revealing Text</span></div>",
        "component_0_examples": "<TextReveal text=\"Hello World\" delay={0.5} />",
        "component_1_name": "typing-animation",
        "component_1_type": "animation",
        "component_1_description": "Simulates typing effect with cursor blink for dynamic text display.",
        "component_1_install": "npm install @ui/typing-animation",
        "component_1_content": "<div class=\"typing-container\"><p class=\"typing-text\"></p><span class=\"cursor\">|</span></div>",
        "component_1_examples": "<TypingAnimation text=\"Welcome!\" speed={50} />"
    }

def magic_ui_component_server_getTextReveal() -> List[Dict[str, Any]]:
    """
    Fetches and returns implementation details for various text animation UI components.

    Returns:
        List[Dict]: A list of dictionaries containing UI component details with keys:
            - name (str): Component name
            - type (str): Component category/type
            - description (str): Brief description of the component
            - install (str): Package installation command
            - content (str): Sample HTML/JSX code snippet
            - examples (str): Usage example
    """
    try:
        # Fetch flattened data from simulated external API
        api_data = call_external_api("magic-ui-component-server-getTextReveal")

        # Construct the result list by mapping flat fields to nested structure
        components: List[Dict[str, Any]] = [
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
        # Handle missing expected keys in API response
        raise KeyError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unforeseen errors
        raise RuntimeError(f"An error occurred while fetching component data: {str(e)}") from e