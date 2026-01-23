from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cryptocurrency price information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - price_bitcoin_usd (float): Current price of Bitcoin in USD
        - price_ethereum_usd (float): Current price of Ethereum in USD
        - price_bitcoin_eur (float): Current price of Bitcoin in EUR
        - price_ethereum_eur (float): Current price of Ethereum in EUR
        - change_24h_bitcoin_usd (float): 24h price change percentage for Bitcoin in USD
        - change_24h_ethereum_usd (float): 24h price change percentage for Ethereum in USD
        - volume_24h_bitcoin_usd (float): 24h trading volume for Bitcoin in USD
        - volume_24h_ethereum_usd (float): 24h trading volume for Ethereum in USD
        - market_cap_bitcoin_usd (float): Market cap for Bitcoin in USD
        - market_cap_ethereum_usd (float): Market cap for Ethereum in USD
    """
    return {
        "price_bitcoin_usd": 43000.0,
        "price_ethereum_usd": 2600.0,
        "price_bitcoin_eur": 39500.0,
        "price_ethereum_eur": 2400.0,
        "change_24h_bitcoin_usd": 2.5,
        "change_24h_ethereum_usd": -1.2,
        "volume_24h_bitcoin_usd": 28000000000.0,
        "volume_24h_ethereum_usd": 15000000000.0,
        "market_cap_bitcoin_usd": 850000000000.0,
        "market_cap_ethereum_usd": 310000000000.0,
    }


def coingecko_mcp_server_coingecko_price(
    ids: List[str],
    vs_currencies: List[str],
    include_24hr_change: Optional[bool] = False,
    include_24hr_vol: Optional[bool] = False,
    include_market_cap: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Get current price data for cryptocurrencies.

    Args:
        ids (List[str]): List of coin IDs (e.g., 'bitcoin', 'ethereum').
        vs_currencies (List[str]): List of currencies to compare against (e.g., 'usd', 'eur').
        include_24hr_change (Optional[bool]): Whether to include 24hr price change data.
        include_24hr_vol (Optional[bool]): Whether to include 24hr volume data.
        include_market_cap (Optional[bool]): Whether to include market cap data.

    Returns:
        Dict containing:
        - prices (Dict): mapping of coin IDs to a dictionary of currency-price pairs

    Example:
        {
            "prices": {
                "bitcoin": {"usd": 43000.0, "eur": 39500.0},
                "ethereum": {"usd": 2600.0, "eur": 2400.0}
            }
        }
    """
    # Input validation
    if not ids:
        raise ValueError("Parameter 'ids' must be a non-empty list.")
    if not vs_currencies:
        raise ValueError("Parameter 'vs_currencies' must be a non-empty list.")

    # Fetch simulated API data
    api_data = call_external_api("coingecko-mcp-server-coingecko_price")

    # Initialize result structure
    result: Dict[str, Any] = {"prices": {}}

    # Construct prices dictionary
    for coin_id in ids:
        result["prices"][coin_id] = {}
        for currency in vs_currencies:
            key = f"price_{coin_id}_{currency}"
            # Generate realistic price if not in mock data
            if key in api_data:
                result["prices"][coin_id][currency] = api_data[key]
            else:
                # Fallback: generate a plausible price based on coin and currency
                base_price = 10000 if "bitcoin" in coin_id else 2000
                currency_factor = 1.0 if currency == "usd" else 0.92
                volatility = hash(coin_id + currency) % 1000 / 1000 * 0.1
                price = base_price * currency_factor * (1 + volatility)
                result["prices"][coin_id][currency] = round(price, 2)

    return result