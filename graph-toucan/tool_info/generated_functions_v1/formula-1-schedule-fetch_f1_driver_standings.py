from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for F1 driver standings.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - year (str): The year for which the driver standings are fetched
        - source (str): URL source of the driver standings data
        - driver_0_position (int): Position of the first driver in standings
        - driver_0_name (str): Name of the first driver
        - driver_0_code (str): Code (abbreviation) of the first driver
        - driver_0_nationality (str): Nationality of the first driver
        - driver_0_team (str): Team name of the first driver
        - driver_0_points (int): Points scored by the first driver
        - driver_1_position (int): Position of the second driver in standings
        - driver_1_name (str): Name of the second driver
        - driver_1_code (str): Code (abbreviation) of the second driver
        - driver_1_nationality (str): Nationality of the second driver
        - driver_1_team (str): Team name of the second driver
        - driver_1_points (int): Points scored by the second driver
    """
    return {
        "year": "2024",
        "source": "https://example-f1-standings.com/2024",
        "driver_0_position": 1,
        "driver_0_name": "Max Verstappen",
        "driver_0_code": "VER",
        "driver_0_nationality": "Dutch",
        "driver_0_team": "Red Bull Racing",
        "driver_0_points": 374,
        "driver_1_position": 2,
        "driver_1_name": "Sergio Perez",
        "driver_1_code": "PER",
        "driver_1_nationality": "Mexican",
        "driver_1_team": "Red Bull Racing",
        "driver_1_points": 280,
    }

def formula_1_schedule_fetch_f1_driver_standings(year: str) -> Dict[str, Any]:
    """
    Fetches Formula 1 driver standings data for a specified year.

    Args:
        year (str): The year for which to fetch F1 data (e.g., '2024', '2025')

    Returns:
        Dictionary with F1 driver standings information containing:
        - year (str): the year for which the driver standings are fetched
        - source (str): URL source of the driver standings data
        - drivers (List[Dict]): list of driver standings, each with 'position', 'name', 'code', 'nationality', 'team', and 'points' fields
        - total_drivers (int): total number of drivers in the standings
    """
    if not year:
        raise ValueError("Year is required and cannot be empty.")

    api_data = call_external_api("formula-1-schedule-fetch_f1_driver_standings")

    # Construct drivers list from flattened API response
    drivers = [
        {
            "position": api_data["driver_0_position"],
            "name": api_data["driver_0_name"],
            "code": api_data["driver_0_code"],
            "nationality": api_data["driver_0_nationality"],
            "team": api_data["driver_0_team"],
            "points": api_data["driver_0_points"],
        },
        {
            "position": api_data["driver_1_position"],
            "name": api_data["driver_1_name"],
            "code": api_data["driver_1_code"],
            "nationality": api_data["driver_1_nationality"],
            "team": api_data["driver_1_team"],
            "points": api_data["driver_1_points"],
        },
    ]

    result = {
        "year": api_data["year"],
        "source": api_data["source"],
        "drivers": drivers,
        "total_drivers": len(drivers),
    }

    return result