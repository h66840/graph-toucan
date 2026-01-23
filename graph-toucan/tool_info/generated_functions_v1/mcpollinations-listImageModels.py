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

def mcpollinations_listImageModels() -> Dict[str, Any]:
    """
    List available image models from the MCPollinations service.
    
    This function retrieves a list of available image generation models
    by querying an external API and formatting the response according to
    the expected output schema.
    
    Returns:
        Dict containing:
        - models (List[str]): List of available image model names
        - error (str): Error message if listing models failed, empty string if successful
    """
    try:
        # Fetch data from external API
        api_data = call_external_api("mcpollinations-listImageModels")
        
        # Construct the result according to the output schema
        result: Dict[str, Any] = {
            "models": [],
            "error": api_data.get("error", "")
        }
        
        # Collect model names from indexed fields
        if "model_0" in api_data and api_data["model_0"]:
            result["models"].append(api_data["model_0"])
        if "model_1" in api_data and api_data["model_1"]:
            result["models"].append(api_data["model_1"])
            
        return result
        
    except Exception as e:
        # In case of any unexpected error, return error state
        return {
            "models": [],
            "error": f"Failed to list image models: {str(e)}"
        }