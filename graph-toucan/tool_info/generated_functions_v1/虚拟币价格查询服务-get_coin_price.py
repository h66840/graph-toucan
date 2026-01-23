from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency price data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - coin_name (str): Name of the cryptocurrency in uppercase
        - current_price (float): Current price in the specified currency
        - currency (str): Currency code (e.g., CNY, USD)
        - market_cap (float): Total market capitalization
        - volume_24h (float): 24-hour trading volume
        - price_change_24h (float): 24-hour price change percentage
        - last_updated (str): Timestamp of last update in "YYYY-MM-DD HH:MM:SS" format
    """
    # Simulated data based on tool name and typical crypto values
    return {
        "coin_name": "BITCOIN",
        "current_price": 285000.0,
        "currency": "CNY",
        "market_cap": 5600000000000.0,
        "volume_24h": 85000000000.0,
        "price_change_24h": 2.45,
        "last_updated": "2023-10-15 14:30:22"
    }

def 虚拟币价格查询服务_get_coin_price(coin_id: str, currency: Optional[str] = "cny") -> Dict[str, Any]:
    """
    获取指定虚拟币的当前价格信息。
    
    Args:
        coin_id (str): 虚拟币的ID (例如 bitcoin, ethereum, dogecoin)
        currency (str, optional): 货币单位，默认为人民币(cny)，也可以是usd等
    
    Returns:
        Dict containing the following keys:
        - coin_name (str): name of the cryptocurrency in uppercase
        - current_price (float): current price in the specified currency
        - currency (str): the currency unit used (e.g., CNY, USD)
        - market_cap (float): total market capitalization in the specified currency
        - volume_24h (float): 24-hour trading volume in the specified currency
        - price_change_24h (float): percentage change in price over the last 24 hours
        - last_updated (str): timestamp of when the data was last updated (format: "YYYY-MM-DD HH:MM:SS")
    
    Raises:
        ValueError: If coin_id is empty or invalid
    """
    if not coin_id or not coin_id.strip():
        raise ValueError("coin_id is required and cannot be empty")
    
    # Normalize currency input
    currency = currency.strip().lower() if currency else "cny"
    currency_upper = currency.upper()
    
    # Call external API simulation
    raw_data = call_external_api("虚拟币价格查询服务_get_coin_price")
    
    # Construct result using raw data with proper structure
    result = {
        "coin_name": raw_data["coin_name"],
        "current_price": raw_data["current_price"],
        "currency": raw_data["currency"],
        "market_cap": raw_data["market_cap"],
        "volume_24h": raw_data["volume_24h"],
        "price_change_24h": raw_data["price_change_24h"],
        "last_updated": raw_data["last_updated"]
    }
    
    # Adjust currency display if needed (though data is simulated)
    result["currency"] = currency_upper
    
    return result