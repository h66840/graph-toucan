from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cryptocurrency prices.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - coin_0_name (str): First cryptocurrency name
        - coin_0_symbol (str): First cryptocurrency symbol
        - coin_0_cny_price (float): First cryptocurrency price in CNY
        - coin_0_usd_price (float): First cryptocurrency price in USD
        - coin_0_price_change_24h (float): First cryptocurrency 24h price change in percentage
        - coin_1_name (str): Second cryptocurrency name
        - coin_1_symbol (str): Second cryptocurrency symbol
        - coin_1_cny_price (float): Second cryptocurrency price in CNY
        - coin_1_usd_price (float): Second cryptocurrency price in USD
        - coin_1_price_change_24h (float): Second cryptocurrency 24h price change in percentage
    """
    return {
        "coin_0_name": "Bitcoin",
        "coin_0_symbol": "BTC",
        "coin_0_cny_price": 285000.0,
        "coin_0_usd_price": 39500.0,
        "coin_0_price_change_24h": 2.5,
        "coin_1_name": "Ethereum",
        "coin_1_symbol": "ETH",
        "coin_1_cny_price": 18500.0,
        "coin_1_usd_price": 2560.0,
        "coin_1_price_change_24h": -1.2
    }

def 虚拟币价格查询服务_get_common_coins_prices() -> Dict[str, Any]:
    """
    获取常见虚拟币的价格信息
    
    Returns:
        Dict containing a list of coin price information, each with:
        - name (str): Name of the cryptocurrency
        - symbol (str): Symbol of the cryptocurrency
        - cny_price (float): Price in Chinese Yuan (CNY)
        - usd_price (float): Price in US Dollar (USD)
        - price_change_24h (float): 24-hour price change percentage
    """
    try:
        api_data = call_external_api("虚拟币价格查询服务_get_common_coins_prices")
        
        coins = [
            {
                "name": api_data["coin_0_name"],
                "symbol": api_data["coin_0_symbol"],
                "cny_price": api_data["coin_0_cny_price"],
                "usd_price": api_data["coin_0_usd_price"],
                "price_change_24h": api_data["coin_0_price_change_24h"]
            },
            {
                "name": api_data["coin_1_name"],
                "symbol": api_data["coin_1_symbol"],
                "cny_price": api_data["coin_1_cny_price"],
                "usd_price": api_data["coin_1_usd_price"],
                "price_change_24h": api_data["coin_1_price_change_24h"]
            }
        ]
        
        return {"coins": coins}
    except KeyError as e:
        return {"error": f"Missing data field: {str(e)}", "coins": []}
    except Exception as e:
        return {"error": f"Failed to retrieve coin prices: {str(e)}", "coins": []}