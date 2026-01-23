from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CoinGecko coins list.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - coin_0_id (str): First coin's unique identifier
        - coin_0_name (str): First coin's name
        - coin_0_symbol (str): First coin's symbol
        - coin_0_platform_contract_address (str): First coin's contract address if include_platform=true
        - coin_1_id (str): Second coin's unique identifier
        - coin_1_name (str): Second coin's name
        - coin_1_symbol (str): Second coin's symbol
        - coin_1_platform_contract_address (str): Second coin's contract address if include_platform=true
    """
    return {
        "coin_0_id": "bitcoin",
        "coin_0_name": "Bitcoin",
        "coin_0_symbol": "btc",
        "coin_0_platform_contract_address": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
        "coin_1_id": "ethereum",
        "coin_1_name": "Ethereum",
        "coin_1_symbol": "eth",
        "coin_1_platform_contract_address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
    }

def coingecko_api_server_API_coins_list(include_platform: Optional[bool] = False) -> Dict[str, Any]:
    """
    Fetches the list of all supported coins from CoinGecko API with optional platform contract addresses.

    Args:
        include_platform (bool, optional): Whether to include platform and token contract addresses. Defaults to False.

    Returns:
        Dict containing a list of coin objects with id, name, symbol, and optionally platform contract addresses.
        - coins (List[Dict]): List of coin dictionaries with keys 'id', 'name', 'symbol', 
          and 'platform_contract_address' if include_platform is True.

    Example:
        {
            "coins": [
                {
                    "id": "bitcoin",
                    "name": "Bitcoin",
                    "symbol": "btc"
                },
                {
                    "id": "ethereum",
                    "name": "Ethereum",
                    "symbol": "eth"
                }
            ]
        }
    """
    try:
        # Validate input
        if include_platform is None:
            include_platform = False
        if not isinstance(include_platform, bool):
            raise ValueError("include_platform must be a boolean value")

        # Fetch simulated external API data
        api_data = call_external_api("coingecko-api-server-API-coins-list")

        # Construct the coins list from flattened API response
        coins = []
        
        # Process first coin
        coin_0 = {
            "id": api_data["coin_0_id"],
            "name": api_data["coin_0_name"],
            "symbol": api_data["coin_0_symbol"]
        }
        # Add platform contract address only if requested
        if include_platform:
            coin_0["platform_contract_address"] = api_data["coin_0_platform_contract_address"]
        coins.append(coin_0)

        # Process second coin
        coin_1 = {
            "id": api_data["coin_1_id"],
            "name": api_data["coin_1_name"],
            "symbol": api_data["coin_1_symbol"]
        }
        # Add platform contract address only if requested
        if include_platform:
            coin_1["platform_contract_address"] = api_data["coin_1_platform_contract_address"]
        coins.append(coin_1)

        return {"coins": coins}

    except Exception as e:
        # Handle unexpected errors
        return {"coins": [], "error": str(e)}