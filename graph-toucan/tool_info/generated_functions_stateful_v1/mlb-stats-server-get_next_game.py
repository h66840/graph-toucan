from typing import Dict, Any

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
    Simulates fetching data from external API for MLB stats server.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - game_id (int): unique identifier for the upcoming game
        - team_id (int): ID of the team whose next game is being referenced
        - date (str): date of the next game in YYYY-MM-DD format
        - opponent_id (int): ID of the opposing team
        - opponent_name (str): Name of the opposing team
        - opponent_abbreviation (str): Abbreviation of the opposing team
        - status (str): current status of the game, such as "Scheduled" or "Pre-Game"
        - is_home (bool): indicates whether the team is playing at home (True) or away (False)
    """
    return {
        "game_id": 123456,
        "team_id": 123,
        "date": "2023-10-05",
        "opponent_id": 456,
        "opponent_name": "New York Yankees",
        "opponent_abbreviation": "NYY",
        "status": "Scheduled",
        "is_home": True
    }

def mlb_stats_server_get_next_game(team_id: int) -> Dict[str, Any]:
    """
    Get the game ID for a team's next scheduled game.

    Args:
        team_id (int): ID of the team whose next game is being referenced.

    Returns:
        Dict containing:
        - game_id (int): unique identifier for the upcoming game
        - team_id (int): ID of the team whose next game is being referenced
        - date (str): date of the next game in YYYY-MM-DD format
        - opponent (Dict): contains 'id' (int), 'name' (str), and 'abbreviation' (str) of the opposing team
        - status (str): current status of the game, such as "Scheduled" or "Pre-Game"
        - is_home (bool): indicates whether the team is playing at home (True) or away (False)
    """
    if not isinstance(team_id, int) or team_id <= 0:
        raise ValueError("team_id must be a positive integer")

    api_data = call_external_api("mlb-stats-server-get_next_game", **locals())

    opponent = {
        "id": api_data["opponent_id"],
        "name": api_data["opponent_name"],
        "abbreviation": api_data["opponent_abbreviation"]
    }

    result = {
        "game_id": api_data["game_id"],
        "team_id": api_data["team_id"],
        "date": api_data["date"],
        "opponent": opponent,
        "status": api_data["status"],
        "is_home": api_data["is_home"]
    }

    return result

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
