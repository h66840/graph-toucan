from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for joke retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - joke (str): The full text of the random joke returned by the service
    """
    return {
        "joke": "Why don't scientists trust atoms? Because they make up everything!"
    }

def manga_translator_get_random_joke() -> Dict[str, Any]:
    """
    Fetches a random joke using the JokeAPI service.
    
    This function simulates retrieving a random joke from an external API
    by calling a helper function that returns simple scalar values, then
    constructs the proper output structure as defined in the schema.
    
    Returns:
        Dict containing:
        - joke (str): The full text of the random joke returned by the service
    """
    try:
        # Call external API helper to get data
        api_data = call_external_api("manga-translator-get_random_joke")
        
        # Validate required field exists
        if "joke" not in api_data:
            raise KeyError("Expected 'joke' field missing from API response")
            
        # Construct result matching output schema
        result = {
            "joke": str(api_data["joke"])
        }
        
        return result
        
    except Exception as e:
        # Handle any errors during processing
        return {
            "joke": f"A technical issue prevented a joke from being retrieved: {str(e)}"
        }