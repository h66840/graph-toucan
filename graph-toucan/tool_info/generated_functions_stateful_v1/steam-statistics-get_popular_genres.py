from typing import Dict, List, Any

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
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
        api_data = call_external_api("steam-statistics-get_popular_genres", **locals())
        
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

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
