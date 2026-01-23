from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for dictionary definitions.
    
    Returns:
        Dict with simple fields only (str, bool):
        - definition (str): The definition of the given word or a message indicating no definition was found
        - is_found (bool): Whether a definition was found for the word
    """
    # Simulate realistic responses based on the tool name and input
    if tool_name == "dictionary-server-get_definitions":
        return {
            "definition": "a structured set of data stored in a computer memory or storage",
            "is_found": True
        }
    else:
        return {
            "definition": "No definition available",
            "is_found": False
        }

def dictionary_server_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a given word.
    
    This function retrieves the definition of a specified word by querying an external
    dictionary service. If the word is not found, a message is returned indicating that
    no definition was found.
    
    Args:
        word (str): The word to look up in the dictionary. Must be a non-empty string.
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - definition (str): The definition of the given word, or a message indicating no definition was found
            - is_found (bool): Whether a definition was found for the word
            
    Raises:
        ValueError: If the input word is empty or not a string.
    """
    # Input validation
    if not isinstance(word, str):
        raise ValueError("Word must be a string.")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace.")
    
    # Normalize input
    word = word.strip().lower()
    
    # Call external API to get data (simulated)
    api_data = call_external_api("dictionary-server-get_definitions")
    
    # Construct result matching output schema
    result = {
        "definition": api_data["definition"],
        "is_found": api_data["is_found"]
    }
    
    return result