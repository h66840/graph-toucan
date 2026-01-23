from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency market data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - coin_0_id (str): First coin's ID
        - coin_0_symbol (str): First coin's symbol
        - coin_0_name (str): First coin's name
        - coin_0_image (str): First coin's image URL
        - coin_0_current_price (float): First coin's current price
        - coin_0_market_cap (float): First coin's market cap
        - coin_0_market_cap_rank (int): First coin's market cap rank
        - coin_0_total_volume (float): First coin's total volume
        - coin_0_high_24h (float): First coin's 24h high price
        - coin_0_low_24h (float): First coin's 24h low price
        - coin_0_price_change_24h (float): First coin's 24h price change
        - coin_0_price_change_percentage_24h (float): First coin's 24h price change percentage
        - coin_0_market_cap_change_24h (float): First coin's 24h market cap change
        - coin_0_market_cap_change_percentage_24h (float): First coin's 24h market cap change percentage
        - coin_0_circulating_supply (float): First coin's circulating supply
        - coin_0_total_supply (float): First coin's total supply
        - coin_0_max_supply (float): First coin's max supply
        - coin_0_ath (float): First coin's all-time high price
        - coin_0_ath_change_percentage (float): First coin's ATH change percentage
        - coin_0_ath_date (str): First coin's ATH date
        - coin_0_atl (float): First coin's all-time low price
        - coin_0_atl_change_percentage (float): First coin's ATL change percentage
        - coin_0_atl_date (str): First coin's ATL date
        - coin_0_last_updated (str): First coin's last updated timestamp
        - coin_1_id (str): Second coin's ID
        - coin_1_symbol (str): Second coin's symbol
        - coin_1_name (str): Second coin's name
        - coin_1_image (str): Second coin's image URL
        - coin_1_current_price (float): Second coin's current price
        - coin_1_market_cap (float): Second coin's market cap
        - coin_1_market_cap_rank (int): Second coin's market cap rank
        - coin_1_total_volume (float): Second coin's total volume
        - coin_1_high_24h (float): Second coin's 24h high price
        - coin_1_low_24h (float): Second coin's 24h low price
        - coin_1_price_change_24h (float): Second coin's 24h price change
        - coin_1_price_change_percentage_24h (float): Second coin's 24h price change percentage
        - coin_1_market_cap_change_24h (float): Second coin's 24h market cap change
        - coin_1_market_cap_change_percentage_24h (float): Second coin's 24h market cap change percentage
        - coin_1_circulating_supply (float): Second coin's circulating supply
        - coin_1_total_supply (float): Second coin's total supply
        - coin_1_max_supply (float): Second coin's max supply
        - coin_1_ath (float): Second coin's all-time high price
        - coin_1_ath_change_percentage (float): Second coin's ATH change percentage
        - coin_1_ath_date (str): Second coin's ATH date
        - coin_1_atl (float): Second coin's all-time low price
        - coin_1_atl_change_percentage (float): Second coin's ATL change percentage
        - coin_1_atl_date (str): Second coin's ATL date
        - coin_1_last_updated (str): Second coin's last updated timestamp
    """
    return {
        "coin_0_id": "bitcoin",
        "coin_0_symbol": "btc",
        "coin_0_name": "Bitcoin",
        "coin_0_image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        "coin_0_current_price": 45000.0,
        "coin_0_market_cap": 880000000000,
        "coin_0_market_cap_rank": 1,
        "coin_0_total_volume": 25000000000,
        "coin_0_high_24h": 46000.0,
        "coin_0_low_24h": 44000.0,
        "coin_0_price_change_24h": 1200.0,
        "coin_0_price_change_percentage_24h": 2.73,
        "coin_0_market_cap_change_24h": 20000000000,
        "coin_0_market_cap_change_percentage_24h": 2.33,
        "coin_0_circulating_supply": 19500000.0,
        "coin_0_total_supply": 21000000.0,
        "coin_0_max_supply": 21000000.0,
        "coin_0_ath": 69000.0,
        "coin_0_ath_change_percentage": -34.78,
        "coin_0_ath_date": "2021-11-10T14:24:11.849Z",
        "coin_0_atl": 67.81,
        "coin_0_atl_change_percentage": 66300.0,
        "coin_0_atl_date": "2013-07-06T00:00:00.000Z",
        "coin_0_last_updated": "2023-10-15T12:34:56.789Z",
        "coin_1_id": "ethereum",
        "coin_1_symbol": "eth",
        "coin_1_name": "Ethereum",
        "coin_1_image": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
        "coin_1_current_price": 3200.0,
        "coin_1_market_cap": 384000000000,
        "coin_1_market_cap_rank": 2,
        "coin_1_total_volume": 15000000000,
        "coin_1_high_24h": 3250.0,
        "coin_1_low_24h": 3150.0,
        "coin_1_price_change_24h": 80.0,
        "coin_1_price_change_percentage_24h": 2.56,
        "coin_1_market_cap_change_24h": 8000000000,
        "coin_1_market_cap_change_percentage_24h": 2.13,
        "coin_1_circulating_supply": 120000000.0,
        "coin_1_total_supply": 120000000.0,
        "coin_1_max_supply": None,
        "coin_1_ath": 4891.70,
        "coin_1_ath_change_percentage": -34.58,
        "coin_1_ath_date": "2021-11-10T14:24:19.648Z",
        "coin_1_atl": 0.43,
        "coin_1_atl_change_percentage": 743000.0,
        "coin_1_atl_date": "2015-10-20T00:00:00.000Z",
        "coin_1_last_updated": "2023-10-15T12:34:56.789Z"
    }


def coingecko_api_server_API_coins_markets(
    vs_currency: str,
    category: Optional[str] = None,
    ids: Optional[str] = None,
    include_tokens: Optional[str] = None,
    locale: Optional[str] = None,
    names: Optional[str] = None,
    order: Optional[str] = None,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    precision: Optional[str] = None,
    price_change_percentage: Optional[str] = None,
    sparkline: Optional[bool] = None
):
    pass