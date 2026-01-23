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
    Simulates fetching data from external API for OpenDota match data.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - match_id (int): unique identifier for the match
        - date (str): start time of the match in ISO 8601 format (YYYY-MM-DD HH:MM:SS)
        - duration (str): duration of the match in MM:SS format
        - game_mode (int): numeric code representing the game mode played
        - radiant_team_name (str): name of the Radiant team if available, otherwise "Radiant"
        - dire_team_name (str): name of the Dire team if available, otherwise "Dire"
        - score_radiant (int): number of kills by Radiant team
        - score_dire (int): number of kills by Dire team
        - winner (str): side that won the match: either "Radiant" or "Dire"
        - player_0_player_id (int or str): account ID or "Anonymous"
        - player_0_team (str): team affiliation: "Radiant" or "Dire"
        - player_0_hero_id (int): numeric identifier of the hero played
        - player_0_hero_name (str): display name of the hero
        - player_0_kills (int): number of kills by the player
        - player_0_deaths (int): number of deaths by the player
        - player_0_assists (int): number of assists by the player
        - player_0_gpm (int): gold per minute
        - player_0_xpm (int): experience per minute
        - player_1_player_id (int or str): account ID or "Anonymous"
        - player_1_team (str): team affiliation: "Radiant" or "Dire"
        - player_1_hero_id (int): numeric identifier of the hero played
        - player_1_hero_name (str): display name of the hero
        - player_1_kills (int): number of kills by the player
        - player_1_deaths (int): number of deaths by the player
        - player_1_assists (int): number of assists by the player
        - player_1_gpm (int): gold per minute
        - player_1_xpm (int): experience per minute
    """
    return {
        "match_id": 1234567890,
        "date": "2023-10-05 14:30:22",
        "duration": "38:45",
        "game_mode": 22,
        "radiant_team_name": "Team Spirit",
        "dire_team_name": "OG",
        "score_radiant": 34,
        "score_dire": 28,
        "winner": "Radiant",
        "player_0_player_id": 100000001,
        "player_0_team": "Radiant",
        "player_0_hero_id": 1,
        "player_0_hero_name": "Anti-Mage",
        "player_0_kills": 12,
        "player_0_deaths": 4,
        "player_0_assists": 8,
        "player_0_gpm": 520,
        "player_0_xpm": 580,
        "player_1_player_id": 100000002,
        "player_1_team": "Dire",
        "player_1_hero_id": 2,
        "player_1_hero_name": "Axe",
        "player_1_kills": 6,
        "player_1_deaths": 11,
        "player_1_assists": 14,
        "player_1_gpm": 410,
        "player_1_xpm": 490,
    }

def opendota_api_server_get_match_data(match_id: int) -> Dict[str, Any]:
    """
    Get detailed data for a specific match.
    
    Args:
        match_id (int): ID of the match to retrieve
        
    Returns:
        Dict containing detailed match information including players, scores, and stats.
        Structure includes:
        - match_id (int)
        - date (str)
        - duration (str)
        - game_mode (int)
        - radiant_team_name (str)
        - dire_team_name (str)
        - score (Dict with 'radiant' and 'dire' keys)
        - winner (str)
        - players (List of Dicts with player performance data)
        
    Raises:
        ValueError: If match_id is not a positive integer
    """
    if not isinstance(match_id, int) or match_id <= 0:
        raise ValueError("match_id must be a positive integer")
    
    # Call external API to get flat data
    api_data = call_external_api("opendota-api-server-get_match_data", **locals())
    
    # Construct the nested structure as per output schema
    result = {
        "match_id": api_data["match_id"],
        "date": api_data["date"],
        "duration": api_data["duration"],
        "game_mode": api_data["game_mode"],
        "radiant_team_name": api_data["radiant_team_name"],
        "dire_team_name": api_data["dire_team_name"],
        "score": {
            "radiant": api_data["score_radiant"],
            "dire": api_data["score_dire"]
        },
        "winner": api_data["winner"],
        "players": [
            {
                "player_id": api_data["player_0_player_id"],
                "team": api_data["player_0_team"],
                "hero_id": api_data["player_0_hero_id"],
                "hero_name": api_data["player_0_hero_name"],
                "kills": api_data["player_0_kills"],
                "deaths": api_data["player_0_deaths"],
                "assists": api_data["player_0_assists"],
                "gpm": api_data["player_0_gpm"],
                "xpm": api_data["player_0_xpm"]
            },
            {
                "player_id": api_data["player_1_player_id"],
                "team": api_data["player_1_team"],
                "hero_id": api_data["player_1_hero_id"],
                "hero_name": api_data["player_1_hero_name"],
                "kills": api_data["player_1_kills"],
                "deaths": api_data["player_1_deaths"],
                "assists": api_data["player_1_assists"],
                "gpm": api_data["player_1_gpm"],
                "xpm": api_data["player_1_xpm"]
            }
        ]
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
