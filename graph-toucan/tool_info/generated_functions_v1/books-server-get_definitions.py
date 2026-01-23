from typing import Dict,Any
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - word (str): The word for which definitions are retrieved
        - definitions_0_part_of_speech (str): Part of speech for the first definition
        - definitions_0_meaning (str): Meaning of the first definition
        - definitions_1_part_of_speech (str): Part of speech for the second definition
        - definitions_1_meaning (str): Meaning of the second definition
    """
    return {
        "word": "example",
        "definitions_0_part_of_speech": "noun",
        "definitions_0_meaning": "a thing characteristic of its kind or illustrating a general rule",
        "definitions_1_part_of_speech": "verb",
        "definitions_1_meaning": "demonstrate by example"
    }

def books_server_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a word using Dictionary API.
    
    Args:
        word (str): The word to get definitions for
    
    Returns:
        Dict containing:
            - word (str): the word for which definitions are retrieved
            - definitions (List[Dict]): list of definition entries, each with 'part_of_speech' and 'meaning' fields
    
    Raises:
        ValueError: If word is empty or not a string
    """
    if not word or not isinstance(word, str):
        raise ValueError("Word must be a non-empty string")
    
    api_data = call_external_api("books-server-get_definitions")
    
    # Construct definitions list from flattened API response
    definitions = [
        {
            "part_of_speech": api_data["definitions_0_part_of_speech"],
            "meaning": api_data["definitions_0_meaning"]
        },
        {
            "part_of_speech": api_data["definitions_1_part_of_speech"],
            "meaning": api_data["definitions_1_meaning"]
        }
    ]
    
    return {
        "word": word,
        "definitions": definitions
    }