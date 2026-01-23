from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB player lookup.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - player_0_name (str): First player's full name
        - player_0_position (str): First player's position
        - player_0_team (str): First player's current team
        - player_0_mlbam_id (int): First player's MLBAM ID
        - player_0_retro_id (str): First player's Retrosheet ID
        - player_0_bbref_id (str): First player's Baseball Reference ID
        - player_0_fangraphs_id (int): First player's FanGraphs ID
        - player_0_birth_date (str): First player's birth date in YYYY-MM-DD
        - player_0_debut_date (str): First player's debut date in YYYY-MM-DD
        - player_1_name (str): Second player's full name
        - player_1_position (str): Second player's position
        - player_1_team (str): Second player's current team
        - player_1_mlbam_id (int): Second player's MLBAM ID
        - player_1_retro_id (str): Second player's Retrosheet ID
        - player_1_bbref_id (str): Second player's Baseball Reference ID
        - player_1_fangraphs_id (int): Second player's FanGraphs ID
        - player_1_birth_date (str): Second player's birth date in YYYY-MM-DD
        - player_1_debut_date (str): Second player's debut date in YYYY-MM-DD
        - total_count (int): Total number of players found
        - not_found_0 (int): First player ID not found (if any)
        - not_found_1 (int): Second player ID not found (if any)
        - key_type_used (str): The key type used for lookup
        - timestamp (str): ISO format timestamp of the request
        - source (str): Data source name
    """
    return {
        "player_0_name": "Mike Trout",
        "player_0_position": "CF",
        "player_0_team": "Los Angeles Angels",
        "player_0_mlbam_id": 545361,
        "player_0_retro_id": "troum001",
        "player_0_bbref_id": "troutmi01",
        "player_0_fangraphs_id": 1001,
        "player_0_birth_date": "1991-07-08",
        "player_0_debut_date": "2011-07-08",
        "player_1_name": "Aaron Judge",
        "player_1_position": "RF",
        "player_1_team": "New York Yankees",
        "player_1_mlbam_id": 592158,
        "player_1_retro_id": "judaa001",
        "player_1_bbref_id": "judgeaa01",
        "player_1_fangraphs_id": 1002,
        "player_1_birth_date": "1992-04-26",
        "player_1_debut_date": "2016-08-13",
        "total_count": 2,
        "not_found_0": 999999,
        "not_found_1": 888888,
        "key_type_used": "mlbam",
        "timestamp": datetime.datetime.now().isoformat(),
        "source": "MLB Stats API"
    }


def mlb_stats_server_reverse_lookup_player(player_ids: List[int], key_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve a table of player information given a list of player ids.

    :param player_ids: List of player IDs to look up
    :type player_ids: list of int
    :param key_type: Type of ID being used for lookup ('mlbam', 'retro', 'bbref', 'fangraphs')
    :type key_type: str, optional

    :return: Dictionary containing:
        - players (List[Dict]): List of player records with detailed information
        - total_count (int): Number of players successfully found
        - not_found (List[int]): List of IDs that were not found
        - metadata (Dict): Context about the lookup operation
    :rtype: Dict[str, Any]

    :raises ValueError: If player_ids is empty
    """
    if not player_ids:
        raise ValueError("player_ids list cannot be empty")

    # Validate key_type if provided
    valid_key_types = {'mlbam', 'retro', 'bbref', 'fangraphs'}
    if key_type and key_type not in valid_key_types:
        raise ValueError(f"key_type must be one of {valid_key_types}")

    # Call external API (simulated)
    api_data = call_external_api("mlb-stats-server-reverse_lookup_player")

    # Construct players list from indexed fields
    players = []
    for i in range(api_data["total_count"]):
        player_data = {
            "name": api_data[f"player_{i}_name"],
            "position": api_data[f"player_{i}_position"],
            "team": api_data[f"player_{i}_team"],
            "mlbam_id": api_data[f"player_{i}_mlbam_id"],
            "retro_id": api_data[f"player_{i}_retro_id"],
            "bbref_id": api_data[f"player_{i}_bbref_id"],
            "fangraphs_id": api_data[f"player_{i}_fangraphs_id"],
            "birth_date": api_data[f"player_{i}_birth_date"],
            "debut_date": api_data[f"player_{i}_debut_date"]
        }
        players.append(player_data)

    # Construct not_found list
    not_found = []
    for i in range(2):  # We expect up to 2 not_found entries based on API mock
        key = f"not_found_{i}"
        if key in api_data and api_data[key] is not None:
            not_found.append(api_data[key])

    # Construct metadata
    metadata = {
        "key_type_used": api_data["key_type_used"],
        "timestamp": api_data["timestamp"],
        "source": api_data["source"]
    }

    # Final result structure
    result = {
        "players": players,
        "total_count": api_data["total_count"],
        "not_found": not_found,
        "metadata": metadata
    }

    return result