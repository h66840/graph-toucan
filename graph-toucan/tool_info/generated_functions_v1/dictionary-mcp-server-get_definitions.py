def dictionary_mcp_server_get_definitions(word: str) -> dict:
    """
    Get definitions for a word.
    
    Args:
        word (str): The word to get definitions for. Must be a non-empty string.
    
    Returns:
        dict: A dictionary containing a list of definition strings for the requested word.
              Each string represents a distinct meaning or usage context.
    
    Raises:
        ValueError: If the word is empty or not a string.
    """
    from typing import Any, Dict

    if not isinstance(word, str):
        raise ValueError("Word must be a string.")
    if not word.strip():
        raise ValueError("Word cannot be empty or whitespace.")

    def call_external_api(tool_name: str) -> Dict[str, Any]:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - definition_0 (str): First definition of the word
            - definition_1 (str): Second definition of the word
        """
        # Generate realistic definitions based on the input word
        base_definitions = {
            "run": [
                "Move at a speed faster than walking, never having both feet on the ground at the same time.",
                "Operate, function, or perform a task."
            ],
            "set": [
                "Put, lay, or stand something in a specified place or position.",
                "A collection of related objects or values considered as a single entity."
            ],
            "word": [
                "A single distinct meaningful element of speech or writing.",
                "An assurance or promise about future action or behavior."
            ]
        }
        
        # Default fallback definitions for any other word
        default_defs = [
            f"A term used to describe various concepts, actions, or entities.",
            f"Something commonly referenced in language and communication."
        ]
        
        # Select definitions based on the input word (case-insensitive)
        definitions = base_definitions.get(word.lower(), default_defs)
        
        return {
            "definition_0": definitions[0],
            "definition_1": definitions[1]
        }

    # Call the simulated external API
    api_data = call_external_api("dictionary-mcp-server-get_definitions")

    # Construct the result structure matching the output schema
    result = {
        "definitions": [
            api_data["definition_0"],
            api_data["definition_1"]
        ]
    }

    return result