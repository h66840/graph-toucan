from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for audio response generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if audio generation failed, empty if successful
        - status (str): Status of the audio generation request, e.g., "success" or "error"
    """
    # Simulate success by default unless some condition is met (e.g., invalid voice)
    return {
        "error": "",
        "status": "success"
    }

def mcpollinations_multimodal_server_respondAudio(prompt: str, seed: Optional[int] = None, voice: Optional[str] = "alloy") -> Dict[str, Any]:
    """
    Generate an audio response to a text prompt and simulate playing it through the system.
    
    Args:
        prompt (str): The text prompt to respond to with audio. Must not be empty.
        seed (Optional[int]): Seed for reproducible results. If not provided, a random seed is used.
        voice (Optional[str]): Voice to use for audio generation. 
                               Options: "alloy", "echo", "fable", "onyx", "nova", "shimmer", 
                               "coral", "verse", "ballad", "ash", "sage", "amuch", "dan".
                               Defaults to "alloy".
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error (str): Error message if audio generation failed; empty string if successful.
            - status (str): Status of the request, typically "success" or "error".
    
    Raises:
        ValueError: If prompt is empty or voice is not in the allowed list.
    """
    # Input validation
    if not prompt or not prompt.strip():
        return {
            "error": "Prompt cannot be empty",
            "status": "error"
        }
    
    allowed_voices = [
        "alloy", "echo", "fable", "onyx", "nova", "shimmer",
        "coral", "verse", "ballad", "ash", "sage", "amuch", "dan"
    ]
    
    if voice is not None and voice not in allowed_voices:
        return {
            "error": f"Voice '{voice}' is not supported. Use one of: {', '.join(allowed_voices)}",
            "status": "error"
        }

    # Call simulated external API
    api_data = call_external_api("mcpollinations-multimodal-server-respondAudio")

    # Construct result based on API response
    result = {
        "error": api_data["error"],
        "status": api_data["status"]
    }

    # If there was an error in API simulation, return early
    if api_data["error"]:
        result["status"] = "error"
    
    return result