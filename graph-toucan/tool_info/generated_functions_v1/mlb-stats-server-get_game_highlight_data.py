from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching highlight data from an external MLB stats server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - highlights_0_title (str): Title of the first highlight
        - highlights_0_description (str): Description of the first highlight
        - highlights_0_type (str): Type of the first highlight (e.g., home run)
        - highlights_0_timestamp (str): Timestamp in the game for the first highlight
        - highlights_0_video_url (str): Video URL for the first highlight
        - highlights_0_duration (int): Duration in seconds of the first highlight
        - highlights_0_players_involved (str): Comma-separated list of players involved in the first highlight
        - highlights_1_title (str): Title of the second highlight
        - highlights_1_description (str): Description of the second highlight
        - highlights_1_type (str): Type of the second highlight
        - highlights_1_timestamp (str): Timestamp in the game for the second highlight
        - highlights_1_video_url (str): Video URL for the second highlight
        - highlights_1_duration (int): Duration in seconds of the second highlight
        - highlights_1_players_involved (str): Comma-separated list of players involved in the second highlight
        - game_id (int): The unique identifier of the game
        - game_date (str): ISO 8601 date-time string indicating when the game was played
        - teams_away_name (str): Full name of the away team
        - teams_away_abbr (str): Abbreviation of the away team
        - teams_home_name (str): Full name of the home team
        - teams_home_abbr (str): Abbreviation of the home team
        - total_highlights (int): Total number of highlights returned
        - has_video (bool): Whether full video content is available
        - source (str): Name of the data/video source
    """
    return {
        "highlights_0_title": "Walk-off Home Run",
        "highlights_0_description": "Player hits a dramatic walk-off home run in the 9th inning.",
        "highlights_0_type": "home run",
        "highlights_0_timestamp": "8.2",
        "highlights_0_video_url": "https://videos.mlb.com/clip1.mp4",
        "highlights_0_duration": 45,
        "highlights_0_players_involved": "Mike Trout",
        "highlights_1_title": "Strikeout to End Game",
        "highlights_1_description": "Closer strikes out the final batter to seal the win.",
        "highlights_1_type": "strikeout",
        "highlights_1_timestamp": "9.0",
        "highlights_1_video_url": "https://videos.mlb.com/clip2.mp4",
        "highlights_1_duration": 30,
        "highlights_1_players_involved": "Shohei Ohtani",
        "game_id": 123456,
        "game_date": "2023-06-15T19:05:00Z",
        "teams_away_name": "Los Angeles Angels",
        "teams_away_abbr": "LAA",
        "teams_home_name": "New York Yankees",
        "teams_home_abbr": "NYY",
        "total_highlights": 2,
        "has_video": True,
        "source": "MLB Official"
    }

def mlb_stats_server_get_game_highlight_data(game_id: int) -> Dict[str, Any]:
    """
    Returns a list of highlight data for a given game.
    
    Args:
        game_id (int): The unique identifier of the game to retrieve highlights for.
        
    Returns:
        Dict containing:
        - highlights (List[Dict]): List of highlight clips or moments from the game.
          Each dict includes title, description, type, timestamp, video URL, duration, and players involved.
        - game_id (int): The unique identifier of the game.
        - game_date (str): ISO 8601 date-time string indicating when the game was played.
        - teams (Dict): Contains 'away' and 'home' team names and abbreviations.
        - total_highlights (int): Total number of highlights returned.
        - has_video (bool): Indicates whether full video content is available.
        - source (str): Name or identifier of the data/video source.
        
    Raises:
        ValueError: If game_id is not a positive integer.
    """
    if not isinstance(game_id, int) or game_id <= 0:
        raise ValueError("game_id must be a positive integer")
    
    # Fetch simulated external data
    api_data = call_external_api("mlb-stats-server-get_game_highlight_data")
    
    # Construct highlights list from indexed fields
    highlights = [
        {
            "title": api_data["highlights_0_title"],
            "description": api_data["highlights_0_description"],
            "type": api_data["highlights_0_type"],
            "timestamp": api_data["highlights_0_timestamp"],
            "video_url": api_data["highlights_0_video_url"],
            "duration": api_data["highlights_0_duration"],
            "players_involved": api_data["highlights_0_players_involved"].split(", ") if api_data["highlights_0_players_involved"] else []
        },
        {
            "title": api_data["highlights_1_title"],
            "description": api_data["highlights_1_description"],
            "type": api_data["highlights_1_type"],
            "timestamp": api_data["highlights_1_timestamp"],
            "video_url": api_data["highlights_1_video_url"],
            "duration": api_data["highlights_1_duration"],
            "players_involved": api_data["highlights_1_players_involved"].split(", ") if api_data["highlights_1_players_involved"] else []
        }
    ]
    
    # Construct teams dictionary
    teams = {
        "away": {
            "name": api_data["teams_away_name"],
            "abbreviation": api_data["teams_away_abbr"]
        },
        "home": {
            "name": api_data["teams_home_name"],
            "abbreviation": api_data["teams_home_abbr"]
        }
    }
    
    # Build final result structure
    result = {
        "highlights": highlights,
        "game_id": api_data["game_id"],
        "game_date": api_data["game_date"],
        "teams": teams,
        "total_highlights": api_data["total_highlights"],
        "has_video": api_data["has_video"],
        "source": api_data["source"]
    }
    
    return result