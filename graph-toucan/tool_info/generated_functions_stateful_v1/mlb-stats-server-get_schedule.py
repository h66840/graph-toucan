from typing import Dict, List, Any, Optional
from datetime import datetime, date
import random

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
    Simulates fetching data from external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - game_0_game_id (int): Unique ID for the first game
        - game_0_date (str): Date of the first game in ISO format
        - game_0_home_team (str): Home team name for the first game
        - game_0_away_team (str): Away team name for the first game
        - game_0_venue (str): Venue name for the first game
        - game_0_start_time (str): Start time of the first game in HH:MM format
        - game_0_status (str): Current status of the first game (e.g., 'In Progress', 'Final')
        - game_0_home_score (int): Home team score for the first game
        - game_0_away_score (int): Away team score for the first game
        - game_0_inning (int): Current inning of the first game
        - game_0_is_completed (bool): Whether the first game is completed
        - game_0_series_status (str): Series status for the first game if requested
        - game_1_game_id (int): Unique ID for the second game
        - game_1_date (str): Date of the second game in ISO format
        - game_1_home_team (str): Home team name for the second game
        - game_1_away_team (str): Away team name for the second game
        - game_1_venue (str): Venue name for the second game
        - game_1_start_time (str): Start time of the second game in HH:MM format
        - game_1_status (str): Current status of the second game
        - game_1_home_score (int): Home team score for the second game
        - game_1_away_score (int): Away team score for the second game
        - game_1_inning (int): Current inning of the second game
        - game_1_is_completed (bool): Whether the second game is completed
        - game_1_series_status (str): Series status for the second game if requested
        - total_games (int): Total number of games returned
        - filter_start_date (str): Start date used in filter, ISO format
        - filter_end_date (str): End date used in filter, ISO format
        - filter_team_id (int): Team ID used in filter
        - filter_opponent_id (int): Opponent ID used in filter
        - filter_season (int): Season year used in filter
        - has_more (bool): Whether more games are available beyond this response
        - metadata_api_version (str): Version of the API
        - metadata_request_timestamp (str): Timestamp of the request in ISO format
        - metadata_sport_name (str): Name of the sport ('MLB')
        - metadata_notes (str): Processing notes
    """
    today = date.today().isoformat()
    return {
        "game_0_game_id": 1001,
        "game_0_date": today,
        "game_0_home_team": "New York Yankees",
        "game_0_away_team": "Boston Red Sox",
        "game_0_venue": "Yankee Stadium",
        "game_0_start_time": "19:05",
        "game_0_status": "In Progress",
        "game_0_home_score": 4,
        "game_0_away_score": 3,
        "game_0_inning": 7,
        "game_0_is_completed": False,
        "game_0_series_status": "Yankees lead 2-1",

        "game_1_game_id": 1002,
        "game_1_date": today,
        "game_1_home_team": "Los Angeles Dodgers",
        "game_1_away_team": "San Diego Padres",
        "game_1_venue": "Dodger Stadium",
        "game_1_start_time": "20:10",
        "game_1_status": "Scheduled",
        "game_1_home_score": 0,
        "game_1_away_score": 0,
        "game_1_inning": 1,
        "game_1_is_completed": False,
        "game_1_series_status": "Series tied 1-1",

        "total_games": 2,
        "filter_start_date": today,
        "filter_end_date": today,
        "filter_team_id": 123,
        "filter_opponent_id": 456,
        "filter_season": 2023,
        "has_more": False,
        "metadata_api_version": "1.0",
        "metadata_request_timestamp": datetime.now().isoformat(),
        "metadata_sport_name": "MLB",
        "metadata_notes": "Simulated data for demonstration"
    }


def mlb_stats_server_get_schedule(
    date: Optional[str] = None,
    end_date: Optional[str] = None,
    game_id: Optional[str] = None,
    include_series_status: Optional[bool] = None,
    opponent_id: Optional[str] = None,
    season: Optional[str] = None,
    sport_id: Optional[int] = None,
    start_date: Optional[str] = None,
    team_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get list of games for a given date/range and/or team/opponent.
    
    Args:
        date (Optional[str]): Specific date to query games for (YYYY-MM-DD)
        end_date (Optional[str]): End date for range query (YYYY-MM-DD)
        game_id (Optional[str]): Specific game ID to filter by
        include_series_status (Optional[bool]): Whether to include series status in results
        opponent_id (Optional[str]): Filter games by opponent team ID
        season (Optional[str]): Filter games by season year
        sport_id (Optional[int]): Sport ID (MLB is typically 1)
        start_date (Optional[str]): Start date for range query (YYYY-MM-DD)
        team_id (Optional[str]): Filter games by team ID (home or away)
    
    Returns:
        Dict containing:
        - games (List[Dict]): List of game objects with details like game_id, date, teams, scores, etc.
        - total_games (int): Number of games returned
        - filters_applied (Dict): Summary of filters used in the request
        - has_more (bool): Whether more games are available beyond this response
        - metadata (Dict): Contextual information about the request and API
    """
    # Call external API to get flat data
    api_data = call_external_api("mlb-stats-server-get_schedule", **locals())
    
    # Construct games list from indexed fields
    games = []
    
    for i in range(2):  # We have two games (0 and 1)
        game_key_prefix = f"game_{i}"
        if f"{game_key_prefix}_game_id" not in api_data:
            continue
            
        game = {
            "game_id": api_data[f"{game_key_prefix}_game_id"],
            "date": api_data[f"{game_key_prefix}_date"],
            "home_team": api_data[f"{game_key_prefix}_home_team"],
            "away_team": api_data[f"{game_key_prefix}_away_team"],
            "venue": api_data[f"{game_key_prefix}_venue"],
            "start_time": api_data[f"{game_key_prefix}_start_time"],
            "status": api_data[f"{game_key_prefix}_status"],
            "home_score": api_data[f"{game_key_prefix}_home_score"],
            "away_score": api_data[f"{game_key_prefix}_away_score"],
            "inning": api_data[f"{game_key_prefix}_inning"],
            "is_completed": api_data[f"{game_key_prefix}_is_completed"]
        }
        
        # Add series_status only if it was requested or available
        series_status_key = f"{game_key_prefix}_series_status"
        if include_series_status and series_status_key in api_data:
            game["series_status"] = api_data[series_status_key]
            
        games.append(game)
    
    # Construct filters_applied from available filter data
    filters_applied = {}
    if "filter_start_date" in api_data:
        filters_applied["start_date"] = api_data["filter_start_date"]
    if "filter_end_date" in api_data:
        filters_applied["end_date"] = api_data["filter_end_date"]
    if "filter_team_id" in api_data:
        filters_applied["team_id"] = api_data["filter_team_id"]
    if "filter_opponent_id" in api_data:
        filters_applied["opponent_id"] = api_data["filter_opponent_id"]
    if "filter_season" in api_data:
        filters_applied["season"] = api_data["filter_season"]
    
    # Construct metadata
    metadata = {
        "api_version": api_data["metadata_api_version"],
        "request_timestamp": api_data["metadata_request_timestamp"],
        "sport_name": api_data["metadata_sport_name"],
        "processing_notes": api_data["metadata_notes"]
    }
    
    # Final result structure
    result = {
        "games": games,
        "total_games": api_data["total_games"],
        "filters_applied": filters_applied,
        "has_more": api_data["has_more"],
        "metadata": metadata
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
