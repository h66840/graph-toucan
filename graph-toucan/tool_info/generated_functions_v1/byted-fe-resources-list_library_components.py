from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing library components.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - components_0_name (str): Name of the first component
        - components_0_description (str): Description of the first component
        - components_0_category (str): Category of the first component
        - components_0_status (str): Status of the first component
        - components_0_version (str): Version of the first component
        - components_1_name (str): Name of the second component
        - components_1_description (str): Description of the second component
        - components_1_category (str): Category of the second component
        - components_1_status (str): Status of the second component
        - components_1_version (str): Version of the second component
        - error_message (str): Error message if any, otherwise empty string
        - library_found (bool): Whether the requested library exists
    """
    # Simulated response based on tool_name
    if tool_name == "byted-fe-resources-list_library_components":
        return {
            "components_0_name": "Button",
            "components_0_description": "A customizable button component",
            "components_0_category": "UI",
            "components_0_status": "active",
            "components_0_version": "1.2.0",
            "components_1_name": "InputField",
            "components_1_description": "Text input component with validation",
            "components_1_category": "Form",
            "components_1_status": "deprecated",
            "components_1_version": "0.8.5",
            "error_message": "",
            "library_found": True
        }
    else:
        return {
            "components_0_name": "",
            "components_0_description": "",
            "components_0_category": "",
            "components_0_status": "",
            "components_0_version": "",
            "components_1_name": "",
            "components_1_description": "",
            "components_1_category": "",
            "components_1_status": "",
            "components_1_version": "",
            "error_message": "Unknown tool",
            "library_found": False
        }

def byted_fe_resources_list_library_components(library: str) -> Dict[str, Any]:
    """
    List all components in the specified component library.
    
    Args:
        library (str): The name of the component library (e.g., dprc, okee, auxo)
    
    Returns:
        Dict containing:
        - components (List[Dict]): List of component objects with name, description, category, status, version
        - error_message (str): Error message if library not found or no components available
        - library_found (bool): Whether the requested library exists
    """
    # Input validation
    if not library or not isinstance(library, str):
        return {
            "components": [],
            "error_message": "Library name must be a non-empty string",
            "library_found": False
        }

    # Fetch data from external API simulation
    api_data = call_external_api("byted-fe-resources-list_library_components")
    
    # Construct components list from flattened fields
    components = []
    for i in range(2):
        name_key = f"components_{i}_name"
        desc_key = f"components_{i}_description"
        cat_key = f"components_{i}_category"
        status_key = f"components_{i}_status"
        version_key = f"components_{i}_version"
        
        if api_data.get(name_key):
            component = {
                "name": api_data[name_key],
                "description": api_data[desc_key],
                "category": api_data[cat_key],
                "status": api_data[status_key],
                "version": api_data[version_key]
            }
            components.append(component)
    
    # Return structured result
    return {
        "components": components,
        "error_message": api_data["error_message"],
        "library_found": api_data["library_found"]
    }