from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB boxscore.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - home_team_name (str): Name of the home team
        - home_team_runs (int): Runs scored by home team
        - home_team_hits (int): Hits by home team
        - home_team_errors (int): Errors by home team
        - away_team_name (str): Name of the away team
        - away_team_runs (int): Runs scored by away team
        - away_team_hits (int): Hits by away team
        - away_team_errors (int): Errors by away team
        - game_info_date (str): Game date
        - game_info_venue (str): Venue name
        - game_info_attendance (int): Attendance count
        - game_info_start_time (str): Game start time
        - game_info_status (str): Game status
        - linescore_0_inning (int): First inning number
        - linescore_0_home_score (int): Home team score in first inning
        - linescore_0_away_score (int): Away team score in first inning
        - linescore_1_inning (int): Second inning number
        - linescore_1_home_score (int): Home team score in second inning
        - linescore_1_away_score (int): Away team score in second inning
        - pitching_summary_0_name (str): First pitcher name
        - pitching_summary_0_ip (float): Innings pitched
        - pitching_summary_0_er (int): Earned runs allowed
        - pitching_summary_0_so (int): Strikeouts
        - pitching_summary_0_bb (int): Walks
        - pitching_summary_0_decision (str): Decision (W, L, SV)
        - pitching_summary_1_name (str): Second pitcher name
        - pitching_summary_1_ip (float): Innings pitched
        - pitching_summary_1_er (int): Earned runs allowed
        - pitching_summary_1_so (int): Strikeouts
        - pitching_summary_1_bb (int): Walks
        - pitching_summary_1_decision (str): Decision (W, L, SV)
        - status (str): Current game status
        - duration (str): Game duration in HH:MM format
        - umpires_0_name (str): First umpire name
        - umpires_0_position (str): First umpire position
        - umpires_1_name (str): Second umpire name
        - umpires_1_position (str): Second umpire position
        - weather_temperature (int): Temperature in degrees
        - weather_wind_speed (int): Wind speed in mph
        - weather_field_condition (str): Field condition (e.g., "Dry", "Wet")
    """
    return {
        "home_team_name": "New York Yankees",
        "home_team_runs": 5,
        "home_team_hits": 8,
        "home_team_errors": 1,
        "away_team_name": "Boston Red Sox",
        "away_team_runs": 3,
        "away_team_hits": 7,
        "away_team_errors": 2,
        "game_info_date": "2023-09-15",
        "game_info_venue": "Yankee Stadium",
        "game_info_attendance": 47893,
        "game_info_start_time": "19:08",
        "game_info_status": "Final",
        "linescore_0_inning": 1,
        "linescore_0_home_score": 2,
        "linescore_0_away_score": 0,
        "linescore_1_inning": 2,
        "linescore_1_home_score": 1,
        "linescore_1_away_score": 2,
        "pitching_summary_0_name": "Gerrit Cole",
        "pitching_summary_0_ip": 7.0,
        "pitching_summary_0_er": 2,
        "pitching_summary_0_so": 9,
        "pitching_summary_0_bb": 1,
        "pitching_summary_0_decision": "W",
        "pitching_summary_1_name": "Kenley Jansen",
        "pitching_summary_1_ip": 1.0,
        "pitching_summary_1_er": 1,
        "pitching_summary_1_so": 2,
        "pitching_summary_1_bb": 0,
        "pitching_summary_1_decision": "SV",
        "status": "Final",
        "duration": "3:15",
        "umpires_0_name": "Joe West",
        "umpires_0_position": "HP",
        "umpires_1_name": "Derek Thomas",
        "umpires_1_position": "1B",
        "weather_temperature": 72,
        "weather_wind_speed": 8,
        "weather_field_condition": "Dry"
    }

def mlb_stats_server_get_boxscore(game_id: int, timecode: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a formatted boxscore for a given MLB game.

    Args:
        game_id (int): The unique identifier for the MLB game.
        timecode (Optional[str]): Optional timecode to retrieve boxscore at a specific point in time.

    Returns:
        Dict containing:
        - home_team (Dict): Home team stats including name, runs, hits, errors, and player stats
        - away_team (Dict): Away team stats including name, runs, hits, errors, and player stats
        - game_info (Dict): Metadata about the game (date, venue, attendance, start time, status)
        - linescore (List[Dict]): Inning-by-inning breakdown of runs
        - pitching_summary (List[Dict]): Summary of pitchers used with key stats and decisions
        - status (str): Current game status (e.g., 'Final', 'InProgress', 'Scheduled')
        - duration (str): Length of the game in hours and minutes
        - umpires (List[Dict]): Names and positions of umpires
        - weather (Dict): Game-time weather conditions

    Raises:
        ValueError: If game_id is not a positive integer
    """
    if not isinstance(game_id, int) or game_id <= 0:
        raise ValueError("game_id must be a positive integer")

    # Fetch data from external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_boxscore")

    # Construct home_team
    home_team = {
        "name": api_data["home_team_name"],
        "runs": api_data["home_team_runs"],
        "hits": api_data["home_team_hits"],
        "errors": api_data["home_team_errors"],
        "player_statistics": []  # Placeholder as no specific player data in API
    }

    # Construct away_team
    away_team = {
        "name": api_data["away_team_name"],
        "runs": api_data["away_team_runs"],
        "hits": api_data["away_team_hits"],
        "errors": api_data["away_team_errors"],
        "player_statistics": []  # Placeholder as no specific player data in API
    }

    # Construct game_info
    game_info = {
        "date": api_data["game_info_date"],
        "venue": api_data["game_info_venue"],
        "attendance": api_data["game_info_attendance"],
        "start_time": api_data["game_info_start_time"],
        "status": api_data["game_info_status"]
    }

    # Construct linescore
    linescore = [
        {
            "inning": api_data["linescore_0_inning"],
            "home_score": api_data["linescore_0_home_score"],
            "away_score": api_data["linescore_0_away_score"]
        },
        {
            "inning": api_data["linescore_1_inning"],
            "home_score": api_data["linescore_1_home_score"],
            "away_score": api_data["linescore_1_away_score"]
        }
    ]

    # Construct pitching_summary
    pitching_summary = [
        {
            "name": api_data["pitching_summary_0_name"],
            "ip": api_data["pitching_summary_0_ip"],
            "er": api_data["pitching_summary_0_er"],
            "so": api_data["pitching_summary_0_so"],
            "bb": api_data["pitching_summary_0_bb"],
            "decision": api_data["pitching_summary_0_decision"]
        },
        {
            "name": api_data["pitching_summary_1_name"],
            "ip": api_data["pitching_summary_1_ip"],
            "er": api_data["pitching_summary_1_er"],
            "so": api_data["pitching_summary_1_so"],
            "bb": api_data["pitching_summary_1_bb"],
            "decision": api_data["pitching_summary_1_decision"]
        }
    ]

    # Construct umpires
    umpires = [
        {
            "name": api_data["umpires_0_name"],
            "position": api_data["umpires_0_position"]
        },
        {
            "name": api_data["umpires_1_name"],
            "position": api_data["umpires_1_position"]
        }
    ]

    # Construct weather
    weather = {
        "temperature": api_data["weather_temperature"],
        "wind_speed": api_data["weather_wind_speed"],
        "field_condition": api_data["weather_field_condition"]
    }

    # Return the complete boxscore
    return {
        "home_team": home_team,
        "away_team": away_team,
        "game_info": game_info,
        "linescore": linescore,
        "pitching_summary": pitching_summary,
        "status": api_data["status"],
        "duration": api_data["duration"],
        "umpires": umpires,
        "weather": weather
    }