from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for emoji-hub-server-get_random_emoji_tool.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - name (str): Name of the emoji (e.g., "relieved face")
        - category (str): Top-level category of the emoji (e.g., "smileys and people")
        - group (str): Subgroup within the category (e.g., "face neutral")
        - htmlCode_0 (str): First HTML entity code for the emoji (e.g., "&#128524;")
        - htmlCode_1 (str): Second HTML entity code if applicable
        - unicode_0 (str): First Unicode code point (e.g., "U+1F60C")
        - unicode_1 (str): Second Unicode code point if applicable
    """
    return {
        "name": "relieved face",
        "category": "smileys and people",
        "group": "face neutral",
        "htmlCode_0": "&#128524;",
        "htmlCode_1": "&#65279;",
        "unicode_0": "U+1F60C",
        "unicode_1": "U+FE0F"
    }

def emoji_hub_server_get_random_emoji_tool() -> Dict[str, Any]:
    """
    Get a random emoji from the Emoji Hub API.
    
    This function simulates retrieving a random emoji by calling an external API
    and parsing the response into the required structured format.
    
    Returns:
        Dict containing:
        - name (str): name of the emoji (e.g., "relieved face", "european union")
        - category (str): top-level category of the emoji (e.g., "flags", "smileys and people")
        - group (str): subgroup within the category (e.g., "face neutral", "flags")
        - htmlCode (List[str]): list of HTML entity codes representing the emoji (e.g., ["&#128524;"])
        - unicode (List[str]): list of Unicode code points for the emoji (e.g., ["U+1F60C"])
    """
    try:
        # Call the external API simulation
        api_data = call_external_api("emoji-hub-server-get_random_emoji_tool")
        
        # Construct the result with proper nested structure
        result = {
            "name": api_data["name"],
            "category": api_data["category"],
            "group": api_data["group"],
            "htmlCode": [
                api_data["htmlCode_0"],
                api_data["htmlCode_1"]
            ],
            "unicode": [
                api_data["unicode_0"],
                api_data["unicode_1"]
            ]
        }
        
        return result
        
    except KeyError as e:
        # Handle missing fields in API response
        raise KeyError(f"Missing required field in API response: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise Exception(f"Failed to retrieve random emoji: {str(e)}")