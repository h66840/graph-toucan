from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - word (str): The word or phrase that was searched for
        - definitions_0_part_of_speech (str): Part of speech for the first definition
        - definitions_0_definition_text (str): Definition text for the first definition
        - definitions_1_part_of_speech (str): Part of speech for the second definition
        - definitions_1_definition_text (str): Definition text for the second definition
    """
    return {
        "word": "example",
        "definitions_0_part_of_speech": "noun",
        "definitions_0_definition_text": "a thing serving as a pattern to be imitated or not to be imitated.",
        "definitions_1_part_of_speech": "verb",
        "definitions_1_definition_text": "demonstrate by instance."
    }

def books_server_search_word(query: str) -> Dict[str, Any]:
    """
    Search for a word and provide basic information.
    
    Args:
        query (str): The word or phrase to search for
    
    Returns:
        Dict containing:
            - word (str): the word or phrase that was searched for
            - definitions (List[Dict]): list of definition entries, each containing 'part_of_speech' (str) and 'definition_text' (str) fields
    
    Raises:
        ValueError: If query is empty or not a string
    """
    if not isinstance(query, str):
        raise ValueError("Query must be a string")
    if not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Call external API to get data
    api_data = call_external_api("books-server-search_word")
    
    # Construct definitions list from flattened API response
    definitions = [
        {
            "part_of_speech": api_data["definitions_0_part_of_speech"],
            "definition_text": api_data["definitions_0_definition_text"]
        },
        {
            "part_of_speech": api_data["definitions_1_part_of_speech"],
            "definition_text": api_data["definitions_1_definition_text"]
        }
    ]
    
    # Return structured result matching output schema
    return {
        "word": query.strip(),
        "definitions": definitions
    }