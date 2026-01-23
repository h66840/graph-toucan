from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for team information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - team_id (int): Unique identifier for the team
        - name (str): Official name of the team
        - tag (str): Short abbreviation or acronym used by the team
        - logo_url (str): URL to the team's logo image
        - country_code (str): ISO country code associated with the team
        - admin_id (int): Player ID of the team administrator or captain
        - rating (float): Elo-based rating indicating team strength
        - wins (int): Total number of wins in ranked play
        - losses (int): Total number of losses in ranked play
        - last_match_time (int): Timestamp of the most recent match played by the team
        - league_count (int): Number of leagues the team is currently participating in
        - is_locked (bool): Indicates whether the team roster is locked from changes
        - created_at (int): Unix timestamp when the team was created
        - updated_at (int): Unix timestamp of the last update to team data
        - player_0_player_id (int): Player ID of the first current player
        - player_0_name (str): Name of the first current player
        - player_0_join_date (int): Join date timestamp of the first player
        - player_1_player_id (int): Player ID of the second current player
        - player_1_name (str): Name of the second current player
        - player_1_join_date (int): Join date timestamp of the second player
        - history_0_opponent (str): Opponent in the first historical match
        - history_0_result (str): Result of the first historical match (e.g., 'win', 'loss')
        - history_0_date (int): Date timestamp of the first historical match
        - history_1_opponent (str): Opponent in the second historical match
        - history_1_result (str): Result of the second historical match (e.g., 'win', 'loss')
        - history_1_date (int): Date timestamp of the second historical match
    """
    return {
        "team_id": 12345,
        "name": "Evil Geniuses",
        "tag": "EG",
        "logo_url": "https://example.com/logos/eg.png",
        "country_code": "US",
        "admin_id": 98765,
        "rating": 2450.75,
        "wins": 142,
        "losses": 89,
        "last_match_time": 1700000000,
        "league_count": 3,
        "is_locked": True,
        "created_at": 1400000000,
        "updated_at": 1700000000,
        "player_0_player_id": 50123,
        "player_0_name": "SumaiL",
        "player_0_join_date": 1500000000,
        "player_1_player_id": 50124,
        "player_1_name": "Arteezy",
        "player_1_join_date": 1520000000,
        "history_0_opponent": "Team Liquid",
        "history_0_result": "win",
        "history_0_date": 1699000000,
        "history_1_opponent": "OG",
        "history_1_result": "loss",
        "history_1_date": 1698000000,
    }

def opendota_api_server_get_team_info(team_id: int) -> Dict[str, Any]:
    """
    Get information about a team using its team ID.
    
    Args:
        team_id (int): The unique identifier for the team.
        
    Returns:
        Dict containing detailed team information including:
        - team_id (int): Unique identifier for the team
        - name (str): Official name of the team
        - tag (str): Short abbreviation or acronym used by the team
        - logo_url (str): URL to the team's logo image
        - country_code (str): ISO country code associated with the team
        - admin_id (int): Player ID of the team administrator or captain
        - rating (float): Elo-based rating indicating team strength
        - wins (int): Total number of wins in ranked play
        - losses (int): Total number of losses in ranked play
        - last_match_time (int): Timestamp of the most recent match played by the team
        - league_count (int): Number of leagues the team is currently participating in
        - player_list (List[Dict]): List of current players with player_id, name, and join_date
        - full_history (List[Dict]): Historical matches with opponent, result, and date
        - is_locked (bool): Whether the team roster is locked from changes
        - created_at (int): Unix timestamp when the team was created
        - updated_at (int): Unix timestamp of the last update to team data
        
    Raises:
        ValueError: If team_id is not a positive integer
    """
    if not isinstance(team_id, int) or team_id <= 0:
        raise ValueError("team_id must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_team_info")
    
    # Construct player_list from indexed fields
    player_list = [
        {
            "player_id": api_data["player_0_player_id"],
            "name": api_data["player_0_name"],
            "join_date": api_data["player_0_join_date"]
        },
        {
            "player_id": api_data["player_1_player_id"],
            "name": api_data["player_1_name"],
            "join_date": api_data["player_1_join_date"]
        }
    ]
    
    # Construct full_history from indexed fields
    full_history = [
        {
            "opponent": api_data["history_0_opponent"],
            "result": api_data["history_0_result"],
            "date": api_data["history_0_date"]
        },
        {
            "opponent": api_data["history_1_opponent"],
            "result": api_data["history_1_result"],
            "date": api_data["history_1_date"]
        }
    ]
    
    # Build final result structure matching output schema
    result = {
        "team_id": api_data["team_id"],
        "name": api_data["name"],
        "tag": api_data["tag"],
        "logo_url": api_data["logo_url"],
        "country_code": api_data["country_code"],
        "admin_id": api_data["admin_id"],
        "rating": api_data["rating"],
        "wins": api_data["wins"],
        "losses": api_data["losses"],
        "last_match_time": api_data["last_match_time"],
        "league_count": api_data["league_count"],
        "player_list": player_list,
        "full_history": full_history,
        "is_locked": api_data["is_locked"],
        "created_at": api_data["created_at"],
        "updated_at": api_data["updated_at"]
    }
    
    return result