from typing import Dict, List, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - voice_0 (str): First available audio voice identifier
        - voice_1 (str): Second available audio voice identifier
    """
    return {
        "voice_0": "en-US-Journey-D",
        "voice_1": "en-US-Journey-F"
    }


def mcpollinations_listAudioVoices() -> Dict[str, List[str]]:
    """
    List all available audio voices for text-to-speech generation.

    This function retrieves a list of available voice identifiers that can be used
    for text-to-speech synthesis in the system.

    Returns:
        Dict containing a single key 'voices' with a list of voice identifier strings.
        Example: {"voices": ["en-US-Journey-D", "en-US-Journey-F"]}
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("mcpollinations-listAudioVoices")

        # Construct the output structure matching the schema
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
        raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e