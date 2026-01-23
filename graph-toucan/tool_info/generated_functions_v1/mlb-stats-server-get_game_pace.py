from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching pace-of-game data from an external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - pace_data_0_average_inning_duration (float): Average duration of an inning in minutes for first game/team
        - pace_data_0_commercial_break_time (float): Total commercial break time in minutes for first entry
        - pace_data_0_between_play_duration (float): Average time between plays in minutes for first entry
        - pace_data_0_game_length_minutes (float): Total game length in minutes for first entry
        - pace_data_1_average_inning_duration (float): Average duration of an inning in minutes for second game/team
        - pace_data_1_commercial_break_time (float): Total commercial break time in minutes for second entry
        - pace_data_1_between_play_duration (float): Average time between plays in minutes for second entry
        - pace_data_1_game_length_minutes (float): Total game length in minutes for second entry
        - season (int): The MLB season year for which data is reported
        - average_game_pace_minutes (float): Overall average game duration in minutes
        - average_innings_per_game (float): Average number of innings per game
        - total_games_tracked (int): Total number of games included in the dataset
        - metadata_source (str): Source of the data
        - metadata_last_updated (str): Timestamp when data was last updated (ISO format)
        - metadata_coverage (str): Description of data coverage (e.g., regular season only)
    """
    return {
        "pace_data_0_average_inning_duration": 19.8,
        "pace_data_0_commercial_break_time": 47.2,
        "pace_data_0_between_play_duration": 38.5,
        "pace_data_0_game_length_minutes": 189,
        "pace_data_1_average_inning_duration": 20.1,
        "pace_data_1_commercial_break_time": 48.0,
        "pace_data_1_between_play_duration": 39.1,
        "pace_data_1_game_length_minutes": 192,
        "season": 2023,
        "average_game_pace_minutes": 190.5,
        "average_innings_per_game": 9.05,
        "total_games_tracked": 2430,
        "metadata_source": "MLB Official Statistics Server",
        "metadata_last_updated": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "metadata_coverage": "Regular season games only; excludes postseason and spring training"
    }

def mlb_stats_server_get_game_pace(season: Optional[int] = None) -> Dict[str, Any]:
    """
    Returns data about pace of game for a given MLB season (back to 1999).
    
    If no season is specified, returns data for the most recent available season.
    
    Args:
        season (Optional[int]): The MLB season year to retrieve pace data for. 
                               Must be between 1999 and current year. If None, uses latest.
    
    Returns:
        Dict containing:
        - pace_data (List[Dict]): List of dictionaries with pace-of-game statistics per game/team
        - season (int): The season year to which the data applies
        - average_game_pace_minutes (float): Overall average game duration in minutes
        - average_innings_per_game (float): Average number of innings per game
        - total_games_tracked (int): Number of games included in the dataset
        - metadata (Dict): Additional context including source, last_updated, and coverage notes
    
    Raises:
        ValueError: If season is provided and is outside valid range (1999 to current year)
    """
    current_year = datetime.now().year
    
    if season is not None:
        if not isinstance(season, int):
            raise ValueError("Season must be an integer.")
        if season < 1999 or season > current_year:
            raise ValueError(f"Season must be between 1999 and {current_year}.")
    
    # Fetch simulated external data
    api_data = call_external_api("mlb-stats-server-get_game_pace")
    
    # Construct pace_data list from indexed fields
    pace_data = [
        {
            "average_inning_duration": api_data["pace_data_0_average_inning_duration"],
            "commercial_break_time": api_data["pace_data_0_commercial_break_time"],
            "between_play_duration": api_data["pace_data_0_between_play_duration"],
            "game_length_minutes": api_data["pace_data_0_game_length_minutes"]
        },
        {
            "average_inning_duration": api_data["pace_data_1_average_inning_duration"],
            "commercial_break_time": api_data["pace_data_1_commercial_break_time"],
            "between_play_duration": api_data["pace_data_1_between_play_duration"],
            "game_length_minutes": api_data["pace_data_1_game_length_minutes"]
        }
    ]
    
    # Build metadata dictionary
    metadata = {
        "source": api_data["metadata_source"],
        "last_updated": api_data["metadata_last_updated"],
        "coverage": api_data["metadata_coverage"]
    }
    
    # Final result structure matching output schema
    result = {
        "pace_data": pace_data,
        "season": api_data["season"],
        "average_game_pace_minutes": api_data["average_game_pace_minutes"],
        "average_innings_per_game": api_data["average_innings_per_game"],
        "total_games_tracked": api_data["total_games_tracked"],
        "metadata": metadata
    }
    
    return result