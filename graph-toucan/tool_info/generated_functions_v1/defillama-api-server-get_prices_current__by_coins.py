from typing import Dict, Any, Optional
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for current token prices.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Indicates whether the price retrieval was successful
        - error (str): Error message if the request failed, otherwise null/None
        - timestamp (int): Unix timestamp indicating when the prices were fetched
        - price_0_price (float): Price of the first token in USD
        - price_0_symbol (str): Symbol of the first token (e.g., "WETH")
        - price_0_confidence (float): Confidence score for the first token's price (0.0 to 1.0)
        - price_0_timestamp (int): Unix timestamp of the latest price observation for the first token
        - price_0_chainId (str): Blockchain identifier for the first token (e.g., "ethereum")
        - price_0_decimals (int): Number of decimal places for the first token
        - price_1_price (float): Price of the second token in USD
        - price_1_symbol (str): Symbol of the second token (e.g., "USDC")
        - price_1_confidence (float): Confidence score for the second token's price (0.0 to 1.0)
        - price_1_timestamp (int): Unix timestamp of the latest price observation for the second token
        - price_1_chainId (str): Blockchain identifier for the second token (e.g., "polygon")
        - price_1_decimals (int): Number of decimal places for the second token
    """
    return {
        "success": True,
        "error": None,
        "timestamp": int(time.time()),
        "price_0_price": 2500.5,
        "price_0_symbol": "WETH",
        "price_0_confidence": 0.98,
        "price_0_timestamp": int(time.time()) - 300,
        "price_0_chainId": "ethereum",
        "price_0_decimals": 18,
        "price_1_price": 0.999,
        "price_1_symbol": "USDC",
        "price_1_confidence": 0.99,
        "price_1_timestamp": int(time.time()) - 120,
        "price_1_chainId": "polygon",
        "price_1_decimals": 6,
    }


def defillama_api_server_get_prices_current_by_coins(
    coins: str, searchWidth: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get current prices of tokens by contract address.

    This function simulates querying an external API to retrieve current market prices
    for a set of tokens specified as {chain}:{address}. It returns price data including
    value, symbol, confidence, timestamp, chain ID, and decimals.

    Args:
        coins (str): Comma-separated list of tokens in the format "{chain}:{address}".
                     Example: "ethereum:0x...,polygon:0x..."
        searchWidth (Optional[str]): Time range (in hours) on either side to find price data.
                                     Defaults to "6" hours if not provided.

    Returns:
        Dict containing:
        - prices (Dict): Mapping of token keys to their price data (price, symbol, confidence,
                         timestamp, chainId, decimals)
        - error (Optional[str]): Error message if request failed, else None
        - success (bool): Whether the operation was successful
        - timestamp (int): Unix timestamp when prices were fetched

    Example:
        >>> defillama_api_server_get_prices_current__by_coins("ethereum:0x...,polygon:0x...")
        {
            "prices": {
                "ethereum:0x...": {
                    "price": 2500.5,
                    "symbol": "WETH",
                    "confidence": 0.98,
                    "timestamp": 1717000000,
                    "chainId": "ethereum",
                    "decimals": 18
                },
                "polygon:0x...": {
                    "price": 0.999,
                    "symbol": "USDC",
                    "confidence": 0.99,
                    "timestamp": 1717000180,
                    "chainId": "polygon",
                    "decimals": 6
                }
            },
            "error": None,
            "success": True,
            "timestamp": 1717000300
        }
    """
    # Input validation
    if not coins or not coins.strip():
        return {
            "prices": {},
            "error": "Parameter 'coins' is required and cannot be empty",
            "success": False,
            "timestamp": int(time.time()),
        }

    # Simulate API call
    api_data = call_external_api("defillama-api-server-get_prices_current__by_coins")

    # Construct the nested output structure
    prices = {}

    # Split coins string to get individual tokens
    coin_list = [coin.strip() for coin in coins.split(",") if coin.strip()]

    # Use two mock tokens if available
    for i, coin_key in enumerate(coin_list[:2]):  # Limit to 2 for simulation
        price_key = f"price_{i}_price"
        if price_key not in api_data:
            continue

        prices[coin_key] = {
            "price": api_data[f"price_{i}_price"],
            "symbol": api_data[f"price_{i}_symbol"],
            "confidence": api_data[f"price_{i}_confidence"],
            "timestamp": api_data[f"price_{i}_timestamp"],
            "chainId": api_data[f"price_{i}_chainId"],
            "decimals": api_data[f"price_{i}_decimals"],
        }

    # Return final structured response
    return {
        "prices": prices,
        "error": api_data["error"],
        "success": api_data["success"],
        "timestamp": api_data["timestamp"],
    }