from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching Formula 1 race results data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - year (str): The year for which race results are fetched
        - source (str): URL to the official source page
        - race_0_name (str): Name of the first race
        - race_0_url (str): URL of the first race
        - race_0_date (str): Date of the first race
        - race_0_winner_name (str): Winner's name in the first race
        - race_0_winner_car (str): Winning car in the first race
        - race_0_laps (int): Number of laps in the first race
        - race_0_time (str): Race time of the first race
        - race_1_name (str): Name of the second race
        - race_1_url (str): URL of the second race
        - race_1_date (str): Date of the second race
        - race_1_winner_name (str): Winner's name in the second race
        - race_1_winner_car (str): Winning car in the second race
        - race_1_laps (int): Number of laps in the second race
        - race_1_time (str): Race time of the second race
        - total_races (int): Total number of races in the year
    """
    return {
        "year": "2024",
        "source": "https://www.formula1.com/en/results.html/2024/races.html",
        "race_0_name": "Bahrain Grand Prix",
        "race_0_url": "https://www.formula1.com/en/results.html/2024/races/1234/bahrain.html",
        "race_0_date": "2024-03-02",
        "race_0_winner_name": "Max Verstappen",
        "race_0_winner_car": "Red Bull Racing RB20",
        "race_0_laps": 57,
        "race_0_time": "1:36:52.634",
        "race_1_name": "Saudi Arabian Grand Prix",
        "race_1_url": "https://www.formula1.com/en/results.html/2024/races/1235/saudi-arabia.html",
        "race_1_date": "2024-03-09",
        "race_1_winner_name": "Max Verstappen",
        "race_1_winner_car": "Red Bull Racing RB20",
        "race_1_laps": 50,
        "race_1_time": "1:26:33.514",
        "total_races": 24
    }

def formula_1_schedule_fetch_f1_race_results(year: str) -> Dict[str, Any]:
    """
    Fetches Formula 1 race results data for a specified year.
    
    Args:
        year (str): The year for which to fetch F1 data (e.g., '2024', '2025')
        
    Returns:
        Dictionary containing F1 race results information with the following structure:
        - year (str): the year for which the Formula 1 race results are fetched
        - source (str): URL to the official source page where the race results are published
        - races (List[Dict]): list of race entries, each containing 'name', 'url', 'date', 
          'winner_name', 'winner_car', 'laps', and 'time' fields
        - total_races (int): total number of races held in the specified year
    
    Raises:
        ValueError: If the year is not a valid 4-digit string
    """
    if not year or not year.isdigit() or len(year) != 4:
        raise ValueError("Year must be a valid 4-digit string (e.g., '2024')")

    # Fetch data from simulated external API
    api_data = call_external_api("formula-1-schedule-fetch_f1_race_results")
    
    # Construct the races list from indexed fields
    races = [
        {
            "name": api_data["race_0_name"],
            "url": api_data["race_0_url"],
            "date": api_data["race_0_date"],
            "winner_name": api_data["race_0_winner_name"],
            "winner_car": api_data["race_0_winner_car"],
            "laps": api_data["race_0_laps"],
            "time": api_data["race_0_time"]
        },
        {
            "name": api_data["race_1_name"],
            "url": api_data["race_1_url"],
            "date": api_data["race_1_date"],
            "winner_name": api_data["race_1_winner_name"],
            "winner_car": api_data["race_1_winner_car"],
            "laps": api_data["race_1_laps"],
            "time": api_data["race_1_time"]
        }
    ]
    
    # Build final result structure matching output schema
    result = {
        "year": api_data["year"],
        "source": api_data["source"],
        "races": races,
        "total_races": api_data["total_races"]
    }
    
    return result