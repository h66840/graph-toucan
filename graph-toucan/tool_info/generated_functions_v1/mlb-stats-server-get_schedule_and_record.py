from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external MLB stats server API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - team_abbreviation (str): The team's MLB abbreviation (e.g., "PHI", "LAD")
        - season (int): The season year for which data is retrieved
        - record_summary_wins (int): Number of wins in the season
        - record_summary_losses (int): Number of losses in the season
        - record_summary_ties (int): Number of tied games
        - record_summary_win_percentage (float): Win percentage (0.0 to 1.0)
        - has_completed_season (bool): Whether the season has concluded
        - total_games_played (int): Number of games already completed
        - total_games_scheduled (int): Total number of games scheduled in the season
        - future_games_count (int): Number of upcoming games
        - attendance_stats_average (float): Average attendance per game
        - attendance_stats_total (int): Total attendance across all games
        - attendance_stats_highest (int): Highest attendance in a single game
        - attendance_stats_lowest (int): Lowest attendance in a single game
        - game_0_date (str): ISO format date of first game
        - game_0_opponent (str): Opponent team abbreviation for first game
        - game_0_location (str): Location of first game ("home" or "away")
        - game_0_result (str): Result of first game ("W", "L", "T", or null as empty string)
        - game_0_score_for (int): Runs scored by the queried team in first game
        - game_0_score_against (int): Runs scored by opponent in first game
        - game_0_winning_pitcher (str): Winning pitcher name for first game
        - game_0_losing_pitcher (str): Losing pitcher name for first game
        - game_0_save_pitcher (str): Save pitcher name for first game
        - game_0_attendance (int): Attendance at first game
        - game_0_game_status (str): Status of first game ("completed", "scheduled", etc.)
        - game_1_date (str): ISO format date of second game
        - game_1_opponent (str): Opponent team abbreviation for second game
        - game_1_location (str): Location of second game ("home" or "away")
        - game_1_result (str): Result of second game ("W", "L", "T", or null as empty string)
        - game_1_score_for (int): Runs scored by the queried team in second game
        - game_1_score_against (int): Runs scored by opponent in second game
        - game_1_winning_pitcher (str): Winning pitcher name for second game
        - game_1_losing_pitcher (str): Losing pitcher name for second game
        - game_1_save_pitcher (str): Save pitcher name for second game
        - game_1_attendance (int): Attendance at second game
        - game_1_game_status (str): Status of second game ("completed", "scheduled", etc.)
    """
    # Simulate realistic data based on inputs
    is_completed = random.choice([True, False])
    total_scheduled = 162
    played = total_scheduled if is_completed else random.randint(50, 161)
    future = total_scheduled - played

    wins = random.randint(played // 3, played // 2)
    losses = played - wins - random.randint(0, 2)  # up to 2 ties
    ties = played - wins - losses
    win_pct = round(wins / played, 3) if played > 0 else 0.0

    avg_att = random.randint(25000, 45000)
    total_att = avg_att * played
    high_att = random.randint(int(avg_att * 1.1), int(avg_att * 1.3))
    low_att = random.randint(int(avg_att * 0.7), int(avg_att * 0.9))

    teams = ["PHI", "BOS", "LAD", "NYY", "SFG", "CHC", "ATL", "HOU"]
    pitchers = [
        "Zack Wheeler",
        "Aaron Nola",
        "Max Scherzer",
        "Justin Verlander",
        "Clayton Kershaw",
        "Yu Darvish",
    ]

    game_status_0 = "completed" if random.random() > 0.1 else "postponed"
    game_status_1 = "scheduled" if future > 0 else "completed"

    base_date = datetime(season, 4, 1)  # Start of MLB season
    date_0 = (base_date + timedelta(days=random.randint(0, 160))).strftime("%Y-%m-%d")
    date_1 = (base_date + timedelta(days=random.randint(1, 161))).strftime("%Y-%m-%d")

    return {
        "team_abbreviation": random.choice(teams),
        "season": season,
        "record_summary_wins": wins,
        "record_summary_losses": losses,
        "record_summary_ties": ties,
        "record_summary_win_percentage": win_pct,
        "has_completed_season": is_completed,
        "total_games_played": played,
        "total_games_scheduled": total_scheduled,
        "future_games_count": future,
        "attendance_stats_average": float(avg_att),
        "attendance_stats_total": total_att,
        "attendance_stats_highest": high_att,
        "attendance_stats_lowest": low_att,
        "game_0_date": date_0,
        "game_0_opponent": random.choice([t for t in teams if t != team]),
        "game_0_location": random.choice(["home", "away"]),
        "game_0_result": random.choice(["W", "L", "T"]) if game_status_0 == "completed" else "",
        "game_0_score_for": random.randint(0, 12),
        "game_0_score_against": random.randint(0, 12),
        "game_0_winning_pitcher": random.choice(pitchers),
        "game_0_losing_pitcher": random.choice(pitchers),
        "game_0_save_pitcher": random.choice(pitchers),
        "game_0_attendance": random.randint(20000, 50000) if game_status_0 == "completed" else 0,
        "game_0_game_status": game_status_0,
        "game_1_date": date_1,
        "game_1_opponent": random.choice([t for t in teams if t != team]),
        "game_1_location": random.choice(["home", "away"]),
        "game_1_result": random.choice(["W", "L", "T"]) if game_status_1 == "completed" else "",
        "game_1_score_for": random.randint(0, 12),
        "game_1_score_against": random.randint(0, 12),
        "game_1_winning_pitcher": random.choice(pitchers),
        "game_1_losing_pitcher": random.choice(pitchers),
        "game_1_save_pitcher": random.choice(pitchers),
        "game_1_attendance": random.randint(20000, 50000) if game_status_1 == "completed" else 0,
        "game_1_game_status": game_1,
    }


def mlb_stats_server_get_schedule_and_record(season: int, team: str) -> Dict[str, Any]:
    """
    Retrieve a team's game-level results for a given season, including win/loss/tie result, score, attendance,
    and winning/losing/saving pitcher. If the season is incomplete, it will provide scheduling information for
    future games.

    Args:
        season (int): The season for which you want a team's record data.
        team (str): The abbreviation of the team for which you are requesting data (e.g. "PHI", "BOS", "LAD").

    Returns:
        Dict containing:
        - games (List[Dict]): List of game entries with detailed game information
        - team_abbreviation (str): The team's MLB abbreviation
        - season (int): The season year
        - record_summary (Dict): Summary of wins, losses, ties, and win percentage
        - has_completed_season (bool): Whether the season has ended
        - total_games_played (int): Number of completed games
        - total_games_scheduled (int): Total games in the season
        - future_games_count (int): Number of upcoming games
        - attendance_stats (Dict): Aggregated attendance data
    """
    # Input validation
    if not isinstance(season, int) or season < 1876 or season > datetime.now().year + 1:
        raise ValueError("Season must be a valid year between 1876 and next year.")
    if not isinstance(team, str) or not team.isalpha() or len(team) != 3:
        raise ValueError("Team must be a valid 3-letter MLB team abbreviation.")

    team = team.upper()