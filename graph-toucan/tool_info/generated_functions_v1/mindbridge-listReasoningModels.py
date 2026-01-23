from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - model_0_id (str): Identifier of the first reasoning model
        - model_1_id (str): Identifier of the second reasoning model
        - description (str): Description explaining that these models are optimized for reasoning tasks and support the reasoning_effort parameter
    """
    return {
        "model_0_id": "reasoning-model-pro-2024",
        "model_1_id": "reasoning-model-ultra-2023",
        "description": "These models are optimized for complex reasoning tasks and support the reasoning_effort parameter to control depth of thought."
    }

def mindbridge_listReasoningModels() -> Dict[str, Any]:
    """
    List all available models that support reasoning capabilities.
    
    This function retrieves a list of model identifiers that have reasoning capabilities
    and provides a description about their optimization for reasoning tasks and support
    for the reasoning_effort parameter.
    
    Returns:
        Dict containing:
        - models (List[str]): List of model identifiers that support reasoning capabilities
        - description (str): Description explaining that these models are optimized for reasoning tasks and support the reasoning_effort parameter
    """
    try:
        # Fetch data from external API (simulated)
        api_data = call_external_api("mindbridge-listReasoningModels")
        
        # Construct the result structure according to the output schema
        result = {
            "models": [
                api_data["model_0_id"],
                api_data["model_1_id"]
            ],
            "description": api_data["description"]
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields in API response
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")