from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Steam game genres.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the request, e.g., "success"
        - game_name (str): Name of the game corresponding to the given app_id
        - genre_0 (str): First genre associated with the game
        - genre_1 (str): Second genre associated with the game
    """
    return {
        "status": "success",
        "game_name": "Half-Life 2",
        "genre_0": "Action",
        "genre_1": "Adventure"
    }

def steam_statistics_get_game_genres(app_id: str) -> Dict[str, Any]:
    """
    Belirli bir oyunun türlerini döndürür.

    Args:
        app_id (str): The unique identifier for the game on Steam (required).

    Returns:
        Dict[str, Any]: A dictionary containing:
            - status (str): Status of the request (e.g., "success")
            - game_name (str): Name of the game corresponding to the given app_id
            - genres (List[str]): List of genres associated with the game (up to 2 genres)
    
    Raises:
        ValueError: If app_id is empty or not a string.
    """
    if not app_id or not isinstance(app_id, str):
        raise ValueError("app_id must be a non-empty string")

    # Fetch data from simulated external API
    api_data = call_external_api("steam-statistics-get_game_genres")

    # Construct the genres list from indexed fields
    genres = []
    if "genre_0" in api_data and api_data["genre_0"]:
        genres.append(api_data["genre_0"])
    if "genre_1" in api_data and api_data["genre_1"]:
        genres.append(api_data["genre_1"])

    # Build final result matching output schema
    result = {
        "status": api_data["status"],
        "game_name": api_data["game_name"],
        "genres": genres
    }

    return result