from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching pitching stats data from an external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pitching_stats_0_player_id (str): Player ID for the first record
        - pitching_stats_0_player_name (str): Player name for the first record
        - pitching_stats_0_team_id (str): Team ID for the first record
        - pitching_stats_0_team_name (str): Team name for the first record
        - pitching_stats_0_ip (float): Innings pitched for the first record
        - pitching_stats_0_so (int): Strikeouts for the first record
        - pitching_stats_0_er (int): Earned runs for the first record
        - pitching_stats_0_h (int): Hits allowed for the first record
        - pitching_stats_0_bb (int): Walks issued for the first record
        - pitching_stats_0_era (float): Earned run average for the first record
        - pitching_stats_1_player_id (str): Player ID for the second record
        - pitching_stats_1_player_name (str): Player name for the second record
        - pitching_stats_1_team_id (str): Team ID for the second record
        - pitching_stats_1_team_name (str): Team name for the second record
        - pitching_stats_1_ip (float): Innings pitched for the second record
        - pitching_stats_1_so (int): Strikeouts for the second record
        - pitching_stats_1_er (int): Earned runs for the second record
        - pitching_stats_1_h (int): Hits allowed for the second record
        - pitching_stats_1_bb (int): Walks issued for the second record
        - pitching_stats_1_era (float): Earned run average for the second record
        - date_range_start (str): Start date in YYYY-MM-DD format
        - date_range_end (str): End date in YYYY-MM-DD format
        - total_players (int): Total number of unique players returned
        - metadata_timestamp (str): ISO format timestamp of data generation
        - metadata_source (str): Source of the data
        - metadata_disclaimer (str): Disclaimer about data completeness
    """
    return {
        "pitching_stats_0_player_id": "P1001",
        "pitching_stats_0_player_name": "John Doe",
        "pitching_stats_0_team_id": "T201",
        "pitching_stats_0_team_name": "New York Yankees",
        "pitching_stats_0_ip": 12.2,
        "pitching_stats_0_so": 15,
        "pitching_stats_0_er": 3,
        "pitching_stats_0_h": 8,
        "pitching_stats_0_bb": 4,
        "pitching_stats_0_era": 2.13,
        "pitching_stats_1_player_id": "P1002",
        "pitching_stats_1_player_name": "Jane Smith",
        "pitching_stats_1_team_id": "T205",
        "pitching_stats_1_team_name": "Boston Red Sox",
        "pitching_stats_1_ip": 14.0,
        "pitching_stats_1_so": 18,
        "pitching_stats_1_er": 2,
        "pitching_stats_1_h": 6,
        "pitching_stats_1_bb": 3,
        "pitching_stats_1_era": 1.29,
        "date_range_start": "2023-08-01",
        "date_range_end": "2023-08-15",
        "total_players": 2,
        "metadata_timestamp": "2023-08-16T10:30:00Z",
        "metadata_source": "MLB Stats API v3",
        "metadata_disclaimer": "Data may be delayed by up to 1 hour. Not for betting purposes."
    }

def mlb_stats_server_get_pitching_stats_range(start_dt: str, end_dt: Optional[str] = None) -> Dict[str, Any]:
    """
    Get all pitching stats for a set time range. This can be the past week, the
    month of August, anything. Just supply the start and end date in YYYY-MM-DD
    format.
    
    Args:
        start_dt (str): Start date in YYYY-MM-DD format (required).
        end_dt (Optional[str]): End date in YYYY-MM-DD format (optional). If not provided,
                                defaults to current date.
    
    Returns:
        Dict containing:
        - pitching_stats (List[Dict]): List of pitching performance records for players
          within the specified date range. Each entry contains statistics like innings
          pitched, strikeouts, earned runs, etc., along with player and team identifiers.
        - date_range (Dict): Object containing the effective start and end dates used
          for the query. Keys include 'start' and 'end', both in YYYY-MM-DD format.
        - total_players (int): Total number of unique players returned in the response.
        - metadata (Dict): Additional contextual information such as data source,
          generation timestamp, and any disclaimers or notes about data completeness
          or limitations.
    
    Raises:
        ValueError: If start_dt is not in valid YYYY-MM-DD format or if end_dt is before start_dt.
    """
    # Input validation
    try:
        start_date = datetime.strptime(start_dt, "%Y-%m-%d")
    except ValueError:
        raise ValueError("start_dt must be in YYYY-MM-DD format")
    
    if end_dt is None:
        end_date = datetime.now()
        end_dt = end_date.strftime("%Y-%m-%d")
    else:
        try:
            end_date = datetime.strptime(end_dt, "%Y-%m-%d")
        except ValueError:
            raise ValueError("end_dt must be in YYYY-MM-DD format")
        
        if end_date < start_date:
            raise ValueError("end_dt cannot be earlier than start_dt")
    
    # Fetch data from simulated external API
    api_data = call_external_api("mlb-stats-server-get_pitching_stats_range")
    
    # Construct pitching stats list from indexed fields
    pitching_stats = [
        {
            "player_id": api_data["pitching_stats_0_player_id"],
            "player_name": api_data["pitching_stats_0_player_name"],
            "team_id": api_data["pitching_stats_0_team_id"],
            "team_name": api_data["pitching_stats_0_team_name"],
            "ip": api_data["pitching_stats_0_ip"],
            "so": api_data["pitching_stats_0_so"],
            "er": api_data["pitching_stats_0_er"],
            "h": api_data["pitching_stats_0_h"],
            "bb": api_data["pitching_stats_0_bb"],
            "era": api_data["pitching_stats_0_era"]
        },
        {
            "player_id": api_data["pitching_stats_1_player_id"],
            "player_name": api_data["pitching_stats_1_player_name"],
            "team_id": api_data["pitching_stats_1_team_id"],
            "team_name": api_data["pitching_stats_1_team_name"],
            "ip": api_data["pitching_stats_1_ip"],
            "so": api_data["pitching_stats_1_so"],
            "er": api_data["pitching_stats_1_er"],
            "h": api_data["pitching_stats_1_h"],
            "bb": api_data["pitching_stats_1_bb"],
            "era": api_data["pitching_stats_1_era"]
        }
    ]
    
    # Construct result matching output schema
    result = {
        "pitching_stats": pitching_stats,
        "date_range": {
            "start": api_data["date_range_start"],
            "end": api_data["date_range_end"]
        },
        "total_players": api_data["total_players"],
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "source": api_data["metadata_source"],
            "disclaimer": api_data["metadata_disclaimer"]
        }
    }
    
    return result