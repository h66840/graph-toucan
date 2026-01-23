from typing import Dict, List, Any, Optional

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
    Simulates fetching data from external API for player's most played heroes.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hero_0_name (str): Name of the first most played hero
        - hero_0_id (int): ID of the first most played hero
        - hero_0_games (int): Number of games played with the first hero
        - hero_0_wins (int): Number of wins with the first hero
        - hero_0_win_rate (float): Win rate percentage for the first hero
        - hero_0_last_played (int): Timestamp of last play for the first hero
        - hero_1_name (str): Name of the second most played hero
        - hero_1_id (int): ID of the second most played hero
        - hero_1_games (int): Number of games played with the second hero
        - hero_1_wins (int): Number of wins with the second hero
        - hero_1_win_rate (float): Win rate percentage for the second hero
        - hero_1_last_played (int): Timestamp of last play for the second hero
    """
    return {
        "hero_0_name": "Anti-Mage",
        "hero_0_id": 1,
        "hero_0_games": 150,
        "hero_0_wins": 89,
        "hero_0_win_rate": 59.3,
        "hero_0_last_played": 1678886400,
        "hero_1_name": "Phantom Lancer",
        "hero_1_id": 17,
        "hero_1_games": 132,
        "hero_1_wins": 76,
        "hero_1_win_rate": 57.6,
        "hero_1_last_played": 1678790123
    }

def opendota_api_server_get_player_heroes(account_id: int, limit: Optional[int] = 5) -> Dict[str, Any]:
    """
    Get a player's most played heroes.
    
    Args:
        account_id (int): Steam32 account ID of the player (required)
        limit (int, optional): Number of heroes to retrieve (default: 5)
    
    Returns:
        Dict containing a list of hero statistics, each with 'name', 'id', 'games', 'wins', 'win_rate', and 'last_played' fields
    
    Raises:
        ValueError: If account_id is not a positive integer
    """
    # Input validation
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id must be a positive integer")
    
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("limit must be a positive integer")
    
    # Default limit is 5
    effective_limit = limit if limit is not None else 5
    
    # Call external API to get data (simulated)
    api_data = call_external_api("opendota-api-server-get_player_heroes", **locals())
    
    # Construct the heroes list from flattened API response
    heroes = []
    
    # Process up to the limit or available heroes (only 2 simulated)
    for i in range(min(effective_limit, 2)):
        hero_key = f"hero_{i}"
        try:
            hero = {
                "name": api_data[f"{hero_key}_name"],
                "id": api_data[f"{hero_key}_id"],
                "games": api_data[f"{hero_key}_games"],
                "wins": api_data[f"{hero_key}_wins"],
                "win_rate": api_data[f"{hero_key}_win_rate"],
                "last_played": api_data[f"{hero_key}_last_played"]
            }
            heroes.append(hero)
        except KeyError:
            # If any key is missing, skip this hero
            continue
    
    return {"heroes": heroes}

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
