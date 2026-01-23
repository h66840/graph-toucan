from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB Stats Server meta information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - value_0 (str): First available value for the meta type
        - value_1 (str): Second available value for the meta type
        - description_0_value (str): Value corresponding to first description entry
        - description_0_description (str): Human-readable description for first value
        - description_0_notes (str): Additional notes for first value
        - description_1_value (str): Value corresponding to second description entry
        - description_1_description (str): Human-readable description for second value
        - description_1_notes (str): Additional notes for second value
        - meta_type (str): Type of metadata being returned
        - total_count (int): Total number of values returned
        - has_descriptions (bool): Whether descriptive metadata is available
    """
    return {
        "value_0": "homeRuns",
        "value_1": "strikeouts",
        "description_0_value": "homeRuns",
        "description_0_description": "Total home runs hit by player or team",
        "description_0_notes": "Includes regular season and postseason stats",
        "description_1_value": "strikeouts",
        "description_1_description": "Total strikeouts recorded",
        "description_1_notes": "Pitcher strikeouts only, regular season",
        "meta_type": "leagueLeaderTypes",
        "total_count": 2,
        "has_descriptions": True
    }

def mlb_stats_server_get_meta(type_name: str, fields: Optional[str] = None) -> Dict[str, Any]:
    """
    Get available values from StatsAPI for use in other queries, or look up descriptions
    for values found in API results.
    
    This function simulates calling an external API to retrieve metadata such as
    league leader types, stat types, or game statuses. It returns a structured response
    with values, optional descriptions, metadata type, count, and description availability.
    
    Args:
        type_name (str): The type of metadata to retrieve (e.g., 'leagueLeaderTypes', 'gameStatus')
        fields (Optional[str]): Optional filter for specific fields to return (not used in simulation)
    
    Returns:
        Dict containing:
        - values (List[str]): List of available string values for the given meta type
        - descriptions (List[Dict]): Optional list of key-value pairs mapping each value to its
          human-readable description or metadata; includes 'value', 'description', and 'notes' fields
        - meta_type (str): The type of metadata being returned
        - total_count (int): Total number of values returned
        - has_descriptions (bool): Indicates whether descriptive metadata is available
    
    Example:
        >>> mlb_stats_server_get_meta('leagueLeaderTypes')
        {
            'values': ['homeRuns', 'strikeouts'],
            'descriptions': [
                {'value': 'homeRuns', 'description': 'Total home runs hit by player or team', 'notes': 'Includes regular season and postseason stats'},
                {'value': 'strikeouts', 'description': 'Total strikeouts recorded', 'notes': 'Pitcher strikeouts only, regular season'}
            ],
            'meta_type': 'leagueLeaderTypes',
            'total_count': 2,
            'has_descriptions': True
        }
    """
    if not type_name:
        raise ValueError("type_name is required and cannot be empty")
    
    # Call simulated external API
    api_data = call_external_api("mlb-stats-server-get_meta")
    
    # Construct values list
    values = [
        api_data["value_0"],
        api_data["value_1"]
    ]
    
    # Construct descriptions list
    descriptions = [
        {
            "value": api_data["description_0_value"],
            "description": api_data["description_0_description"],
            "notes": api_data["description_0_notes"]
        },
        {
            "value": api_data["description_1_value"],
            "description": api_data["description_1_description"],
            "notes": api_data["description_1_notes"]
        }
    ]
    
    # Build final result structure
    result = {
        "values": values,
        "descriptions": descriptions,
        "meta_type": api_data["meta_type"],
        "total_count": api_data["total_count"],
        "has_descriptions": api_data["has_descriptions"]
    }
    
    return result