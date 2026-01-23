from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for F1 team standings.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - year (str): The year for which the team standings are fetched
        - source (str): URL to the official source of the standings data
        - team_0_position (str): Position of the first team in standings
        - team_0_name (str): Name of the first team
        - team_0_points (str): Points of the first team
        - team_1_position (str): Position of the second team in standings
        - team_1_name (str): Name of the second team
        - team_1_points (str): Points of the second team
        - total_teams (int): Total number of teams in the standings
    """
    return {
        "year": "2024",
        "source": "https://www.formula1.com/en/results.html/2024/team.html",
        "team_0_position": "1",
        "team_0_name": "Red Bull Racing",
        "team_0_points": "400",
        "team_1_position": "2",
        "team_1_name": "Mercedes",
        "team_1_points": "320",
        "total_teams": 10
    }

def formula_1_schedule_fetch_f1_team_standings(year: str) -> Dict[str, Any]:
    """
    Fetches Formula 1 team standings data for a specified year.

    Args:
        year (str): The year for which to fetch F1 data (e.g., '2024', '2025')

    Returns:
        Dictionary with F1 team standings information containing:
        - year (str): the year for which the team standings are fetched
        - source (str): URL to the official source of the standings data
        - teams (List[Dict]): list of team standings, each with 'position' (str), 'name' (str), and 'points' (str) fields
        - total_teams (int): total number of teams in the standings
    """
    if not year:
        raise ValueError("Year is required and cannot be empty")

    # Call the external API to get the data (simulated)
    api_data = call_external_api("formula-1-schedule-fetch_f1_team_standings")

    # Construct the teams list from flattened API response
    teams = [
        {
            "position": api_data["team_0_position"],
            "name": api_data["team_0_name"],
            "points": api_data["team_0_points"]
        },
        {
            "position": api_data["team_1_position"],
            "name": api_data["team_1_name"],
            "points": api_data["team_1_points"]
        }
    ]

    # Build the final result structure as per output schema
    result = {
        "year": api_data["year"],
        "source": api_data["source"],
        "teams": teams,
        "total_teams": api_data["total_teams"]
    }

    return result