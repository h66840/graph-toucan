from typing import Dict, Any, Optional, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for shadcn/ui component details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Name of the shadcn/ui component
        - description (str): Brief description of the component
        - url (str): Official documentation URL
        - sourceUrl (str): GitHub repository URL for source code
        - installation (str): Installation command or instructions
        - usage (str): Code example or usage guidance
        - props_0_type (str): Type of the first prop/variant
        - props_0_description (str): Description of the first prop/variant
        - props_0_required (bool): Whether the first prop is required
        - props_0_example (str): Example value for the first prop
        - props_1_type (str): Type of the second prop/variant
        - props_1_description (str): Description of the second prop/variant
        - props_1_required (bool): Whether the second prop is required
        - props_1_example (str): Example value for the second prop
    """
    return {
        "name": "button",
        "description": "A customizable button component with multiple variants and sizes.",
        "url": "https://ui.shadcn.com/docs/components/button",
        "sourceUrl": "https://github.com/shadcn/ui/tree/main/components/button",
        "installation": "npx shadcn-ui add button",
        "usage": '<Button variant="default">Click me</Button>',
        "props_0_type": "string",
        "props_0_description": "Determines the visual variant of the button.",
        "props_0_required": False,
        "props_0_example": '"default" | "outline" | "secondary" | "destructive"',
        "props_1_type": "boolean",
        "props_1_description": "Disables the button when set to true.",
        "props_1_required": False,
        "props_1_example": "false"
    }

def shadcn_ui_component_reference_server_get_component_details(componentName: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific shadcn/ui component.
    
    Args:
        componentName (str): Name of the shadcn/ui component (e.g., "accordion", "button")
    
    Returns:
        Dict containing detailed information about the component:
        - name (str): name of the shadcn/ui component
        - description (str): brief description of the component's purpose and functionality
        - url (str): official documentation URL for the component
        - sourceUrl (str): GitHub repository URL where the component source code is located
        - installation (str): instructions or command to install the component
        - usage (str): code example or guidance on how to use the component in a project
        - props (Optional[Dict]): contains component variants or properties with their details
          including 'type', 'description', 'required', and 'example' fields
    """
    if not componentName or not isinstance(componentName, str):
        raise ValueError("componentName must be a non-empty string")
    
    # Fetch simulated external data
    api_data = call_external_api("shadcn/ui-component-reference-server-get_component_details")
    
    # Construct props list from indexed fields
    props = [
        {
            "type": api_data["props_0_type"],
            "description": api_data["props_0_description"],
            "required": api_data["props_0_required"],
            "example": api_data["props_0_example"]
        },
        {
            "type": api_data["props_1_type"],
            "description": api_data["props_1_description"],
            "required": api_data["props_1_required"],
            "example": api_data["props_1_example"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "name": api_data["name"],
        "description": api_data["description"],
        "url": api_data["url"],
        "sourceUrl": api_data["sourceUrl"],
        "installation": api_data["installation"],
        "usage": api_data["usage"],
        "props": {prop["type"]: prop for prop in props}  # Group by type as key
    }
    
    return result