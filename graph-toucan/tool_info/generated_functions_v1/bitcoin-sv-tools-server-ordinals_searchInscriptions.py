from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bitcoin SV ordinal inscriptions search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_txid (str): Transaction ID of the first matching inscription
        - result_0_vout (int): Output index of the first inscription
        - result_0_outpoint (str): Outpoint (txid:vout) of the first inscription
        - result_0_satoshis (int): Number of satoshis in the first inscription
        - result_0_accSats (int): Accumulated sats offset for the first inscription
        - result_0_spend (str): Spend status of the first inscription
        - result_0_spend_height (int): Block height when first inscription was spent (or null as 0 if unspent)
        - result_0_spend_idx (int): Index of spend transaction for the first inscription
        - result_1_txid (str): Transaction ID of the second matching inscription
        - result_1_vout (int): Output index of the second inscription
        - result_1_outpoint (str): Outpoint (txid:vout) of the second inscription
        - result_1_satoshis (int): Number of satoshis in the second inscription
        - result_1_accSats (int): Accumulated sats offset for the second inscription
        - result_1_spend (str): Spend status of the second inscription
        - result_1_spend_height (int): Block height when second inscription was spent (or null as 0 if unspent)
        - result_1_spend_idx (int): Index of spend transaction for the second inscription
    """
    return {
        "result_0_txid": "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890",
        "result_0_vout": 0,
        "result_0_outpoint": "a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f67890:0",
        "result_0_satoshis": 546,
        "result_0_accSats": 123456789,
        "result_0_spend": "spent",
        "result_0_spend_height": 789000,
        "result_0_spend_idx": 1,
        "result_1_txid": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3",
        "result_1_vout": 1,
        "result_1_outpoint": "b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3:1",
        "result_1_satoshis": 1000,
        "result_1_accSats": 987654321,
        "result_1_spend": "unspent",
        "result_1_spend_height": 0,
        "result_1_spend_idx": -1,
    }

def bitcoin_sv_tools_server_ordinals_searchInscriptions(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Searches for Bitcoin SV ordinal inscriptions using flexible criteria.

    This function simulates querying an external service to find ordinal inscriptions
    based on provided search parameters such as address, content, MIME type, or MAP fields.
    It returns a list of matching inscription records with detailed metadata.

    Args:
        args (Dict[str, Any]): Search parameters including optional filters like:
            - address (str): Bitcoin address to filter inscriptions
            - content_type (str): MIME type to filter by (e.g., 'text/plain')
            - map_key (str): Key in the MAP protocol to search for
            - map_value (str): Value in the MAP protocol to match
            - limit (int): Maximum number of results to return

    Returns:
        Dict[str, Any]: A dictionary containing:
            - results (List[Dict]): List of inscription records with fields:
                - txid (str)
                - vout (int)
                - outpoint (str)
                - satoshis (int)
                - accSats (int)
                - spend (str)
                - spend_height (Optional[int])
                - spend_idx (int)
    """
    # Validate input
    if not isinstance(args, dict):
        raise ValueError("args must be a dictionary")

    # Call simulated external API
    api_data = call_external_api("bitcoin-sv-tools-server-ordinals_searchInscriptions")

    # Construct results list from flattened API response
    results: List[Dict[str, Any]] = []

    # Process first result
    if "result_0_txid" in api_data:
        spend_height_0 = api_data["result_0_spend_height"] if api_data["result_0_spend_height"] > 0 else None
        results.append({
            "txid": api_data["result_0_txid"],
            "vout": api_data["result_0_vout"],
            "outpoint": api_data["result_0_outpoint"],
            "satoshis": api_data["result_0_satoshis"],
            "accSats": api_data["result_0_accSats"],
            "spend": api_data["result_0_spend"],
            "spend_height": spend_height_0,
            "spend_idx": api_data["result_0_spend_idx"]
        })

    # Process second result
    if "result_1_txid" in api_data:
        spend_height_1 = api_data["result_1_spend_height"] if api_data["result_1_spend_height"] > 0 else None
        results.append({
            "txid": api_data["result_1_txid"],
            "vout": api_data["result_1_vout"],
            "outpoint": api_data["result_1_outpoint"],
            "satoshis": api_data["result_1_satoshis"],
            "accSats": api_data["result_1_accSats"],
            "spend": api_data["result_1_spend"],
            "spend_height": spend_height_1,
            "spend_idx": api_data["result_1_spend_idx"]
        })

    # Apply limit if specified
    limit = args.get("limit")
    if isinstance(limit, int) and limit > 0:
        results = results[:limit]

    return {"results": results}