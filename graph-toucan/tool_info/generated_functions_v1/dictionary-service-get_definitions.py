from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - definition_0 (str): First definition of the queried word
        - definition_1 (str): Second definition of the queried word
    """
    return {
        "definition_0": "A single distinct meaning of a word or phrase.",
        "definition_1": "The act of defining or making something clear and distinct."
    }

def dictionary_service_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a word.
    
    This function retrieves a list of definitions for the given word by querying
    an external dictionary service via a simulated API call.
    
    Args:
        word (str): The word to get definitions for. Must be a non-empty string.
    
    Returns:
        Dict[str, Any]: A dictionary containing a single key 'definitions' mapped
        to a list of definition strings. If the word is invalid or no definitions
        are found, returns an empty list.
    
    Raises:
        ValueError: If the input word is empty or not a string.
    """
    if not isinstance(word, str):
        raise ValueError("Word must be a string.")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace.")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("dictionary-service-get_definitions")
    
    # Construct the output structure from flattened API response
    definitions: List[str] = [
        api_data["definition_0"],
        api_data["definition_1"]
    ]
    
    return {
        "definitions": definitions
    }