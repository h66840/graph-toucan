from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Steam statistics on popular genres.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the response, e.g., "success"
        - genre_0_genre (str): Name of the first popular genre
        - genre_0_total_players (int): Total number of players for the first genre
        - genre_0_game_count (int): Number of games in the first genre
        - genre_1_genre (str): Name of the second popular genre
        - genre_1_total_players (int): Total number of players for the second genre
        - genre_1_game_count (int): Number of games in the second genre
    """
    return {
        "status": "success",
        "genre_0_genre": "Action",
        "genre_0_total_players": 15000000,
        "genre_0_game_count": 12500,
        "genre_1_genre": "RPG",
        "genre_1_total_players": 12000000,
        "genre_1_game_count": 9800
    }

def steam_statistics_get_popular_genres() -> Dict[str, Any]:
    """
    En popüler oyun türlerini ve oyuncu sayılarını döndürür.
    
    Returns:
        Dict containing:
        - status (str): Status of the response, e.g., "success"
        - genres (List[Dict]): List of genre objects with 'genre', 'total_players', and 'game_count' fields
    """
    try:
        api_data = call_external_api("steam-statistics-get_popular_genres")
        
        genres = [
            {
                "genre": api_data["genre_0_genre"],
                "total_players": api_data["genre_0_total_players"],
                "game_count": api_data["genre_0_game_count"]
            },
            {
                "genre": api_data["genre_1_genre"],
                "total_players": api_data["genre_1_total_players"],
                "game_count": api_data["genre_1_game_count"]
            }
        ]
        
        result = {
            "status": api_data["status"],
            "genres": genres
        }
        
        return result
    except KeyError as e:
        return {
            "status": "error",
            "genres": [],
            "error": f"Missing data field: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "genres": [],
            "error": f"Unexpected error occurred: {str(e)}"
        }