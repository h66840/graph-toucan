from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for emoji retrieval by group.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): The name of the emoji, e.g., "red apple"
        - category (str): The broad category, e.g., "food and drink"
        - group (str): The specific group, e.g., "food fruit"
        - htmlCode_0 (str): First HTML entity code, e.g., "&#127822;"
        - htmlCode_1 (str): Second HTML entity code if applicable, otherwise empty string
        - unicode_0 (str): First Unicode code point, e.g., "U+1F34E"
        - unicode_1 (str): Second Unicode code point if applicable, otherwise empty string
    """
    # Simulated response data based on tool name
    if tool_name == "emoji-hub-server-get_random_emoji_by_group_tool":
        return {
            "name": "face with tears of joy",
            "category": "smileys and emotion",
            "group": "face-positive",
            "htmlCode_0": "&#128514;",
            "htmlCode_1": "",
            "unicode_0": "U+1F602",
            "unicode_1": ""
        }
    else:
        return {}

def emoji_hub_server_get_random_emoji_by_group_tool(group: str) -> Dict[str, Any]:
    """
    Get a random emoji from a specific group.
    
    Args:
        group (str): The emoji group to retrieve from (e.g., 'face-positive', 'animal-bird', 'food-fruit').
        
    Returns:
        Dict containing:
            - name (str): The name of the emoji
            - category (str): The broad category of the emoji
            - group (str): The specific group within the category
            - htmlCode (List[str]): List of HTML entity codes representing the emoji
            - unicode (List[str]): List of Unicode code points for the emoji
            
    Raises:
        ValueError: If group is empty or not a string
    """
    # Input validation
    if not group or not isinstance(group, str):
        raise ValueError("Group must be a non-empty string")
    
    # Call external API to get emoji data
    api_data = call_external_api("emoji-hub-server-get_random_emoji_by_group_tool")
    
    # Construct htmlCode list from indexed fields
    html_codes = []
    if api_data.get("htmlCode_0"):
        html_codes.append(api_data["htmlCode_0"])
    if api_data.get("htmlCode_1"):
        html_codes.append(api_data["htmlCode_1"])
    
    # Construct unicode list from indexed fields
    unicode_codes = []
    if api_data.get("unicode_0"):
        unicode_codes.append(api_data["unicode_0"])
    if api_data.get("unicode_1"):
        unicode_codes.append(api_data["unicode_1"])
    
    # Build final result structure matching output schema
    result = {
        "name": api_data["name"],
        "category": api_data["category"],
        "group": api_data["group"],
        "htmlCode": html_codes,
        "unicode": unicode_codes
    }
    
    return result