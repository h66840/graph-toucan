from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for film information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - film_0_title (str): Title of the first matching film
        - film_0_year (int): Release year of the first film
        - film_1_title (str): Title of the second matching film
        - film_1_year (int): Release year of the second film
        - films_message (str): Message about films matching the query
    """
    return {
        "film_0_title": "Inception",
        "film_0_year": 2010,
        "film_1_title": "Interstellar",
        "film_1_year": 2014,
        "films_message": "Found 2 films matching your query."
    }

def film_information_server_get_films(name: str) -> Dict[str, Any]:
    """
    Retrieves information about films matching the given name query.
    
    Args:
        name (str): The name or partial name of the film to search for.
        
    Returns:
        Dict[str, Any]: A dictionary containing a message or result about films matching the query.
                        The 'films' key contains a string message describing the results.
                        
    Raises:
        ValueError: If the name parameter is empty or not provided.
    """
    if not name or not name.strip():
        raise ValueError("The 'name' parameter is required and cannot be empty.")
    
    # Call the external API to get film data
    api_data = call_external_api("film-information-server-get_films")
    
    # Construct the result based on the retrieved data
    result = {
        "films": api_data["films_message"]
    }
    
    return result