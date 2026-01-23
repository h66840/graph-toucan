from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for professional matches.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - match_0_match_id (int): Match ID of the first professional match
        - match_0_radiant_team (str): Radiant team name of the first match
        - match_0_dire_team (str): Dire team name of the first match
        - match_0_league (str): League name of the first match
        - match_0_date (int): Match date as timestamp for the first match
        - match_0_duration (int): Duration of the first match in seconds
        - match_0_score_radiant (int): Radiant team score in the first match
        - match_0_score_dire (int): Dire team score in the first match
        - match_0_winner (str): Winner of the first match ('radiant' or 'dire')
        - match_1_match_id (int): Match ID of the second professional match
        - match_1_radiant_team (str): Radiant team name of the second match
        - match_1_dire_team (str): Dire team name of the second match
        - match_1_league (str): League name of the second match
        - match_1_date (int): Match date as timestamp for the second match
        - match_1_duration (int): Duration of the second match in seconds
        - match_1_score_radiant (int): Radiant team score in the second match
        - match_1_score_dire (int): Dire team score in the second match
        - match_1_winner (str): Winner of the second match ('radiant' or 'dire')
    """
    return {
        "match_0_match_id": 1234567890,
        "match_0_radiant_team": "Team Secret",
        "match_0_dire_team": "OG",
        "match_0_league": "The International 2023",
        "match_0_date": 1696543200,
        "match_0_duration": 2450,
        "match_0_score_radiant": 34,
        "match_0_score_dire": 28,
        "match_0_winner": "radiant",
        "match_1_match_id": 1234567891,
        "match_1_radiant_team": "Evil Geniuses",
        "match_1_dire_team": "PSG.LGD",
        "match_1_league": "ESL One Malaysia 2023",
        "match_1_date": 1696456800,
        "match_1_duration": 2100,
        "match_1_score_radiant": 22,
        "match_1_score_dire": 31,
        "match_1_winner": "dire"
    }

def opendota_api_server_get_pro_matches(limit: Optional[int] = 5) -> List[Dict[str, Any]]:
    """
    Get recent professional matches from the OpenDota API.
    
    Args:
        limit (Optional[int]): Number of matches to retrieve (default: 5). Maximum of 2 matches available in simulation.
    
    Returns:
        List of recent professional matches, each containing:
        - match_id (int): Unique identifier for the match
        - radiant_team (str): Name of the Radiant team
        - dire_team (str): Name of the Dire team
        - league (str): Name of the league/tournament
        - date (int): Match date as Unix timestamp
        - duration (int): Match duration in seconds
        - score_radiant (int): Final score for Radiant team
        - score_dire (int): Final score for Dire team
        - winner (str): Winner of the match ('radiant' or 'dire')
    
    Note:
        This is a simulated implementation. In a real scenario, this would make an API call
        to the OpenDota server. The current implementation returns mock data with up to 2 matches.
    """
    if limit is None:
        limit = 5
    
    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer")
    
    if limit <= 0:
        raise ValueError("Limit must be a positive integer")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("opendota-api-server-get_pro_matches")
    
    # Construct matches list from flattened API data
    matches: List[Dict[str, Any]] = []
    
    # Process up to 2 matches (based on available mock data)
    max_available = 2
    actual_limit = min(limit, max_available)
    
    for i in range(actual_limit):
        match_key_prefix = f"match_{i}"
        match = {
            "match_id": api_data[f"{match_key_prefix}_match_id"],
            "radiant_team": api_data[f"{match_key_prefix}_radiant_team"],
            "dire_team": api_data[f"{match_key_prefix}_dire_team"],
            "league": api_data[f"{match_key_prefix}_league"],
            "date": api_data[f"{match_key_prefix}_date"],
            "duration": api_data[f"{match_key_prefix}_duration"],
            "score_radiant": api_data[f"{match_key_prefix}_score_radiant"],
            "score_dire": api_data[f"{match_key_prefix}_score_dire"],
            "winner": api_data[f"{match_key_prefix}_winner"]
        }
        matches.append(match)
    
    return matches