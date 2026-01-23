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
        api_data = call_external_api("steam-statistics-get_top_games", **locals())
        
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
