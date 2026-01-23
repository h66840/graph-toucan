from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for shadcn/ui component examples.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - example_0_title (str): Title of the first code example
        - example_0_code (str): Code snippet of the first example
        - example_0_description (str): Description of the first example
        - example_1_title (str): Title of the second code example
        - example_1_code (str): Code snippet of the second example
        - example_1_description (str): Description of the second example
    """
    return {
        "example_0_title": "Basic Button",
        "example_0_code": '<Button>Click me</Button>',
        "example_0_description": "A simple button with default styling.",
        "example_1_title": "Primary Button",
        "example_1_code": '<Button variant="primary">Submit</Button>',
        "example_1_description": "A primary button variant used for main actions."
    }

def shadcn_ui_component_reference_server_get_component_examples(componentName: str) -> Dict[str, Any]:
    """
    Get usage examples for a specific shadcn/ui component.
    
    Args:
        componentName (str): Name of the shadcn/ui component (e.g., "accordion", "button")
    
    Returns:
        Dict containing a list of code examples, each with 'title', 'code', and 'description' fields.
        
    Raises:
        ValueError: If componentName is empty or not a string
    """
    if not componentName:
        raise ValueError("componentName is required")
    if not isinstance(componentName, str):
        raise ValueError("componentName must be a string")
    
    # Fetch simulated external data
    api_data = call_external_api("shadcn/ui-component-reference-server-get_component_examples")
    
    # Construct the examples list from flattened API response
    examples = [
        {
            "title": api_data["example_0_title"],
            "code": api_data["example_0_code"],
            "description": api_data["example_0_description"]
        },
        {
            "title": api_data["example_1_title"],
            "code": api_data["example_1_code"],
            "description": api_data["example_1_description"]
        }
    ]
    
    return {"examples": examples}