from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bitcoin SV price.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - price_usd (float): the current price of Bitcoin SV (BSV) in USD
        - currency (str): the cryptocurrency symbol being priced, always "BSV"
        - price_source (str): the source or exchange providing the price data
    """
    return {
        "price_usd": 45.67,
        "currency": "BSV",
        "price_source": "reliable exchange API"
    }

def bitcoin_sv_tools_server_bsv_getPrice(args=None) -> Dict[str, Any]:
    """
    Retrieves the current price of Bitcoin SV (BSV) in USD from a reliable exchange API.
    
    This function simulates real-time market data retrieval and can be used for calculating
    transaction values, monitoring market conditions, or converting between BSV and fiat currencies.
    
    Args:
        args (object, optional): No parameters required - simply returns the current BSV price in USD
        
    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - price_usd (float): The current price of Bitcoin SV (BSV) in USD
            - currency (str): The cryptocurrency symbol, always "BSV"
            - price_source (str): The source or exchange providing the price data
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("bitcoin-sv-tools-server-bsv_getPrice")
        
        # Construct result matching output schema
        result = {
            "price_usd": float(api_data["price_usd"]),
            "currency": str(api_data["currency"]),
            "price_source": str(api_data["price_source"])
        }
        
        return result
        
    except Exception as e:
        # Handle any potential errors during execution
        return {
            "price_usd": 0.0,
            "currency": "BSV",
            "price_source": "error"
        }