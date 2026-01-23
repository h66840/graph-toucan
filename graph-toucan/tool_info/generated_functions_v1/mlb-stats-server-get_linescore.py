from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching linescore data from external MLB stats server API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - game_id (int): Unique identifier for the MLB game
        - game_date (str): Date and time of the game in ISO 8601 format
        - status (str): Current status of the game
        - venue (str): Name of the stadium where the game is played
        - home_team_name (str): Name of the home team
        - home_team_abbreviation (str): Abbreviation of the home team
        - home_team_total_runs (int): Total runs scored by the home team
        - away_team_name (str): Name of the away team
        - away_team_abbreviation (str): Abbreviation of the away team
        - away_team_total_runs (int): Total runs scored by the away team
        - linescore_0_inning (int): First inning number
        - linescore_0_home_runs (int): Runs scored by home team in first inning
        - linescore_0_away_runs (int): Runs scored by away team in first inning
        - linescore_1_inning (int): Second inning number
        - linescore_1_home_runs (int): Runs scored by home team in second inning
        - linescore_1_away_runs (int): Runs scored by away team in second inning
        - has_started (bool): Whether the game has started
        - is_complete (bool): Whether the game has finished
        - current_inning (int): Current inning being played (if in progress)
        - inning_state (str): Current state within the inning (e.g., 'Top', 'Bottom')
        - weather_temperature (int): Temperature at the venue in Fahrenheit
        - weather_wind_speed (int): Wind speed in mph
        - weather_humidity (int): Humidity percentage
        - weather_conditions (str): Weather conditions description
    """
    # Generate realistic but static mock data based on game_id
    game_id = 123456  # Fixed for consistency
    start_time = (datetime.utcnow() - timedelta(hours=2)).replace(microsecond=0).isoformat() + "Z"
    
    return {
        "game_id": game_id,
        "game_date": start_time,
        "status": "InProgress",
        "venue": "Yankee Stadium",
        "home_team_name": "New York Yankees",
        "home_team_abbreviation": "NYY",
        "home_team_total_runs": 3,
        "away_team_name": "Boston Red Sox",
        "away_team_abbreviation": "BOS",
        "away_team_total_runs": 2,
        "linescore_0_inning": 1,
        "linescore_0_home_runs": 1,
        "linescore_0_away_runs": 0,
        "linescore_1_inning": 2,
        "linescore_1_home_runs": 2,
        "linescore_1_away_runs": 2,
        "has_started": True,
        "is_complete": False,
        "current_inning": 3,
        "inning_state": "Top",
        "weather_temperature": 72,
        "weather_wind_speed": 8,
        "weather_humidity": 65,
        "weather_conditions": "Partly Cloudy"
    }


def mlb_stats_server_get_linescore(game_id: int) -> Dict[str, Any]:
    """
    Get formatted linescore data for a specific MLB game.
    
    Args:
        game_id (int): Unique identifier for the MLB game
        
    Returns:
        Dict containing comprehensive linescore data for the specified game with the following structure:
        - game_id (int): Unique identifier for the MLB game
        - game_date (str): Date and time of the game in ISO 8601 format
        - status (str): Current status of the game
        - venue (str): Name of the stadium where the game is played
        - home_team (Dict): Home team information including name, abbreviation, and runs
        - away_team (Dict): Away team information including name, abbreviation, and runs
        - linescore (List[Dict]): Inning-by-inning scoring data
        - has_started (bool): Whether the game has started
        - is_complete (bool): Whether the game has finished
        - current_inning (int): Current inning being played if in progress
        - inning_state (str): Current state within the inning
        - weather (Dict): Weather conditions at the venue
    
    Raises:
        ValueError: If game_id is not a positive integer
    """
    # Input validation
    if not isinstance(game_id, int) or game_id <= 0:
        raise ValueError("game_id must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_linescore")
    
    # Construct home_team dictionary
    home_team = {
        "name": api_data["home_team_name"],
        "abbreviation": api_data["home_team_abbreviation"],
        "runs": {
            "total": api_data["home_team_total_runs"]
        }
    }
    
    # Construct away_team dictionary
    away_team = {
        "name": api_data["away_team_name"],
        "abbreviation": api_data["away_team_abbreviation"],
        "runs": {
            "total": api_data["away_team_total_runs"]
        }
    }
    
    # Construct linescore list from indexed fields
    linescore = [
        {
            "inning": api_data["linescore_0_inning"],
            "home_runs": api_data["linescore_0_home_runs"],
            "away_runs": api_data["linescore_0_away_runs"]
        },
        {
            "inning": api_data["linescore_1_inning"],
            "home_runs": api_data["linescore_1_home_runs"],
            "away_runs": api_data["linescore_1_away_runs"]
        }
    ]
    
    # Construct weather dictionary
    weather = {
        "temperature": api_data["weather_temperature"],
        "wind_speed": api_data["weather_wind_speed"],
        "humidity": api_data["weather_humidity"],
        "conditions": api_data["weather_conditions"]
    }
    
    # Build final result matching output schema
    result = {
        "game_id": api_data["game_id"],
        "game_date": api_data["game_date"],
        "status": api_data["status"],
        "venue": api_data["venue"],
        "home_team": home_team,
        "away_team": away_team,
        "linescore": linescore,
        "has_started": api_data["has_started"],
        "is_complete": api_data["is_complete"],
        "current_inning": api_data["current_inning"],
        "inning_state": api_data["inning_state"],
        "weather": weather
    }
    
    return result