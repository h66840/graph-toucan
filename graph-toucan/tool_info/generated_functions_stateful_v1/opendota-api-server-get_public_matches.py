from typing import Dict, List, Any, Optional
import datetime

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
    Simulates fetching data from external API for OpenDota public matches.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - match_0_match_id (int): Match ID of the first recent public match
        - match_0_duration (int): Duration of the first match in seconds
        - match_0_start_time (int): Unix timestamp when the first match started
        - match_0_radiant_win (bool): Whether Radiant won the first match
        - match_0_players_count (int): Number of players in the first match
        - match_0_game_mode (int): Game mode ID of the first match
        - match_1_match_id (int): Match ID of the second recent public match
        - match_1_duration (int): Duration of the second match in seconds
        - match_1_start_time (int): Unix timestamp when the second match started
        - match_1_radiant_win (bool): Whether Radiant won the second match
        - match_1_players_count (int): Number of players in the second match
        - match_1_game_mode (int): Game mode ID of the second match
        - total_count (int): Total number of recent public matches available
        - metadata_data_updated_at (str): ISO format timestamp of when data was last updated
        - metadata_retrieved_at (str): ISO format timestamp of when data was retrieved
        - metadata_filters (str): JSON string describing server-side filters applied
    """
    return {
        "match_0_match_id": 7284759321,
        "match_0_duration": 2345,
        "match_0_start_time": 1700000000,
        "match_0_radiant_win": True,
        "match_0_players_count": 10,
        "match_0_game_mode": 22,
        "match_1_match_id": 7284759320,
        "match_1_duration": 2567,
        "match_1_start_time": 1699998000,
        "match_1_radiant_win": False,
        "match_1_players_count": 10,
        "match_1_game_mode": 22,
        "total_count": 10000,
        "metadata_data_updated_at": "2023-11-15T12:30:00Z",
        "metadata_retrieved_at": datetime.datetime.utcnow().isoformat() + "Z",
        "metadata_filters": '{"lobby_type": 7, "is_ranked": false}'
    }


def opendota_api_server_get_public_matches(limit: Optional[int] = 5) -> Dict[str, Any]:
    """
    Get recent public matches from the OpenDota API server.

    Args:
        limit (Optional[int]): Number of matches to retrieve (default: 5). Maximum allowed is 100.

    Returns:
        Dict containing:
        - matches (List[Dict]): List of match objects with details like match_id, duration, start_time,
          radiant_win, players_count, and game_mode.
        - total_count (int): Total number of recent public matches available.
        - metadata (Dict): Additional contextual information including data freshness and filters applied.

    Raises:
        ValueError: If limit is not a positive integer or exceeds maximum allowed value.
    """
    if limit is None:
        limit = 5

    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer.")
    if limit <= 0:
        raise ValueError("Limit must be a positive integer.")
    if limit > 100:
        raise ValueError("Limit cannot exceed 100.")

    api_data = call_external_api("opendota-api-server-get_public_matches", **locals())

    # Construct matches list from flattened API data
    matches: List[Dict[str, Any]] = []
    for i in range(min(limit, 2)):  # Only 2 simulated matches available
        match_key_prefix = f"match_{i}"
        match = {
            "match_id": api_data[f"{match_key_prefix}_match_id"],
            "duration": api_data[f"{match_key_prefix}_duration"],
            "start_time": api_data[f"{match_key_prefix}_start_time"],
            "radiant_win": api_data[f"{match_key_prefix}_radiant_win"],
            "players_count": api_data[f"{match_key_prefix}_players_count"],
            "game_mode": api_data[f"{match_key_prefix}_game_mode"]
        }
        matches.append(match)

    # Fill remaining matches with placeholder data if limit > 2
    base_match_id = 7284759319
    for i in range(2, limit):
        match = {
            "match_id": base_match_id - (i - 2),
            "duration": 1800 + ((i * 137) % 1200),
            "start_time": 1699998000 - (i * 300),
            "radiant_win": i % 2 == 0,
            "players_count": 10,
            "game_mode": 22
        }
        matches.append(match)

    # Construct metadata
    metadata = {
        "data_updated_at": api_data["metadata_data_updated_at"],
        "retrieved_at": api_data["metadata_retrieved_at"],
        "filters": api_data["metadata_filters"]
    }

    return {
        "matches": matches,
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
