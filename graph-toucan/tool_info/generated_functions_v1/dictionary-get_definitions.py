from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external dictionary API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - definitions_0 (str): First definition of the word
        - definitions_1 (str): Second definition of the word
        - word_found (bool): Whether the word was found in the dictionary
    """
    # Simulate realistic dictionary responses based on the tool name and input
    # Since we can't access real input here, return plausible dummy data
    return {
        "definitions_0": "A written or spoken symbolic representation of a thing or quality",
        "definitions_1": "A unit of language, consisting of one or more spoken sounds or their written representation",
        "word_found": True
    }

def dictionary_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a word.
    
    Args:
        word (str): The word to look up definitions for
        
    Returns:
        Dict containing:
        - definitions (List[str]): list of definition strings for the requested word
        - word_found (bool): indicates whether at least one definition was found for the word
    
    Example:
        {
            "definitions": [
                "A written or spoken symbolic representation of a thing or quality",
                "A unit of language, consisting of one or more spoken sounds..."
            ],
            "word_found": True
        }
    """
    # Input validation
    if not isinstance(word, str):
        raise TypeError("Word must be a string")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace")
    
    # Normalize input
    word = word.strip()
    
    # Call external API simulation
    api_data = call_external_api("dictionary-get_definitions")
    
    # Construct the result according to the output schema
    # Extract definitions from indexed fields
    definitions = []
    if api_data.get("word_found", False):
        if "definitions_0" in api_data and api_data["definitions_0"] is not None:
            definitions.append(api_data["definitions_0"])
        if "definitions_1" in api_data and api_data["definitions_1"] is not None:
            definitions.append(api_data["definitions_1"])
    
    result = {
        "definitions": definitions,
        "word_found": api_data.get("word_found", False)
    }
    
    return result