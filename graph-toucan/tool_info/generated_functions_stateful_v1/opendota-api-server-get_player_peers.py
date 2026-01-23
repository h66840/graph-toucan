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
    Simulates fetching player peer data from external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - peer_0_account_id (int): Account ID of first peer
        - peer_0_name (str): Name of first peer
        - peer_0_last_played (int): Unix timestamp of last game played together
        - peer_0_games_played (int): Number of games played together
        - peer_0_win_count (int): Number of wins when playing together
        - peer_0_with_win_rate (float): Win rate when playing together (0.0 to 1.0)
        - peer_1_account_id (int): Account ID of second peer
        - peer_1_name (str): Name of second peer
        - peer_1_last_played (int): Unix timestamp of last game played together
        - peer_1_games_played (int): Number of games played together
        - peer_1_win_count (int): Number of wins when playing together
        - peer_1_with_win_rate (float): Win rate when playing together (0.0 to 1.0)
        - total_peers_count (int): Total number of unique players the queried player has played with
        - player_account_id (int): The account ID of the queried player
        - retrieved_count (int): Number of peer records returned (should be 2)
    """
    return {
        "peer_0_account_id": 12345678,
        "peer_0_name": "PlayerOne",
        "peer_0_last_played": 1700000000,
        "peer_0_games_played": 150,
        "peer_0_win_count": 85,
        "peer_0_with_win_rate": 0.567,
        "peer_1_account_id": 87654321,
        "peer_1_name": "PlayerTwo",
        "peer_1_last_played": 1699000000,
        "peer_1_games_played": 120,
        "peer_1_win_count": 68,
        "peer_1_with_win_rate": 0.567,
        "total_peers_count": 342,
        "player_account_id": 11111111,
        "retrieved_count": 2
    }

def opendota_api_server_get_player_peers(account_id: int, limit: Optional[int] = 5) -> Dict[str, Any]:
    """
    Get players who have played with the specified player.

    Args:
        account_id (int): Steam32 account ID of the player
        limit (int, optional): Number of peers to retrieve (default: 5)

    Returns:
        Dict containing:
        - peers (List[Dict]): List of player peers with details such as account ID, shared games count,
          last played timestamp, and win rate together.
        - total_peers_count (int): Total number of unique players the specified player has played with
        - player_account_id (int): The account ID of the queried player
        - retrieved_count (int): Number of peer records actually returned in this response

    Each peer dict contains:
        - account_id (int)
        - name (str, optional)
        - last_played (int, Unix timestamp)
        - games_played (int)
        - win_count (int)
        - with_win_rate (float): Win rate when playing together
    """
    # Input validation
    if not isinstance(account_id, int) or account_id <= 0:
        raise ValueError("account_id must be a positive integer")
    
    if limit is not None:
        if not isinstance(limit, int) or limit < 0:
            raise ValueError("limit must be a non-negative integer")
        # Cap limit at a reasonable maximum if needed
        limit = min(limit, 100)
    else:
        limit = 5

    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_player_peers", **locals())
    
    # Construct the peers list from flattened API response
    peers = []
    max_peers_in_response = 2  # Based on how many indexed fields are in call_external_api
    
    # Determine how many peers to include based on limit and available data
    actual_limit = min(limit, max_peers_in_response)
    
    for i in range(actual_limit):
        peer_key = f"peer_{i}"
        if f"{peer_key}_account_id" in api_data:
            peer = {
                "account_id": api_data[f"{peer_key}_account_id"],
                "name": api_data.get(f"{peer_key}_name"),
                "last_played": api_data[f"{peer_key}_last_played"],
                "games_played": api_data[f"{peer_key}_games_played"],
                "win_count": api_data[f"{peer_key}_win_count"],
                "with_win_rate": api_data[f"{peer_key}_with_win_rate"]
            }
            peers.append(peer)
    
    # Construct final result matching output schema
    result = {
        "peers": peers,
        "total_peers_count": api_data["total_peers_count"],
        "player_account_id": api_data["player_account_id"],
        "retrieved_count": len(peers)
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
