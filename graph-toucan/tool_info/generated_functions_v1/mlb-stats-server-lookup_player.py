from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB player lookup.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_0_id (int): First player's ID
        - results_0_first_name (str): First player's first name
        - results_0_last_name (str): First player's last name
        - results_0_team (str): First player's team
        - results_0_position (str): First player's position
        - results_0_career_start (int): First player's career start year
        - results_0_career_end (int): First player's career end year
        - results_1_id (int): Second player's ID
        - results_1_first_name (str): Second player's first name
        - results_1_last_name (str): Second player's last name
        - results_1_team (str): Second player's team
        - results_1_position (str): Second player's position
        - results_1_career_start (int): Second player's career start year
        - results_1_career_end (int): Second player's career end year
        - total_found (int): Total number of players matching the search
        - exact_match_id (int): ID of the exact match player
        - exact_match_first_name (str): First name of the exact match player
        - exact_match_last_name (str): Last name of the exact match player
        - exact_match_team (str): Team of the exact match player
        - exact_match_position (str): Position of the exact match player
        - exact_match_career_start (int): Career start year of the exact match player
        - exact_match_career_end (int): Career end year of the exact match player
        - metadata_processing_time (float): Time taken to process the query in seconds
        - metadata_source_version (str): Version of the data source
        - metadata_warning (str): Warning message if name is ambiguous
    """
    return {
        "results_0_id": 12345,
        "results_0_first_name": "Mike",
        "results_0_last_name": "Trout",
        "results_0_team": "Los Angeles Angels",
        "results_0_position": "CF",
        "results_0_career_start": 2011,
        "results_0_career_end": 2023,
        "results_1_id": 12346,
        "results_1_first_name": "Mike",
        "results_1_last_name": "Minor",
        "results_1_team": "Cincinnati Reds",
        "results_1_position": "P",
        "results_1_career_start": 2010,
        "results_1_career_end": 2023,
        "total_found": 2,
        "exact_match_id": 12345,
        "exact_match_first_name": "Mike",
        "exact_match_last_name": "Trout",
        "exact_match_team": "Los Angeles Angels",
        "exact_match_position": "CF",
        "exact_match_career_start": 2011,
        "exact_match_career_end": 2023,
        "metadata_processing_time": 0.12,
        "metadata_source_version": "v2.3.1",
        "metadata_warning": "Ambiguous name: multiple players found"
    }

def mlb_stats_server_lookup_player(name: str) -> Dict[str, Any]:
    """
    Get data about players based on first, last, or full name.
    
    Args:
        name (str): The player's first, last, or full name to search for.
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of player objects matching the name query
        - total_found (int): Total number of players matching the search name
        - exact_match (Dict): Player data for the closest or most likely match
        - metadata (Dict): Additional context about the query
        
    Raises:
        ValueError: If name is empty or not a string
    """
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")
    
    # Call external API to get flattened data
    api_data = call_external_api("mlb-stats-server-lookup_player")
    
    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["results_0_id"],
            "first_name": api_data["results_0_first_name"],
            "last_name": api_data["results_0_last_name"],
            "team": api_data["results_0_team"],
            "position": api_data["results_0_position"],
            "career_start": api_data["results_0_career_start"],
            "career_end": api_data["results_0_career_end"]
        },
        {
            "id": api_data["results_1_id"],
            "first_name": api_data["results_1_first_name"],
            "last_name": api_data["results_1_last_name"],
            "team": api_data["results_1_team"],
            "position": api_data["results_1_position"],
            "career_start": api_data["results_1_career_start"],
            "career_end": api_data["results_1_career_end"]
        }
    ]
    
    # Construct exact match
    exact_match = {
        "id": api_data["exact_match_id"],
        "first_name": api_data["exact_match_first_name"],
        "last_name": api_data["exact_match_last_name"],
        "team": api_data["exact_match_team"],
        "position": api_data["exact_match_position"],
        "career_start": api_data["exact_match_career_start"],
        "career_end": api_data["exact_match_career_end"]
    }
    
    # Construct metadata
    metadata = {
        "processing_time": api_data["metadata_processing_time"],
        "source_version": api_data["metadata_source_version"],
        "warning": api_data["metadata_warning"]
    }
    
    # Return final structured response
    return {
        "results": results,
        "total_found": api_data["total_found"],
        "exact_match": exact_match,
        "metadata": metadata
    }