from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for word definitions.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - definition_0 (str): First definition of the word
        - definition_1 (str): Second definition of the word
        - found (bool): Whether at least one definition was found
    """
    # Simulated response data with only flat, scalar values
    return {
        "definition_0": "a single distinct meaning of a word or phrase",
        "definition_1": "an exact statement or description of the nature, scope, or meaning of something",
        "found": True
    }

def mobile_challenge_server_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a word.
    
    This function retrieves a list of definitions for the given word.
    
    Args:
        word (str): The word to get definitions for. Required.
        
    Returns:
        Dict containing:
        - definitions (List[str]): list of definition strings for the requested word, each representing a distinct meaning or usage
        - found (bool): whether at least one definition was found for the word
    
    Raises:
        ValueError: If word is empty or not a string
    """
    # Input validation
    if not isinstance(word, str):
        raise ValueError("Word must be a string")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace")
    
    # Normalize input
    word = word.strip()
    
    # Fetch data from simulated external API
    api_data = call_external_api("mobile-challenge-server-get_definitions")
    
    # Construct the result structure according to the output schema
    definitions = []
    
    # Collect definitions from indexed fields
    if api_data.get("found", False):
        definitions.append(api_data["definition_0"])
        definitions.append(api_data["definition_1"])
    
    # Build final result
    result = {
        "definitions": definitions,
        "found": api_data["found"]
    }
    
    return result