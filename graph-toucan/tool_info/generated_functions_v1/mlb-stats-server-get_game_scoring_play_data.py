from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB game scoring play data.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - home_id (int): Home team ID
        - home_name (str): Home team full name
        - home_abbreviation (str): Home team abbreviation
        - home_teamName (str): Home team name
        - home_locationName (str): Home team location name
        - away_id (int): Away team ID
        - away_name (str): Away team full name
        - away_abbreviation (str): Away team abbreviation
        - away_teamName (str): Away team name
        - away_locationName (str): Away team location name
        - plays_0_result (str): Description and scores of first scoring play
        - plays_0_about_inning (int): Inning number of first scoring play
        - plays_0_about_halfInning (str): Half-inning ('top' or 'bottom') of first scoring play
        - plays_0_about_atBatIndex (int): At-bat index of first scoring play
        - plays_0_about_endTime (str): End time of first scoring play in ISO format
        - plays_0_atBatIndex (int): At-bat index of first scoring play
        - plays_1_result (str): Description and scores of second scoring play
        - plays_1_about_inning (int): Inning number of second scoring play
        - plays_1_about_halfInning (str): Half-inning ('top' or 'bottom') of second scoring play
        - plays_1_about_atBatIndex (int): At-bat index of second scoring play
        - plays_1_about_endTime (str): End time of second scoring play in ISO format
        - plays_1_atBatIndex (int): At-bat index of second scoring play
    """
    return {
        "home_id": 123,
        "home_name": "New York Yankees",
        "home_abbreviation": "NYY",
        "home_teamName": "Yankees",
        "home_locationName": "New York",
        "away_id": 120,
        "away_name": "Boston Red Sox",
        "away_abbreviation": "BOS",
        "away_teamName": "Red Sox",
        "away_locationName": "Boston",
        "plays_0_result": "Home run by Aaron Judge (435 ft), 2 RBI",
        "plays_0_about_inning": 3,
        "plays_0_about_halfInning": "bottom",
        "plays_0_about_atBatIndex": 5,
        "plays_0_about_endTime": "2023-06-15T21:45:30Z",
        "plays_0_atBatIndex": 5,
        "plays_1_result": "Solo home run by Rafael Devers",
        "plays_1_about_inning": 5,
        "plays_1_about_halfInning": "top",
        "plays_1_about_atBatIndex": 14,
        "plays_1_about_endTime": "2023-06-15T22:10:15Z",
        "plays_1_atBatIndex": 14
    }

def mlb_stats_server_get_game_scoring_play_data(game_id: int) -> Dict[str, Any]:
    """
    Returns a dictionary of scoring plays for a given MLB game.
    
    Args:
        game_id (int): The MLB game ID to retrieve scoring play data for.
        
    Returns:
        Dict containing:
        - home (Dict): Home team information including id, name, abbreviation, teamName, locationName
        - away (Dict): Away team information including id, name, abbreviation, teamName, locationName
        - plays (List[Dict]): Sorted list of scoring play data with result, about, and atBatIndex fields
        
    Raises:
        ValueError: If game_id is not a positive integer
    """
    if not isinstance(game_id, int) or game_id <= 0:
        raise ValueError("game_id must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("mlb-stats-server-get_game_scoring_play_data")
    
    # Construct home team data
    home = {
        "id": api_data["home_id"],
        "name": api_data["home_name"],
        "abbreviation": api_data["home_abbreviation"],
        "teamName": api_data["home_teamName"],
        "locationName": api_data["home_locationName"]
    }
    
    # Construct away team data
    away = {
        "id": api_data["away_id"],
        "name": api_data["away_name"],
        "abbreviation": api_data["away_abbreviation"],
        "teamName": api_data["away_teamName"],
        "locationName": api_data["away_locationName"]
    }
    
    # Construct plays list
    plays = [
        {
            "result": api_data["plays_0_result"],
            "about": {
                "inning": api_data["plays_0_about_inning"],
                "halfInning": api_data["plays_0_about_halfInning"],
                "atBatIndex": api_data["plays_0_about_atBatIndex"],
                "endTime": api_data["plays_0_about_endTime"]
            },
            "atBatIndex": api_data["plays_0_atBatIndex"]
        },
        {
            "result": api_data["plays_1_result"],
            "about": {
                "inning": api_data["plays_1_about_inning"],
                "halfInning": api_data["plays_1_about_halfInning"],
                "atBatIndex": api_data["plays_1_about_atBatIndex"],
                "endTime": api_data["plays_1_about_endTime"]
            },
            "atBatIndex": api_data["plays_1_atBatIndex"]
        }
    ]
    
    # Return the complete scoring play data
    return {
        "home": home,
        "away": away,
        "plays": plays
    }