from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for autocomplete definitions.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success_v (int): API version number indicating the response format version
        - success_license (str): license type under which the data is provided (e.g., "CC-BY 4.0")
        - success_data_intervals_0_id (int): unique identifier for the first interval
        - success_data_intervals_0_name (str): name of the first geological interval
        - success_data_intervals_0_category (str): category type of the first entry (e.g., "interval")
        - success_data_intervals_1_id (int): unique identifier for the second interval
        - success_data_intervals_1_name (str): name of the second geological interval
        - success_data_intervals_1_category (str): category type of the second entry (e.g., "interval")
    """
    return {
        "success_v": 1,
        "success_license": "CC-BY 4.0",
        "success_data_intervals_0_id": 101,
        "success_data_intervals_0_name": "Cambrian",
        "success_data_intervals_0_category": "interval",
        "success_data_intervals_1_id": 102,
        "success_data_intervals_1_name": "Ordovician",
        "success_data_intervals_1_category": "interval",
    }

def macrostrat_api_server_defs_autocomplete(query: str) -> Dict[str, Any]:
    """
    Quickly retrieve all definitions matching a query. Limited to 100 results.

    Args:
        query (str): The search term to match against geological definitions.

    Returns:
        Dict containing the following structure:
        - success (Dict):
          - v (int): API version number
          - license (str): License type (e.g., "CC-BY 4.0")
          - data (Dict):
            - intervals (List[Dict]): List of matching geological intervals with:
              - id (int): Unique identifier
              - name (str): Name of the interval
              - category (str): Category type (e.g., "interval")
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")

    api_data = call_external_api("macrostrat-api-server-defs-autocomplete")

    intervals = [
        {
            "id": api_data["success_data_intervals_0_id"],
            "name": api_data["success_data_intervals_0_name"],
            "category": api_data["success_data_intervals_0_category"],
        },
        {
            "id": api_data["success_data_intervals_1_id"],
            "name": api_data["success_data_intervals_1_name"],
            "category": api_data["success_data_intervals_1_category"],
        },
    ]

    result = {
        "success": {
            "v": api_data["success_v"],
            "license": api_data["success_license"],
            "data": {
                "intervals": intervals
            }
        }
    }

    return result