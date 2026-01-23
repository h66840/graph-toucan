from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB player ID lookup.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_0_name_last (str): Last name of first player
        - data_0_name_first (str): First name of first player
        - data_0_key_mlbam (int): MLB AM key of first player
        - data_0_key_retro (str): Retrosheet key of first player
        - data_0_key_bbref (str): Baseball Reference key of first player
        - data_0_key_fangraphs (int): FanGraphs key of first player
        - data_0_mlb_played_first (int): First MLB year of first player
        - data_0_mlb_played_last (int): Last MLB year of first player
        - data_1_name_last (str): Last name of second player
        - data_1_name_first (str): First name of second player
        - data_1_key_mlbam (int): MLB AM key of second player
        - data_1_key_retro (str): Retrosheet key of second player
        - data_1_key_bbref (str): Baseball Reference key of second player
        - data_1_key_fangraphs (int): FanGraphs key of second player
        - data_1_mlb_played_first (int): First MLB year of second player
        - data_1_mlb_played_last (int): Last MLB year of second player
        - count (int): Total number of player records returned
        - columns_0 (str): First column name in data records
        - columns_1 (str): Second column name in data records
        - columns_2 (str): Third column name in data records
        - columns_3 (str): Fourth column name in data records
        - columns_4 (str): Fifth column name in data records
        - columns_5 (str): Sixth column name in data records
        - columns_6 (str): Seventh column name in data records
        - columns_7 (str): Eighth column name in data records
    """
    return {
        "data_0_name_last": "Smith",
        "data_0_name_first": "John",
        "data_0_key_mlbam": 666666,
        "data_0_key_retro": "smitj001",
        "data_0_key_bbref": "smithjo01",
        "data_0_key_fangraphs": 12345,
        "data_0_mlb_played_first": 2010,
        "data_0_mlb_played_last": 2020,
        "data_1_name_last": "Smith",
        "data_1_name_first": "James",
        "data_1_key_mlbam": 777777,
        "data_1_key_retro": "smitj002",
        "data_1_key_bbref": "smithja01",
        "data_1_key_fangraphs": 12346,
        "data_1_mlb_played_first": 2015,
        "data_1_mlb_played_last": 2021,
        "count": 2,
        "columns_0": "name_last",
        "columns_1": "name_first",
        "columns_2": "key_mlbam",
        "columns_3": "key_retro",
        "columns_4": "key_bbref",
        "columns_5": "key_fangraphs",
        "columns_6": "mlb_played_first",
        "columns_7": "mlb_played_last"
    }

def mlb_stats_server_get_playerid_lookup(last: str, first: Optional[str] = None, fuzzy: bool = False) -> Dict[str, Any]:
    """
    Lookup playerIDs (MLB AM, bbref, retrosheet, FG) for a given player.
    
    Args:
        last (str): Player's last name (required).
        first (str, optional): Player's first name. Defaults to None.
        fuzzy (bool, optional): If True, returns players with names close to input in case of typos.
            Defaults to False.
    
    Returns:
        Dict containing:
            - data (List[Dict]): List of player records with fields:
                'name_last', 'name_first', 'key_mlbam', 'key_retro', 'key_bbref',
                'key_fangraphs', 'mlb_played_first', 'mlb_played_last'
            - count (int): Total number of player records returned
            - columns (List[str]): List of column names present in the data records
    
    Raises:
        ValueError: If last name is not provided
    """
    if not last or not isinstance(last, str):
        raise ValueError("Last name must be a non-empty string")
    
    if first is not None and not isinstance(first, str):
        raise ValueError("First name must be a string if provided")
    
    if not isinstance(fuzzy, bool):
        raise ValueError("Fuzzy parameter must be a boolean")
    
    # Call external API to get flattened data
    api_data = call_external_api("mlb-stats-server-get_playerid_lookup")
    
    # Construct the data list from indexed fields
    data = [
        {
            "name_last": api_data["data_0_name_last"],
            "name_first": api_data["data_0_name_first"],
            "key_mlbam": api_data["data_0_key_mlbam"],
            "key_retro": api_data["data_0_key_retro"],
            "key_bbref": api_data["data_0_key_bbref"],
            "key_fangraphs": api_data["data_0_key_fangraphs"],
            "mlb_played_first": api_data["data_0_mlb_played_first"],
            "mlb_played_last": api_data["data_0_mlb_played_last"]
        },
        {
            "name_last": api_data["data_1_name_last"],
            "name_first": api_data["data_1_name_first"],
            "key_mlbam": api_data["data_1_key_mlbam"],
            "key_retro": api_data["data_1_key_retro"],
            "key_bbref": api_data["data_1_key_bbref"],
            "key_fangraphs": api_data["data_1_key_fangraphs"],
            "mlb_played_first": api_data["data_1_mlb_played_first"],
            "mlb_played_last": api_data["data_1_mlb_played_last"]
        }
    ]
    
    # Construct columns list from indexed fields
    columns = [
        api_data["columns_0"],
        api_data["columns_1"],
        api_data["columns_2"],
        api_data["columns_3"],
        api_data["columns_4"],
        api_data["columns_5"],
        api_data["columns_6"],
        api_data["columns_7"]
    ]
    
    # Return the structured result
    return {
        "data": data,
        "count": api_data["count"],
        "columns": columns
    }