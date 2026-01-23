from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - id (str): unique identifier for the cryptocurrency
        - symbol (str): symbol of the cryptocurrency
        - name (str): full name of the cryptocurrency
        - description (str): detailed description of the cryptocurrency
        - image_thumb (str): URL for thumbnail image
        - image_small (str): URL for small image
        - image_large (str): URL for large image
        - market_data_current_price_usd (float): current price in USD
        - market_data_current_price_eur (float): current price in EUR
        - market_data_market_cap_usd (float): market cap in USD
        - market_data_market_cap_eur (float): market cap in EUR
        - market_data_total_volume_usd (float): total volume in USD
        - market_data_total_volume_eur (float): total volume in EUR
        - market_data_high_24h_usd (float): 24h high in USD
        - market_data_high_24h_eur (float): 24h high in EUR
        - market_data_low_24h_usd (float): 24h low in USD
        - market_data_low_24h_eur (float): 24h low in EUR
        - market_data_price_change_percentage_24h (float): price change % in 24h
        - market_data_price_change_percentage_7d (float): price change % in 7d
        - market_data_price_change_percentage_30d (float): price change % in 30d
        - last_updated (str): timestamp when data was last updated (ISO 8601)
    """
    return {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "description": "Bitcoin is a decentralized digital currency that enables instant payments to anyone, anywhere in the world.",
        "image_thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png",
        "image_small": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png",
        "image_large": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        "market_data_current_price_usd": 43250.5,
        "market_data_current_price_eur": 39876.2,
        "market_data_market_cap_usd": 852345678901.23,
        "market_data_market_cap_eur": 787654321098.76,
        "market_data_total_volume_usd": 23456789012.34,
        "market_data_total_volume_eur": 21654321987.65,
        "market_data_high_24h_usd": 44100.0,
        "market_data_high_24h_eur": 40700.0,
        "market_data_low_24h_usd": 42800.0,
        "market_data_low_24h_eur": 39400.0,
        "market_data_price_change_percentage_24h": 2.45,
        "market_data_price_change_percentage_7d": -3.21,
        "market_data_price_change_percentage_30d": 8.76,
        "last_updated": "2023-10-15T12:34:56Z"
    }

def coingecko_mcp_server_coingecko_coin_data(
    id: str, 
    vs_currencies: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Get current data for a coin (price, market, volume, etc.).
    
    Args:
        id (str): Coin ID (e.g., bitcoin, ethereum)
        vs_currencies (Optional[List[str]]): List of currencies to get price data in (e.g., usd, eur, etc.)
    
    Returns:
        Dict containing cryptocurrency data with the following structure:
        - id (str): unique identifier for the cryptocurrency
        - symbol (str): symbol of the cryptocurrency
        - name (str): full name of the cryptocurrency
        - description (str): detailed description of the cryptocurrency
        - image (Dict): contains URLs for thumbnail, small, and large images
        - market_data (Dict): contains current market statistics including price, market cap, volume, etc.
        - last_updated (str): timestamp indicating when the data was last updated (ISO 8601)
    
    Raises:
        ValueError: If id is empty or None
    """
    if not id:
        raise ValueError("Coin ID is required")
    
    # Default vs_currencies if not provided
    if vs_currencies is None:
        vs_currencies = ["usd"]
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("coingecko-mcp-server-coingecko_coin_data")
    
    # Construct image dictionary
    image = {
        "thumb": api_data["image_thumb"],
        "small": api_data["image_small"],
        "large": api_data["image_large"]
    }
    
    # Construct market_data dictionary with only requested currencies
    market_data = {
        "current_price": {},
        "market_cap": {},
        "total_volume": {},
        "high_24h": {},
        "low_24h": {}
    }
    
    # Add price data for requested currencies
    for currency in vs_currencies:
        currency_upper = currency.lower()
        usd_key = f"market_data_current_price_{currency_upper}"
        if usd_key in api_data:
            market_data["current_price"][currency] = api_data[usd_key]
        
        market_cap_key = f"market_data_market_cap_{currency_upper}"
        if market_cap_key in api_data:
            market_data["market_cap"][currency] = api_data[market_cap_key]
        
        volume_key = f"market_data_total_volume_{currency_upper}"
        if volume_key in api_data:
            market_data["total_volume"][currency] = api_data[volume_key]
        
        high_key = f"market_data_high_24h_{currency_upper}"
        if high_key in api_data:
            market_data["high_24h"][currency] = api_data[high_key]
        
        low_key = f"market_data_low_24h_{currency_upper}"
        if low_key in api_data:
            market_data["low_24h"][currency] = api_data[low_key]
    
    # Add percentage change data (currency-agnostic)
    market_data["price_change_percentage_24h"] = api_data["market_data_price_change_percentage_24h"]
    market_data["price_change_percentage_7d"] = api_data["market_data_price_change_percentage_7d"]
    market_data["price_change_percentage_30d"] = api_data["market_data_price_change_percentage_30d"]
    
    # Construct final result
    result = {
        "id": api_data["id"],
        "symbol": api_data["symbol"],
        "name": api_data["name"],
        "description": api_data["description"],
        "image": image,
        "market_data": market_data,
        "last_updated": api_data["last_updated"]
    }
    
    return result