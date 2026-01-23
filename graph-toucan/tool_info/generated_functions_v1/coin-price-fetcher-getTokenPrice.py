from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency price data from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - price (float): The current price of the requested cryptocurrency in USD
        - error (str): Error message if the price fetch failed; empty string if no error
    """
    # Simulated response based on token input (ignored in simulation)
    return {
        "price": 43250.75,
        "error": ""
    }

def coin_price_fetcher_getTokenPrice(token: str) -> Dict[str, Any]:
    """
    Get the current price of a cryptocurrency.
    
    Args:
        token (str): The cryptocurrency token symbol (e.g., 'BTC', 'ETH')
    
    Returns:
        Dict with the following keys:
        - price (float): The current price of the requested cryptocurrency in USD or stablecoin terms
        - error (str): Error message if the price fetch failed, e.g., due to HTTP error or invalid token
        
    Example:
        {
            "price": 43250.75,
            "error": ""
        }
    """
    if not token or not isinstance(token, str):
        return {
            "price": 0.0,
            "error": "Invalid token: token must be a non-empty string"
        }
    
    # Simulate API call to fetch price
    api_data = call_external_api("coin-price-fetcher-getTokenPrice")
    
    # Construct and return result matching output schema
    return {
        "price": api_data["price"],
        "error": api_data["error"]
    }