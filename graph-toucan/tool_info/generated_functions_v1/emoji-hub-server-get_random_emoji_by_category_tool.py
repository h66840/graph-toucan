from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for emoji retrieval by category.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): Name of the emoji, may include aliases
        - category (str): Category to which the emoji belongs
        - group (str): Subgroup within the category
        - htmlCode_0 (str): First HTML entity code for the emoji
        - htmlCode_1 (str): Second HTML entity code for the emoji (if applicable)
        - unicode_0 (str): First Unicode code point for the emoji
        - unicode_1 (str): Second Unicode code point for the emoji (if applicable)
    """
    return {
        "name": "panda face ≊ panda",
        "category": "animals and nature",
        "group": "animal mammal",
        "htmlCode_0": "&#128062;",
        "htmlCode_1": "&#65279;",  # Zero-width space as placeholder if not used
        "unicode_0": "U+1F43C",
        "unicode_1": "U+FE0F"
    }

def emoji_hub_server_get_random_emoji_by_category_tool(category: str) -> Dict[str, Any]:
    """
    Get a random emoji from a specific category.
    
    Available categories:
    - smileys-and-people
    - animals-and-nature
    - food-and-drink
    - travel-and-places
    - activities
    - objects
    - symbols
    - flags
    
    Parameters:
        category (str): The category from which to retrieve a random emoji. Must be one of the valid categories.
    
    Returns:
        Dict[str, Any]: A dictionary containing the emoji details with the following keys:
            - name (str): Name of the emoji, may include aliases separated by " ≊ "
            - category (str): Category to which the emoji belongs
            - group (str): Subgroup within the category
            - htmlCode (List[str]): List of HTML entity codes for the emoji
            - unicode (List[str]): List of Unicode code points for the emoji
    
    Raises:
        ValueError: If the provided category is not one of the allowed categories.
    """
    valid_categories = [
        "smileys-and-people",
        "animals-and-nature",
        "food-and-drink",
        "travel-and-places",
        "activities",
        "objects",
        "symbols",
        "flags"
    ]
    
    if not isinstance(category, str):
        raise TypeError("Category must be a string.")
        
    if category not in valid_categories:
        raise ValueError(f"Invalid category: '{category}'. Must be one of {valid_categories}.")
    
    # Fetch data from simulated external API
    api_data = call_external_api("emoji-hub-server-get_random_emoji_by_category_tool")
    
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