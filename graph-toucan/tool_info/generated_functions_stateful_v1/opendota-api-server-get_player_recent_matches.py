from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

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
    Simulates fetching data from external API for player recent matches.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - match_0_match_id (int): Match ID of the first recent match
        - match_0_date (int): Unix timestamp of the first match
        - match_0_duration (int): Duration of the first match in seconds
        - match_0_hero_id (int): Hero ID used in the first match
        - match_0_kills (int): Number of kills in the first match
        - match_0_deaths (int): Number of deaths in the first match
        - match_0_assists (int): Number of assists in the first match
        - match_0_gpm (int): Gold per minute in the first match
        - match_0_xpm (int): Experience per minute in the first match
        - match_0_result (str): Result of the first match ('win' or 'lose')
        - match_1_match_id (int): Match ID of the second recent match
        - match_1_date (int): Unix timestamp of the second match
        - match_1_duration (int): Duration of the second match in seconds
        - match_1_hero_id (int): Hero ID used in the second match
        - match_1_kills (int): Number of kills in the second match
        - match_1_deaths (int): Number of deaths in the second match
        - match_1_assists (int): Number of assists in the second match
        - match_1_gpm (int): Gold per minute in the second match
        - match_1_xpm (int): Experience per minute in the second match
        - match_1_result (str): Result of the second match ('win' or 'lose')
        - error_message (str): Error message if any, otherwise empty string
    """
    now = datetime.now()
    return {
        "match_0_match_id": 7564321987,
        "match_0_date": int((now - timedelta(minutes=30)).timestamp()),
        "match_0_duration": 2340,
        "match_0_hero_id": 11,
        "match_0_kills": 8,
        "match_0_deaths": 5,
        "match_0_assists": 12,
        "match_0_gpm": 420,
        "match_0_xpm": 480,
        "match_0_result": "win",
        "match_1_match_id": 7564321986,
        "match_1_date": int((now - timedelta(hours=2)).timestamp()),
        "match_1_duration": 2760,
        "match_1_hero_id": 25,
        "match_1_kills": 6,
        "match_1_deaths": 9,
        "match_1_assists": 7,
        "match_1_gpm": 380,
        "match_1_xpm": 410,
        "match_1_result": "lose",
        "error_message": ""
    }


def opendota_api_server_get_player_recent_matches(account_id: int, limit: Optional[int] = 5) -> Dict[str, Any]:
    """
    Get recent matches played by a player.

    Args:
        account_id (int): Steam32 account ID of the player
        limit (int, optional): Number of matches to retrieve (default: 5)

    Returns:
        Dict containing:
        - matches (List[Dict]): list of recent match details, each containing 'match_id', 'date', 'duration',
          'hero_id', 'kills', 'deaths', 'assists', 'gpm', 'xpm', and 'result' fields
        - error_message (str): message indicating no matches found or other issues when no data is available
    """
    # Input validation
    if not isinstance(account_id, int) or account_id <= 0:
        return {
            "matches": [],
            "error_message": "Invalid account_id: must be a positive integer"
        }

    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        return {
            "matches": [],
            "error_message": "Invalid limit: must be a positive integer"
        }

    # Default limit is 5
    actual_limit = limit if limit is not None else 5

    # Call external API to get data (simulated)
    api_data = call_external_api("opendota-api-server-get_player_recent_matches", **locals())

    # Check for error from API
    if api_data.get("error_message"):
        return {
            "matches": [],
            "error_message": api_data["error_message"]
        }

    # Construct matches list from flattened API data
    matches = []
    for i in range(min(actual_limit, 2)):  # We only have 2 simulated matches
        match_key = f"match_{i}"
        if f"{match_key}_match_id" in api_data:
            match = {
                "match_id": api_data[f"{match_key}_match_id"],
                "date": api_data[f"{match_key}_date"],
                "duration": api_data[f"{match_key}_duration"],
                "hero_id": api_data[f"{match_key}_hero_id"],
                "kills": api_data[f"{match_key}_kills"],
                "deaths": api_data[f"{match_key}_deaths"],
                "assists": api_data[f"{match_key}_assists"],
                "gpm": api_data[f"{match_key}_gpm"],
                "xpm": api_data[f"{match_key}_xpm"],
                "result": api_data[f"{match_key}_result"]
            }
            matches.append(match)

    # If no matches were found
    if not matches:
        return {
            "matches": [],
            "error_message": "No recent matches found for this player"
        }

    return {
        "matches": matches,
        "error_message": ""
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
