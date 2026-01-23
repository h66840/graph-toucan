from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for word definitions.
    
    Returns:
        Dict with simple fields only (str, bool):
        - definition (str): The definition text for the queried word
        - is_found (bool): Indicates whether a valid definition was found
    """
    # Simulate different responses based on the tool name
    if tool_name == "mcp-python-server-get_definitions":
        return {
            "definition": "a unit of language, consisting of one or more spoken sounds or their written representation, that functions as a principal carrier of meaning",
            "is_found": True
        }
    else:
        return {
            "definition": "",
            "is_found": False
        }

def mcp_python_server_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a given word.
    
    This function retrieves the definition of a word by querying an external API.
    It returns both the definition text and a boolean indicating whether a definition was found.
    
    Args:
        word (str): The word to get the definition for. Must be a non-empty string.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - definition (str): The definition text for the queried word; may be empty if no definition found
            - is_found (bool): Indicates whether a valid definition was found for the word
    
    Raises:
        ValueError: If the input word is empty or not a string
    """
    # Input validation
    if not isinstance(word, str):
        raise ValueError("Word must be a string")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace")
    
    # Call external API to get definition data
    api_data = call_external_api("mcp-python-server-get_definitions")
    
    # Construct result matching output schema
    result = {
        "definition": api_data["definition"],
        "is_found": api_data["is_found"]
    }
    
    return result