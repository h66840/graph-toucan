from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cryptocurrency price.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - price (float): Current market price of the cryptocurrency in USD
    """
    # Simulated response from external API
    return {
        "price": 43250.75  # Simulated BTC price in USD
    }

def coin_mcp_server_getTokenPrice(token: str) -> Dict[str, Any]:
    """
    Get the current price of a cryptocurrency in USD.
    
    Args:
        token (str): The cryptocurrency symbol or name (e.g., 'BTC', 'ETH')
    
    Returns:
        Dict[str, Any]: A dictionary containing the current market price of the cryptocurrency in USD.
        - price (float): Current market price of the cryptocurrency in USD
    
    Raises:
        ValueError: If the token parameter is empty or not provided
    """
    # Input validation
    if not token or not isinstance(token, str) or not token.strip():
        raise ValueError("Parameter 'token' must be a non-empty string")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("coin-mcp-server-getTokenPrice")
    
    # Construct result matching output schema
    result = {
        "price": api_data["price"]
    }
    
    return result