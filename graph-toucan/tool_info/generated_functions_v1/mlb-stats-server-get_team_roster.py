from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - roster_0_player_id (int): First player's ID
        - roster_0_full_name (str): First player's full name
        - roster_0_position (str): First player's position
        - roster_0_jersey_number (int): First player's jersey number
        - roster_0_status (str): First player's status
        - roster_0_birth_date (str): First player's birth date in ISO format
        - roster_1_player_id (int): Second player's ID
        - roster_1_full_name (str): Second player's full name
        - roster_1_position (str): Second player's position
        - roster_1_jersey_number (int): Second player's jersey number
        - roster_1_status (str): Second player's status
        - roster_1_birth_date (str): Second player's birth date in ISO format
        - team_team_id (int): Team's ID
        - team_team_name (str): Team's full name
        - team_abbreviation (str): Team's abbreviation
        - team_league (str): Team's league (e.g., 'AL', 'NL')
        - season (int): Season year
        - roster_type (str): Type of roster (e.g., 'active', '40-man')
        - as_of_date (str): Roster effective date in ISO format
        - total_players (int): Total number of players on the roster
        - metadata_request_time (str): Timestamp of request in ISO format
        - metadata_source_system (str): Source system identifier
        - metadata_disclaimer (str): Disclaimer or note from API
    """
    return {
        "roster_0_player_id": 1001,
        "roster_0_full_name": "John Doe",
        "roster_0_position": "Pitcher",
        "roster_0_jersey_number": 23,
        "roster_0_status": "active",
        "roster_0_birth_date": "1995-04-15",
        "roster_1_player_id": 1002,
        "roster_1_full_name": "Jane Smith",
        "roster_1_position": "Catcher",
        "roster_1_jersey_number": 12,
        "roster_1_status": "active",
        "roster_1_birth_date": "1993-07-22",
        "team_team_id": 101,
        "team_team_name": "New York Yankees",
        "team_abbreviation": "NYY",
        "team_league": "AL",
        "season": 2023,
        "roster_type": "active",
        "as_of_date": "2023-06-15",
        "total_players": 26,
        "metadata_request_time": datetime.now().isoformat(),
        "metadata_source_system": "MLB Stats API v3",
        "metadata_disclaimer": "Data is for informational purposes and may not reflect real-time transactions."
    }

def mlb_stats_server_get_team_roster(
    date: Optional[str] = None,
    roster_type: Optional[str] = None,
    season: Optional[int] = None,
    team_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get the roster for a given MLB team.
    
    Args:
        date (Optional[str]): The date for which to retrieve the roster (ISO format: YYYY-MM-DD).
        roster_type (Optional[str]): The type of roster to retrieve (e.g., 'active', '40-man', 'injured_list').
        season (Optional[int]): The season year for which to retrieve the roster.
        team_id (Optional[int]): The unique identifier for the MLB team (required).
    
    Returns:
        Dict containing:
        - roster (List[Dict]): List of player objects with keys like 'player_id', 'full_name', 
          'position', 'jersey_number', 'status', 'birth_date'.
        - team (Dict): Team information including 'team_id', 'team_name', 'abbreviation', 'league'.
        - season (int): The season year.
        - roster_type (str): The type of roster.
        - as_of_date (str): The effective date of the roster in ISO format.
        - total_players (int): Total number of players on the roster.
        - metadata (Dict): Additional context including 'request_time', 'source_system', 'disclaimer'.
    
    Raises:
        ValueError: If team_id is not provided.
    """
    if team_id is None:
        raise ValueError("team_id is required")

    # Call external API to get flattened data
    api_data = call_external_api("mlb-stats-server-get_team_roster")

    # Construct roster list from indexed fields
    roster = [
        {
            "player_id": api_data["roster_0_player_id"],
            "full_name": api_data["roster_0_full_name"],
            "position": api_data["roster_0_position"],
            "jersey_number": api_data["roster_0_jersey_number"],
            "status": api_data["roster_0_status"],
            "birth_date": api_data["roster_0_birth_date"]
        },
        {
            "player_id": api_data["roster_1_player_id"],
            "full_name": api_data["roster_1_full_name"],
            "position": api_data["roster_1_position"],
            "jersey_number": api_data["roster_1_jersey_number"],
            "status": api_data["roster_1_status"],
            "birth_date": api_data["roster_1_birth_date"]
        }
    ]

    # Construct team object
    team = {
        "team_id": api_data["team_team_id"],
        "team_name": api_data["team_team_name"],
        "abbreviation": api_data["team_abbreviation"],
        "league": api_data["team_league"]
    }

    # Construct metadata
    metadata = {
        "request_time": api_data["metadata_request_time"],
        "source_system": api_data["metadata_source_system"],
        "disclaimer": api_data["metadata_disclaimer"]
    }

    # Return full response matching output schema
    return {
        "roster": roster,
        "team": team,
        "season": api_data["season"],
        "roster_type": api_data["roster_type"],
        "as_of_date": api_data["as_of_date"],
        "total_players": api_data["total_players"],
        "metadata": metadata
    }