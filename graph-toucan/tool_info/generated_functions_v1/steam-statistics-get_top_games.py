from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Steam's top games.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the request, e.g., "success"
        - game_0_name (str): Name of the first top game
        - game_0_current_players (int): Current number of players for the first game
        - game_0_genre_0 (str): First genre of the first game
        - game_0_genre_1 (str): Second genre of the first game
        - game_1_name (str): Name of the second top game
        - game_1_current_players (int): Current number of players for the second game
        - game_1_genre_0 (str): First genre of the second game
        - game_1_genre_1 (str): Second genre of the second game
    """
    return {
        "status": "success",
        "game_0_name": "Counter-Strike 2",
        "game_0_current_players": 850000,
        "game_0_genre_0": "Action",
        "game_0_genre_1": "FPS",
        "game_1_name": "Dota 2",
        "game_1_current_players": 520000,
        "game_1_genre_0": "Strategy",
        "game_1_genre_1": "MOBA"
    }

def steam_statistics_get_top_games() -> Dict[str, Any]:
    """
    Fetches the top games on Steam along with their current player counts and genres.

    Returns:
        Dict containing:
        - status (str): Status of the request (e.g., "success")
        - games (List[Dict]): List of top games, each with:
            - game_name (str): Title of the game
            - current_players (int): Number of live players
            - genres (List[str]): List of associated genres

    Example:
        {
            "status": "success",
            "games": [
                {
                    "game_name": "Counter-Strike 2",
                    "current_players": 850000,
                    "genres": ["Action", "FPS"]
                },
                {
                    "game_name": "Dota 2",
                    "current_players": 520000,
                    "genres": ["Strategy", "MOBA"]
                }
            ]
        }
    """
    try:
        api_data = call_external_api("steam-statistics-get_top_games")
        
        games = [
            {
                "game_name": api_data["game_0_name"],
                "current_players": api_data["game_0_current_players"],
                "genres": [api_data["game_0_genre_0"], api_data["game_0_genre_1"]]
            },
            {
                "game_name": api_data["game_1_name"],
                "current_players": api_data["game_1_current_players"],
                "genres": [api_data["game_1_genre_0"], api_data["game_1_genre_1"]]
            }
        ]
        
        return {
            "status": api_data["status"],
            "games": games
        }
    except KeyError as e:
        return {
            "status": "error",
            "games": [],
            "error": f"Missing data field: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "games": [],
            "error": f"Unexpected error: {str(e)}"
        }