from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for financial ticker price information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - open (float): Opening price of the ticker for the period
        - high (float): Highest price of the ticker during the period
        - low (float): Lowest price of the ticker during the period
        - close (float): Closing price of the ticker for the period
        - volume (float): Trading volume (in shares or units) for the period
        - error (str): Error message if the request failed, otherwise None
    """
    return {
        "open": 150.25,
        "high": 155.7,
        "low": 148.3,
        "close": 154.6,
        "volume": 2345678.0,
        "error": None
    }

def finance_mcp_server_get_price(ticker: str, period: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the price of a stock/crypto ticker for a given period.
    
    Args:
        ticker (str): The ticker symbol for the stock or cryptocurrency (required)
        period (Optional[str]): The time period for which to retrieve price data (optional)
    
    Returns:
        Dict containing the following fields:
        - open (float): Opening price of the ticker for the period
        - high (float): Highest price of the ticker during the period
        - low (float): Lowest price of the ticker during the period
        - close (float): Closing price of the ticker for the period
        - volume (float): Trading volume (in shares or units) for the period
        - error (Optional[str]): Error message if the request failed, otherwise None
    
    Raises:
        ValueError: If ticker is empty or None
    """
    if not ticker:
        return {"error": "Ticker is required"}
    
    # Call external API to get data (simulated)
    api_data = call_external_api("finance-mcp-server-get_price")
    
    # Construct result dictionary matching output schema
    result: Dict[str, Any] = {
        "open": api_data["open"],
        "high": api_data["high"],
        "low": api_data["low"],
        "close": api_data["close"],
        "volume": api_data["volume"]
    }
    
    # Add error field only if present
    if api_data.get("error") is not None:
        result["error"] = api_data["error"]
    
    return result