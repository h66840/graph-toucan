from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for geologic time intervals.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_0_int_id (int): Interval ID of the first geologic time interval
        - data_0_name (str): Name of the first interval
        - data_0_abbrev (str): Abbreviation of the first interval
        - data_0_t_age (float): Top age in million years of the first interval
        - data_0_b_age (float): Base age in million years of the first interval
        - data_0_int_type (str): Type of the first interval (e.g., period, epoch)
        - data_0_timescale_0_timescale_id (int): First timescale ID for the first interval
        - data_0_timescale_0_name (str): First timescale name for the first interval
        - data_0_timescale_1_timescale_id (int): Second timescale ID for the first interval
        - data_0_timescale_1_name (str): Second timescale name for the first interval
        - data_0_color (str): Hex color code for the first interval
        - data_1_int_id (int): Interval ID of the second geologic time interval
        - data_1_name (str): Name of the second interval
        - data_1_abbrev (str): Abbreviation of the second interval
        - data_1_t_age (float): Top age in million years of the second interval
        - data_1_b_age (float): Base age in million years of the second interval
        - data_1_int_type (str): Type of the second interval (e.g., period, epoch)
        - data_1_timescale_0_timescale_id (int): First timescale ID for the second interval
        - data_1_timescale_0_name (str): First timescale name for the second interval
        - data_1_timescale_1_timescale_id (int): Second timescale ID for the second interval
        - data_1_timescale_1_name (str): Second timescale name for the second interval
        - data_1_color (str): Hex color code for the second interval
        - license (str): License identifier for the data
        - version (int): Version of the API response format
    """
    return {
        "data_0_int_id": 1001,
        "data_0_name": "Cretaceous",
        "data_0_abbrev": "K",
        "data_0_t_age": 145.0,
        "data_0_b_age": 66.0,
        "data_0_int_type": "period",
        "data_0_timescale_0_timescale_id": 1,
        "data_0_timescale_0_name": "ICS",
        "data_0_timescale_1_timescale_id": 2,
        "data_0_timescale_1_name": "GTS2020",
        "data_0_color": "#FF5733",
        "data_1_int_id": 1002,
        "data_1_name": "Jurassic",
        "data_1_abbrev": "J",
        "data_1_t_age": 201.3,
        "data_1_b_age": 145.0,
        "data_1_int_type": "period",
        "data_1_timescale_0_timescale_id": 1,
        "data_1_timescale_0_name": "ICS",
        "data_1_timescale_1_timescale_id": 2,
        "data_1_timescale_1_name": "GTS2020",
        "data_1_color": "#33A8FF",
        "license": "CC-BY 4.0",
        "version": 1
    }

def macrostrat_api_server_timescale(age: Optional[float] = None) -> Dict[str, Any]:
    """
    Get information about a time period from the Macrostrat API timescale service.

    Args:
        age (Optional[float]): The age in million years to filter or query for relevant intervals.
                               If None, returns default time intervals.

    Returns:
        Dict containing:
        - data (List[Dict]): List of geologic time intervals with keys:
            'int_id', 'name', 'abbrev', 't_age', 'b_age', 'int_type',
            'timescales' (list of dicts with 'timescale_id' and 'name'), 'color'
        - license (str): License identifier for the data
        - version (int): Version of the API response format

    Example:
        >>> result = macrostrat_api_server_timescale(age=100.0)
        >>> print(result['data'][0]['name'])
        Cretaceous
    """
    # Fetch simulated external data
    api_data = call_external_api("macrostrat-api-server-timescale")

    # Construct the first interval
    interval_0_timescales = [
        {
            "timescale_id": api_data["data_0_timescale_0_timescale_id"],
            "name": api_data["data_0_timescale_0_name"]
        },
        {
            "timescale_id": api_data["data_0_timescale_1_timescale_id"],
            "name": api_data["data_0_timescale_1_name"]
        }
    ]

    interval_0 = {
        "int_id": api_data["data_0_int_id"],
        "name": api_data["data_0_name"],
        "abbrev": api_data["data_0_abbrev"],
        "t_age": api_data["data_0_t_age"],
        "b_age": api_data["data_0_b_age"],
        "int_type": api_data["data_0_int_type"],
        "timescales": interval_0_timescales,
        "color": api_data["data_0_color"]
    }

    # Construct the second interval
    interval_1_timescales = [
        {
            "timescale_id": api_data["data_1_timescale_0_timescale_id"],
            "name": api_data["data_1_timescale_0_name"]
        },
        {
            "timescale_id": api_data["data_1_timescale_1_timescale_id"],
            "name": api_data["data_1_timescale_1_name"]
        }
    ]

    interval_1 = {
        "int_id": api_data["data_1_int_id"],
        "name": api_data["data_1_name"],
        "abbrev": api_data["data_1_abbrev"],
        "t_age": api_data["data_1_t_age"],
        "b_age": api_data["data_1_b_age"],
        "int_type": api_data["data_1_int_type"],
        "timescales": interval_1_timescales,
        "color": api_data["data_1_color"]
    }

    # Filter intervals based on age if provided
    data = [interval_0, interval_1]
    if age is not None:
        data = [interval for interval in data if interval["t_age"] >= age >= interval["b_age"]]

    # Construct final result
    result = {
        "data": data,
        "license": api_data["license"],
        "version": api_data["version"]
    }

    return result