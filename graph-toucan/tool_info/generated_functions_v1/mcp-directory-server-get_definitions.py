from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - definition_0 (str): First definition of the word
        - definition_1 (str): Second definition of the word
    """
    return {
        "definition_0": "A single distinct meaning of a word or phrase.",
        "definition_1": "The act of defining or making something clear and distinct."
    }

def mcp_directory_server_get_definitions(word: str) -> Dict[str, Any]:
    """
    Get definitions for a given word.
    
    This function retrieves multiple definitions for a specified word by querying
    an external API simulation. It returns a list of definition strings, each 
    representing a distinct meaning or usage of the word.
    
    Args:
        word (str): The word to get definitions for. Required.
        
    Returns:
        Dict[str, Any]: A dictionary containing a single key 'definitions' with a 
                       list of definition strings. Each string represents a 
                       distinct meaning or usage of the input word.
                       
    Example:
        >>> mcp_directory_server_get_definitions("definition")
        {
            'definitions': [
                'A single distinct meaning of a word or phrase.',
                'The act of defining or making something clear and distinct.'
            ]
        }
    """
    # Input validation
    if not isinstance(word, str):
        raise TypeError("Word must be a string")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("mcp-directory-server-get_definitions")
    
    # Construct the output structure matching the schema
    definitions = [
        api_data["definition_0"],
        api_data["definition_1"]
    ]
    
    return {
        "definitions": definitions
    }