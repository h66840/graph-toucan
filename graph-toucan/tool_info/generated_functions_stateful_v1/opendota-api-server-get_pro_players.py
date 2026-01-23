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
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - player_0_account_id (int): Account ID of the first professional player
        - player_0_name (str): Name of the first professional player
        - player_0_team (str): Current team of the first professional player
        - player_0_total_winnings (int): Total career winnings of the first player in USD
        - player_0_is_active (bool): Whether the first player is currently active
        - player_1_account_id (int): Account ID of the second professional player
        - player_1_name (str): Name of the second professional player
        - player_1_team (str): Current team of the second professional player
        - player_1_total_winnings (int): Total career winnings of the second player in USD
        - player_1_is_active (bool): Whether the second player is currently active
        - total_count (int): Total number of professional players available
        - metadata_query_time (float): Time taken to process the query in seconds
        - metadata_source (str): Source of the data
        - metadata_limit_applied (int): Limit applied to the number of results returned
    """
    return {
        "player_0_account_id": 123456789,
        "player_0_name": "N0tail",
        "player_0_team": "Team Secret",
        "player_0_total_winnings": 6969696,
        "player_0_is_active": True,
        "player_1_account_id": 987654321,
        "player_1_name": "Ceb",
        "player_1_team": "Team Liquid",
        "player_1_total_winnings": 5858585,
        "player_1_is_active": True,
        "total_count": 150,
        "metadata_query_time": 0.12,
        "metadata_source": "OpenDota API Server",
        "metadata_limit_applied": 10
    }

def opendota_api_server_get_pro_players(limit: Optional[int] = 10) -> Dict[str, Any]:
    """
    Get list of professional players from OpenDota API server.
    
    Args:
        limit (Optional[int]): Number of players to retrieve. Defaults to 10.
    
    Returns:
        Dict containing:
        - players (List[Dict]): List of professional player objects with account ID, name, team, and career info
        - total_count (int): Total number of professional players available
        - metadata (Dict): Additional context including query time, source, and applied filters
    """
    # Input validation
    if limit is None:
        limit = 10
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("Limit must be a positive integer.")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_pro_players", **locals())
    
    # Construct players list from flattened API data
    players: List[Dict[str, Any]] = []
    
    # Extract up to 'limit' players (we only have 2 in simulation)
    for i in range(min(limit, 2)):  # Only 2 simulated players available
        player_key_prefix = f"player_{i}"
        player = {
            "account_id": api_data[f"{player_key_prefix}_account_id"],
            "name": api_data[f"{player_key_prefix}_name"],
            "team": api_data[f"{player_key_prefix}_team"],
            "career_info": {
                "total_winnings": api_data[f"{player_key_prefix}_total_winnings"],
                "is_active": api_data[f"{player_key_prefix}_is_active"]
            }
        }
        players.append(player)
    
    # Construct metadata
    metadata = {
        "query_time": api_data["metadata_query_time"],
        "source": api_data["metadata_source"],
        "filters_applied": {
            "limit": api_data["metadata_limit_applied"]
        }
    }
    
    # Return final structured response
    return {
        "players": players,
        "total_count": api_data["total_count"],
        "metadata": metadata
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
