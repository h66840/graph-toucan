from typing import Dict, Any, Optional
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for audio generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if audio generation failed, empty string otherwise
    """
    # Simulate occasional error for realism
    if random.random() < 0.1:  # 10% chance of error
        return {
            "error": "Audio generation failed due to invalid voice parameter"
        }
    else:
        return {
            "error": ""
        }

def mcpollinations_respondAudio(prompt: str, seed: Optional[int] = None, voice: str = "alloy") -> Dict[str, Any]:
    """
    Generate an audio response to a text prompt and play it through the system.
    
    Args:
        prompt (str): The text prompt to respond to with audio (required)
        seed (int, optional): Seed for reproducible results (default: random)
        voice (str, optional): Voice to use for audio generation (default: "alloy")
            Available options: "alloy", "echo", "fable", "onyx", "nova", "shimmer", 
            "coral", "verse", "ballad", "ash", "sage", "amuch", "dan"
    
    Returns:
        Dict[str, Any]: Dictionary containing:
            - error (str): error message describing why audio generation failed, 
              empty string if successful
    
    Raises:
        ValueError: If prompt is empty or voice is not in the allowed list
    """
    # Input validation
    if not prompt or not prompt.strip():
        return {"error": "Prompt is required and cannot be empty"}
    
    allowed_voices = [
        "alloy", "echo", "fable", "onyx", "nova", "shimmer", 
        "coral", "verse", "ballad", "ash", "sage", "amuch", "dan"
    ]
    
    if voice not in allowed_voices:
        return {"error": f"Voice '{voice}' is not supported. Use one of: {', '.join(allowed_voices)}"}
    
    # Set seed if provided
    if seed is not None:
        random.seed(seed)
    
    # Call external API simulation
    api_response = call_external_api("mcpollinations-respondAudio")
    
    # Construct result matching output schema
    result = {
        "error": api_response["error"]
    }
    
    return result