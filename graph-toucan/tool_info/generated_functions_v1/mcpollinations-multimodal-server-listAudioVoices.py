from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for listing available audio voices.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - voice_0 (str): First available voice identifier
        - voice_1 (str): Second available voice identifier
    """
    return {
        "voice_0": "en-US-JennyNeural",
        "voice_1": "en-US-GuyNeural"
    }

def mcpollinations_multimodal_server_listAudioVoices() -> Dict[str, Any]:
    """
    List all available audio voices for text-to-speech generation.

    This function queries the external API to retrieve a list of available voice identifiers
    that can be used for text-to-speech synthesis.

    Returns:
        Dict containing:
        - voices (List[str]): List of available voice identifiers for text-to-speech generation
    """
    try:
        # Call external API to get flat data
        api_data = call_external_api("mcpollinations-multimodal-server-listAudioVoices")
        
        # Construct the result structure according to output schema
        result = {
            "voices": [
                api_data["voice_0"],
                api_data["voice_1"]
            ]
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields in API response
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to list audio voices: {str(e)}") from e