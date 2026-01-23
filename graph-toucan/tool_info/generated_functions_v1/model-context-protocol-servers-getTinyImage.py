from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - image_description (str): Description of the image being presented
        - image_label (str): Label or title identifying the image content, specifically indicating it is the MCP tiny image
    """
    return {
        "image_description": "A minimalistic representation of the MCP architecture, showing core components in a compact form.",
        "image_label": "MCP Tiny Image"
    }

def model_context_protocol_servers_getTinyImage() -> Dict[str, str]:
    """
    Returns the MCP_TINY_IMAGE information including its description and label.
    
    This function retrieves data about the tiny image representation of the MCP system
    by querying an external API simulation and returning the structured response.
    
    Returns:
        Dict containing:
        - image_description (str): description of the image being presented
        - image_label (str): label or title identifying the image content, specifically indicating it is the MCP tiny image
    """
    try:
        # Fetch data from external API simulation
        api_data = call_external_api("model-context-protocol-servers-getTinyImage")
        
        # Construct result dictionary matching the output schema
        result = {
            "image_description": api_data["image_description"],
            "image_label": api_data["image_label"]
        }
        
        return result
        
    except KeyError as e:
        raise KeyError(f"Expected field missing in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"An error occurred while retrieving the MCP tiny image data: {str(e)}")