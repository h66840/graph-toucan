from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Formula 1 calendar.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - year (str): The year of the F1 calendar
        - source (str): Official URL source of the F1 calendar data
        - race_0_name (str): Name of the first race/circuit
        - race_0_round (int): Round number of the first race
        - race_0_url (str): Official link to the first race page
        - race_0_is_testing (bool): Whether the first event is a test session
        - race_1_name (str): Name of the second race/circuit
        - race_1_round (int): Round number of the second race
        - race_1_url (str): Official link to the second race page
        - race_1_is_testing (bool): Whether the second event is a test session
        - total_races (int): Total number of events in the calendar
    """
    return {
        "year": "2024",
        "source": "https://www.formula1.com/en/racing/2024.html",
        "race_0_name": "Bahrain Grand Prix",
        "race_0_round": 1,
        "race_0_url": "https://www.formula1.com/en/racing/2024/Bahrain.html",
        "race_0_is_testing": False,
        "race_1_name": "Pre-Season Testing",
        "race_1_round": 0,
        "race_1_url": "https://www.formula1.com/en/racing/2024/Testing.html",
        "race_1_is_testing": True,
        "total_races": 23
    }

def formula_1_schedule_fetch_f1_calendar(year: str) -> Dict[str, Any]:
    """
    Fetches Formula 1 calendar data for a specified year.

    Args:
        year (str): The year for which to fetch F1 data (e.g., '2024', '2025')

    Returns:
        Dictionary with F1 calendar information containing:
        - year (str): The year of the calendar
        - source (str): Official source URL
        - races (List[Dict]): List of race events with name, round, url, and optional is_testing
        - total_races (int): Total number of events including races and tests
    """
    if not year:
        raise ValueError("Year is required and cannot be empty")

    # Call the external API to get flattened data
    api_data = call_external_api("formula-1-schedule-fetch_f1_calendar")

    # Construct the races list from indexed fields
    races: List[Dict[str, Any]] = [
        {
            "name": api_data["race_0_name"],
            "round": api_data["race_0_round"],
            "url": api_data["race_0_url"],
            "is_testing": api_data["race_0_is_testing"]
        },
        {
            "name": api_data["race_1_name"],
            "round": api_data["race_1_round"],
            "url": api_data["race_1_url"],
            "is_testing": api_data["race_1_is_testing"]
        }
    ]

    # Build the final result matching the output schema
    result: Dict[str, Any] = {
        "year": api_data["year"],
        "source": api_data["source"],
        "races": races,
        "total_races": api_data["total_races"]
    }

    return result