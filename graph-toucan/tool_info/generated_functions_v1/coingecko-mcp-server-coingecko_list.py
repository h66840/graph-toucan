from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CoinGecko coin list.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - coin_0_id (str): First coin's ID
        - coin_0_name (str): First coin's name
        - coin_0_symbol (str): First coin's symbol
        - coin_0_platforms_chain (str): First coin's platform chain (if include_platform=True)
        - coin_0_platforms_address (str): First coin's contract address (if include_platform=True)
        - coin_1_id (str): Second coin's ID
        - coin_1_name (str): Second coin's name
        - coin_1_symbol (str): Second coin's symbol
        - coin_1_platforms_chain (str): Second coin's platform chain (if include_platform=True)
        - coin_1_platforms_address (str): Second coin's contract address (if include_platform=True)
        - total_count (int): Total number of coins returned
    """
    return {
        "coin_0_id": "bitcoin",
        "coin_0_name": "Bitcoin",
        "coin_0_symbol": "btc",
        "coin_0_platforms_chain": "ethereum",
        "coin_0_platforms_address": "0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c",
        "coin_1_id": "ethereum",
        "coin_1_name": "Ethereum",
        "coin_1_symbol": "eth",
        "coin_1_platforms_chain": "binance-smart-chain",
        "coin_1_platforms_address": "0x2170ed0880ac9a755fd29b2688956bd959f933f8",
        "total_count": 2
    }

def coingecko_mcp_server_coingecko_list(include_platform: Optional[bool] = False) -> Dict[str, Any]:
    """
    Get list of all supported coins with ids, names, and symbols.

    Args:
        include_platform (bool, optional): Include platform contract addresses (e.g., for tokens on Ethereum).
            Defaults to False.

    Returns:
        Dict containing:
        - coins (List[Dict]): List of coin objects, each containing 'id', 'name', and 'symbol' as strings.
          If include_platform was True, may also include 'platforms' field with contract address mappings.
        - total_count (int): Total number of coins returned in the list.
    """
    # Validate input
    if include_platform is None:
        include_platform = False
    if not isinstance(include_platform, bool):
        raise ValueError("include_platform must be a boolean value")

    # Fetch simulated external data
    api_data = call_external_api("coingecko-mcp-server-coingecko_list")

    # Construct coins list
    coins = []
    
    # Process first coin
    coin_0 = {
        "id": api_data["coin_0_id"],
        "name": api_data["coin_0_name"],
        "symbol": api_data["coin_0_symbol"].upper()
    }
    if include_platform:
        coin_0["platforms"] = {
            api_data["coin_0_platforms_chain"]: api_data["coin_0_platforms_address"]
        }
    coins.append(coin_0)

    # Process second coin
    coin_1 = {
        "id": api_data["coin_1_id"],
        "name": api_data["coin_1_name"],
        "symbol": api_data["coin_1_symbol"].upper()
    }
    if include_platform:
        coin_1["platforms"] = {
            api_data["coin_1_platforms_chain"]: api_data["coin_1_platforms_address"]
        }
    coins.append(coin_1)

    # Construct result
    result = {
        "coins": coins,
        "total_count": api_data["total_count"]
    }

    return result