from typing import Dict,Any
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - instrument (str): Instrument ID (e.g. BTC-USDT)
        - lastPrice (str): Latest traded price of the instrument
        - bid (str): Current highest bid price in the order book
        - ask (str): Current lowest ask price in the order book
        - high24h (str): Highest price in the last 24 hours
        - low24h (str): Lowest price in the last 24 hours
        - volume24h (str): Total trading volume in the last 24 hours
        - timestamp (str): ISO 8601 timestamp of the data point, in UTC
    """
    return {
        "instrument": "BTC-USDT",
        "lastPrice": "35000.00",
        "bid": "34999.50",
        "ask": "35000.50",
        "high24h": "36000.00",
        "low24h": "34000.00",
        "volume24h": "1000.50",
        "timestamp": "2023-04-05T12:00:00Z"
    }

def okx_server_get_price(instrument: str) -> Dict[str, Any]:
    """
    Get latest price for an OKX instrument.
    
    Args:
        instrument (str): Instrument ID (e.g. BTC-USDT)
        
    Returns:
        Dict containing price information with the following fields:
        - instrument (str): Instrument ID (e.g. BTC-USDT)
        - lastPrice (str): Latest traded price of the instrument
        - bid (str): Current highest bid price in the order book
        - ask (str): Current lowest ask price in the order book
        - high24h (str): Highest price in the last 24 hours
        - low24h (str): Lowest price in the last 24 hours
        - volume24h (str): Total trading volume in the last 24 hours
        - timestamp (str): ISO 8601 timestamp of the data point, in UTC
        
    Raises:
        ValueError: If instrument is empty or not a string
    """
    # Input validation
    if not instrument:
        raise ValueError("Instrument parameter is required")
    if not isinstance(instrument, str):
        raise ValueError("Instrument must be a string")
    
    # Call external API to get data
    api_data = call_external_api("okx-server-get_price")
    
    # Construct result matching output schema exactly
    result = {
        "instrument": api_data["instrument"],
        "lastPrice": api_data["lastPrice"],
        "bid": api_data["bid"],
        "ask": api_data["ask"],
        "high24h": api_data["high24h"],
        "low24h": api_data["low24h"],
        "volume24h": api_data["volume24h"],
        "timestamp": api_data["timestamp"]
    }
    
    return result