from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing image models.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - model_0 (str): Name of the first available image model
        - model_1 (str): Name of the second available image model
        - error (str): Error message if listing models failed, empty string if no error
    """
    return {
        "model_0": "stable-diffusion-v1-5",
        "model_1": "dall-e-3",
        "error": ""
    }

def mcpollinations_multimodal_server_listImageModels() -> Dict[str, Any]:
    """
    List available image models from the multimodal server.
    
    This function queries the external API to retrieve a list of available image generation models.
    It handles the transformation of flat API response into the required nested structure.
    
    Returns:
        Dict containing:
        - models (List[str]): List of available image model names
        - error (str): Error message if listing models failed, empty string if successful
    """
    try:
        api_data = call_external_api("mcpollinations-multimodal-server-listImageModels")
        
        # Construct the result following the output schema
        result = {
            "models": [
                api_data["model_0"],
                api_data["model_1"]
            ],
            "error": api_data["error"]
        }
        
        return result
    except KeyError as e:
        return {
            "models": [],
            "error": f"Missing expected data field: {str(e)}"
        }
    except Exception as e:
        return {
            "models": [],
            "error": f"Failed to list image models: {str(e)}"
        }