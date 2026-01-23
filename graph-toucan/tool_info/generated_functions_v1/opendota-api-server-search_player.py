from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching player
        - result_0_account_id (int): Account ID of the first matching player
        - result_0_similarity (float): Similarity score for the first player
        - result_1_name (str): Name of the second matching player
        - result_1_account_id (int): Account ID of the second matching player
        - result_1_similarity (float): Similarity score for the second player
        - query (str): The search query used to find players
    """
    return {
        "result_0_name": "AmazingPlayer",
        "result_0_account_id": 123456789,
        "result_0_similarity": 0.95,
        "result_1_name": "AwesomeGamer",
        "result_1_account_id": 987654321,
        "result_1_similarity": 0.87,
        "query": "Amazing"
    }

def opendota_api_server_search_player(query: str) -> Dict[str, Any]:
    """
    Search for players by name.
    
    Args:
        query (str): Name to search for
        
    Returns:
        Dict containing:
        - results (List[Dict]): list of matching players, each with 'name', 'account_id', and 'similarity' fields
        - query (str): the search query used to find players
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")
    
    api_data = call_external_api("opendota-api-server-search_player")
    
    # Construct results list from flattened API response
    results = [
        {
            "name": api_data["result_0_name"],
            "account_id": api_data["result_0_account_id"],
            "similarity": api_data["result_0_similarity"]
        },
        {
            "name": api_data["result_1_name"],
            "account_id": api_data["result_1_account_id"],
            "similarity": api_data["result_1_similarity"]
        }
    ]
    
    # Return structured response matching output schema
    return {
        "results": results,
        "query": query
    }