from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for text generation response.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - response_text (str): Generated text response to the input prompt
        - error_message (str): Error message if text generation fails; absent if successful
    """
    return {
        "response_text": "The quick brown fox jumps over the lazy dog. This is a randomly generated response based on the given prompt.",
        "error_message": ""
    }

def mcpollinations_multimodal_server_respondText(
    prompt: str,
    model: Optional[str] = "openai",
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Respond with text to a prompt using the Pollinations Text API.
    
    This function simulates interaction with an external text generation API.
    It generates a realistic text response based on the provided prompt and parameters.
    
    Args:
        prompt (str): The text prompt to generate a response for (required)
        model (str, optional): Model to use for text generation (default: "openai")
            Available options: "openai", "anthropic", "mistral", "llama", "gemini"
        seed (int, optional): Seed for reproducible results (default: random)
    
    Returns:
        Dict containing:
        - response_text (str): The generated text response to the input prompt
        - error_message (str, optional): Error message if generation fails; absent if successful
    
    Raises:
        ValueError: If required prompt is empty or None
    """
    # Input validation
    if not prompt or not prompt.strip():
        raise ValueError("Prompt is required and cannot be empty")
    
    # Validate model if provided
    valid_models = ["openai", "anthropic", "mistral", "llama", "gemini"]
    if model and model not in valid_models:
        raise ValueError(f"Invalid model: {model}. Must be one of {valid_models}")
    
    # Call external API simulation
    api_data = call_external_api("mcpollinations-multimodal-server-respondText")
    
    # Construct response matching output schema
    result: Dict[str, Any] = {
        "response_text": api_data["response_text"]
    }
    
    # Add error_message only if present in API response
    if api_data.get("error_message"):
        result["error_message"] = api_data["error_message"]
    
    return result