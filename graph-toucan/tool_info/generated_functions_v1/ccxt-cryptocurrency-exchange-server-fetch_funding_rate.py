from typing import Dict, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching funding rate data from an external cryptocurrency exchange API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - funding_rate (float): The current funding rate as a decimal
        - next_funding_timestamp (int): Unix timestamp in milliseconds for next funding
        - next_funding_datetime (str): ISO 8601 datetime string for next funding
        - previous_funding_rate (float): Previous funding rate value
        - symbol (str): Symbol for which funding rate was fetched
        - exchange_id (str): Exchange ID that provided the data
        - timestamp (int): Unix timestamp when rate was recorded
        - datetime (str): ISO 8601 datetime string corresponding to timestamp
        - info_fundingInterval (int): Funding interval in seconds (example metadata)
        - info_nextFundingTime (int): Next funding time in milliseconds (example metadata)
    """
    return {
        "funding_rate": 0.000125,
        "next_funding_timestamp": 1700006400000,
        "next_funding_datetime": "2023-11-15T00:00:00.000Z",
        "previous_funding_rate": -0.000075,
        "symbol": "BTC/USDT:USDT",
        "exchange_id": "binance",
        "timestamp": 1699999200000,
        "datetime": "2023-11-14T22:00:00.000Z",
        "info_fundingInterval": 28800,
        "info_nextFundingTime": 1700006400000
    }

def ccxt_cryptocurrency_exchange_server_fetch_funding_rate(
    exchange_id: str,
    symbol: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches the current or historical funding rate for a perpetual futures contract symbol.
    
    This function simulates interaction with a cryptocurrency exchange using CCXT to retrieve
    funding rate information for perpetual contracts. It handles both authenticated and 
    unauthenticated requests depending on provided credentials.
    
    Args:
        exchange_id (str): The ID of the exchange (e.g., 'binance', 'bybit'). Case-insensitive.
        symbol (str): The symbol to fetch the funding rate for (e.g., 'BTC/USDT:USDT', 'ETH-PERP').
        api_key (Optional[str]): Optional API key for authentication.
        secret_key (Optional[str]): Optional secret key for authentication.
        passphrase (Optional[str]): Optional passphrase required by some exchanges.
        params (Optional[Dict[str, Any]]): Optional parameters for client setup or API call.
            Critical for client setup: Include {'options': {'defaultType': 'future'}} or 
            {'options': {'defaultType': 'swap'}} for correct market type.
    
    Returns:
        Dict containing funding rate information with the following structure:
        - funding_rate (float): Current funding rate as decimal
        - next_funding_timestamp (int): Unix timestamp (ms) for next funding
        - next_funding_datetime (str): ISO 8601 datetime for next funding
        - previous_funding_rate (float): Previous funding rate value
        - symbol (str): Symbol for which data was fetched
        - exchange_id (str): Exchange ID that provided data
        - timestamp (int): Unix timestamp (ms) when rate was recorded
        - datetime (str): ISO 8601 datetime corresponding to timestamp
        - info (Dict): Raw response from exchange with additional metadata
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not exchange_id:
        raise ValueError("exchange_id is required")
    if not symbol:
        raise ValueError("symbol is required")
    
    # Normalize exchange_id to lowercase
    exchange_id = exchange_id.lower().strip()
    
    # Simulate calling external API
    api_data = call_external_api("ccxt-cryptocurrency-exchange-server-fetch_funding_rate")
    
    # Construct the nested 'info' dictionary from flattened fields
    info = {
        "fundingInterval": api_data["info_fundingInterval"],
        "nextFundingTime": api_data["info_nextFundingTime"]
    }
    
    # Build final result structure matching output schema
    result = {
        "funding_rate": api_data["funding_rate"],
        "next_funding_timestamp": api_data["next_funding_timestamp"],
        "next_funding_datetime": api_data["next_funding_datetime"],
        "previous_funding_rate": api_data["previous_funding_rate"],
        "symbol": api_data["symbol"],
        "exchange_id": api_data["exchange_id"],
        "timestamp": api_data["timestamp"],
        "datetime": api_data["datetime"],
        "info": info
    }
    
    return result