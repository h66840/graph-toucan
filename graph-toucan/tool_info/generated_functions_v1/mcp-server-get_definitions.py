def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - definition (str): The definition of the requested word or phrase
        - is_found (bool): Indicates whether a definition was successfully found
    """
    return {
        "definition": "a statement of the exact meaning of a word, especially in a dictionary",
        "is_found": True
    }


def mcp_server_get_definitions(word: str) -> dict:
    """
    Get definitions for a word.

    Args:
        word (str): The word or phrase to get the definition for. Required.

    Returns:
        dict: A dictionary containing:
            - definition (str): The definition of the requested word or phrase; may be a plain text explanation or an empty result indicator
            - is_found (bool): Indicates whether a definition was successfully found for the requested word (True) or not (False)

    Raises:
        ValueError: If 'word' is not provided or is empty.
    """
    if not word or not word.strip():
        raise ValueError("Parameter 'word' is required and cannot be empty.")

    # Call the external API simulation
    api_data = call_external_api("mcp-server-get_definitions")

    # Construct result matching output schema
    result = {
        "definition": api_data["definition"],
        "is_found": api_data["is_found"]
    }

    return result