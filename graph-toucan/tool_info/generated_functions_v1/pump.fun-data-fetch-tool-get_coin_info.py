from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for pump.fun coin information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - name (str): The name of the coin
        - symbol (str): The symbol or ticker of the coin
        - mint_address (str): The mint ID (address) of the coin on the blockchain
        - creator (str): The wallet address of the coin's creator
        - created_at (str): Timestamp when the coin was created, in ISO 8601 format
        - supply (int): Total supply of the coin
        - current_price_sol (float): Current price of the coin in SOL (Solana)
        - current_price_usd (float): Current price of the coin in USD
        - market_cap_usd (float): Current market capitalization in USD
        - volume_24h (float): Trading volume in the last 24 hours (USD)
        - holders (int): Number of unique wallets holding the coin
        - total_trades (int): Total number of trades since launch
        - image_url (str): URL to the coin's logo or image
        - description (str): Description or about text for the coin project
        - website (str): Official website URL for the coin/project
        - twitter (str): Twitter/X handle or link for the project
        - telegram (str): Telegram group link or username
        - lp_locked_percent (float): Percentage of liquidity that is locked
        - burned_supply_percent (float): Percentage of the supply that has been burned
        - is_active (bool): Whether the coin is currently active and tradable
        - status_bonding_curve_active (bool): Whether bonding curve is active
        - status_tradeable (bool): Whether the coin is tradeable
        - status_locked_liquidity (bool): Whether liquidity is locked
    """
    return {
        "name": "Solana Monkey",
        "symbol": "SMK",
        "mint_address": "HJ38p3s9f2t7qW5nR6vK2mP1cX4zN9bV7eA5rT8yU7i",
        "creator": "G23kL9mN4pQ8rT6wX1zC7vB3nM5sK8jH2fD6gV9cX3z",
        "created_at": "2023-10-05T14:48:00Z",
        "supply": 1000000000,
        "current_price_sol": 0.00000123,
        "current_price_usd": 0.000456,
        "market_cap_usd": 456000.0,
        "volume_24h": 123456.78,
        "holders": 2543,
        "total_trades": 8765,
        "image_url": "https://example.com/images/smk.png",
        "description": "A fun and community-driven meme coin on Solana.",
        "website": "https://solamonkey.example.com",
        "twitter": "https://twitter.com/solamonkey",
        "telegram": "https://t.me/solamonkeygroup",
        "lp_locked_percent": 65.43,
        "burned_supply_percent": 12.5,
        "is_active": True,
        "status_bonding_curve_active": True,
        "status_tradeable": True,
        "status_locked_liquidity": True
    }

def pump_fun_data_fetch_tool_get_coin_info(mintId: str) -> Dict[str, Any]:
    """
    Get information about a coin from pump.fun using its mint ID.
    
    Args:
        mintId (str): The mint id of the coin (coin address)
    
    Returns:
        Dict containing detailed information about the coin including:
        - name (str): The name of the coin
        - symbol (str): The symbol or ticker of the coin
        - mint_address (str): The mint ID (address) of the coin on the blockchain
        - creator (str): The wallet address of the coin's creator
        - created_at (str): Timestamp when the coin was created, in ISO 8601 format
        - supply (int): Total supply of the coin
        - current_price_sol (float): Current price of the coin in SOL (Solana)
        - current_price_usd (float): Current price of the coin in USD
        - market_cap_usd (float): Current market capitalization in USD
        - volume_24h (float): Trading volume in the last 24 hours (USD)
        - holders (int): Number of unique wallets holding the coin
        - total_trades (int): Total number of trades since launch
        - image_url (str): URL to the coin's logo or image
        - description (str): Description or about text for the coin project
        - website (str): Official website URL for the coin/project
        - twitter (str): Twitter/X handle or link for the project
        - telegram (str): Telegram group link or username
        - lp_locked_percent (float): Percentage of liquidity that is locked
        - burned_supply_percent (float): Percentage of the supply that has been burned
        - is_active (bool): Whether the coin is currently active and tradable
        - status (Dict): Dictionary containing status flags like 'bonding_curve_active', 'tradeable', 'locked_liquidity'
    
    Raises:
        ValueError: If mintId is empty or invalid
    """
    if not mintId or not isinstance(mintId, str) or len(mintId.strip()) == 0:
        raise ValueError("mintId is required and must be a non-empty string")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("pump.fun-data-fetch-tool-get_coin_info")
    
    # Construct the nested status object from flat fields
    status = {
        "bonding_curve_active": api_data["status_bonding_curve_active"],
        "tradeable": api_data["status_tradeable"],
        "locked_liquidity": api_data["status_locked_liquidity"]
    }
    
    # Build final result matching the output schema
    result = {
        "name": api_data["name"],
        "symbol": api_data["symbol"],
        "mint_address": api_data["mint_address"],
        "creator": api_data["creator"],
        "created_at": api_data["created_at"],
        "supply": api_data["supply"],
        "current_price_sol": api_data["current_price_sol"],
        "current_price_usd": api_data["current_price_usd"],
        "market_cap_usd": api_data["market_cap_usd"],
        "volume_24h": api_data["volume_24h"],
        "holders": api_data["holders"],
        "total_trades": api_data["total_trades"],
        "image_url": api_data["image_url"],
        "description": api_data["description"],
        "website": api_data["website"],
        "twitter": api_data["twitter"],
        "telegram": api_data["telegram"],
        "lp_locked_percent": api_data["lp_locked_percent"],
        "burned_supply_percent": api_data["burned_supply_percent"],
        "is_active": api_data["is_active"],
        "status": status
    }
    
    return result