from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - name (str): Name of the cryptocurrency
        - symbol (str): Symbol or ticker of the cryptocurrency
        - rank (int): Current market ranking
        - hashing_algorithm (str): Hashing algorithm used by the blockchain
        - price_cny (float): Current price in Chinese Yuan
        - price_usd (float): Current price in US Dollar
        - price_change_24h (float): 24-hour price change percentage
        - market_cap_cny (float): Market capitalization in CNY
        - volume_24h_cny (float): 24-hour trading volume in CNY
        - circulating_supply (float): Number of coins in circulation
        - total_supply (float): Total number of coins that exist
        - ath_cny (float): All-time high price in CNY
        - ath_date (str): Date when all-time high was reached (YYYY-MM-DD)
        - distance_from_ath_percent (float): Percentage difference from current price to ATH
        - links_website (str): Official website URL
        - links_blockchain_explorer (str): Blockchain explorer URL
        - links_forum (str): Forum URL
        - links_reddit (str): Reddit community URL
        - links_github (str): GitHub repository URL
    """
    return {
        "name": "Bitcoin",
        "symbol": "BTC",
        "rank": 1,
        "hashing_algorithm": "SHA-256",
        "price_cny": 285000.0,
        "price_usd": 40000.0,
        "price_change_24h": -2.5,
        "market_cap_cny": 5600000000000.0,
        "volume_24h_cny": 120000000000.0,
        "circulating_supply": 19650000.0,
        "total_supply": 21000000.0,
        "ath_cny": 340000.0,
        "ath_date": "2021-11-10",
        "distance_from_ath_percent": -16.18,
        "links_website": "https://bitcoin.org",
        "links_blockchain_explorer": "https://blockchain.com/explorer",
        "links_forum": "https://bitcointalk.org",
        "links_reddit": "https://www.reddit.com/r/Bitcoin/",
        "links_github": "https://github.com/bitcoin"
    }

def 虚拟币价格查询服务_get_coin_detail(coin_id: str) -> Dict[str, Any]:
    """
    获取虚拟币的详细信息
    
    Args:
        coin_id (str): 虚拟币的ID (例如 bitcoin, ethereum)
    
    Returns:
        Dict containing detailed cryptocurrency information with the following structure:
        - name (str): name of the cryptocurrency
        - symbol (str): symbol or ticker of the cryptocurrency
        - rank (int): current market ranking of the coin
        - hashing_algorithm (str): the hashing algorithm used by the blockchain (if available)
        - price_cny (float): current price in Chinese Yuan (CNY)
        - price_usd (float): current price in US Dollar (USD)
        - price_change_24h (float): percentage change in price over the last 24 hours
        - market_cap_cny (float): total market capitalization in CNY
        - volume_24h_cny (float): trading volume over the last 24 hours in CNY
        - circulating_supply (float): number of coins currently in circulation
        - total_supply (float): total number of coins that exist
        - ath_cny (float): all-time high price in CNY
        - ath_date (str): date when the all-time high was reached, in YYYY-MM-DD format
        - distance_from_ath_percent (float): percentage difference from current price to all-time high
        - links (Dict): contains URLs related to the coin with keys:
            'website', 'blockchain_explorer', 'forum', 'reddit', 'github'
    
    Raises:
        ValueError: If coin_id is empty or not a string
    """
    if not coin_id:
        raise ValueError("coin_id is required")
    if not isinstance(coin_id, str):
        raise ValueError("coin_id must be a string")
    
    # Call external API to get data
    api_data = call_external_api("虚拟币价格查询服务_get_coin_detail")
    
    # Construct the nested structure as per output schema
    result = {
        "name": api_data["name"],
        "symbol": api_data["symbol"],
        "rank": api_data["rank"],
        "hashing_algorithm": api_data["hashing_algorithm"],
        "price_cny": api_data["price_cny"],
        "price_usd": api_data["price_usd"],
        "price_change_24h": api_data["price_change_24h"],
        "market_cap_cny": api_data["market_cap_cny"],
        "volume_24h_cny": api_data["volume_24h_cny"],
        "circulating_supply": api_data["circulating_supply"],
        "total_supply": api_data["total_supply"],
        "ath_cny": api_data["ath_cny"],
        "ath_date": api_data["ath_date"],
        "distance_from_ath_percent": api_data["distance_from_ath_percent"],
        "links": {
            "website": api_data["links_website"],
            "blockchain_explorer": api_data["links_blockchain_explorer"],
            "forum": api_data["links_forum"],
            "reddit": api_data["links_reddit"],
            "github": api_data["links_github"]
        }
    }
    
    return result