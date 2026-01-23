from typing import Dict, List, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching option chain data from external API (e.g., Yahoo Finance).
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ticker (str): The ticker symbol for which the option chain was retrieved
        - expiration_date (str): The expiration date of the options (format: 'YYYY-MM-DD')
        - option_type (str): Type of options returned — either 'calls' or 'puts'
        - underlying_price (float): Current market price of the underlying stock
        - last_updated (str): Timestamp (ISO format) when data was fetched
        - metadata_source (str): Source of the data (e.g., 'Yahoo Finance')
        - metadata_status (str): Status of the query (e.g., 'success')
        - metadata_quality_flag (bool): Data quality indicator
        - option_0_strike (float): Strike price of first option contract
        - option_0_bid (float): Bid price of first option contract
        - option_0_ask (float): Ask price of first option contract
        - option_0_volume (int): Trading volume of first option contract
        - option_0_open_interest (int): Open interest of first option contract
        - option_0_implied_volatility (float): Implied volatility of first option contract
        - option_1_strike (float): Strike price of second option contract
        - option_1_bid (float): Bid price of second option contract
        - option_1_ask (float): Ask price of second option contract
        - option_1_volume (int): Trading volume of second option contract
        - option_1_open_interest (int): Open interest of second option contract
        - option_1_implied_volatility (float): Implied volatility of second option contract
    """
    return {
        "ticker": "AAPL",
        "expiration_date": "2025-04-18",
        "option_type": "calls",
        "underlying_price": 175.43,
        "last_updated": datetime.now().isoformat(),
        "metadata_source": "Yahoo Finance",
        "metadata_status": "success",
        "metadata_quality_flag": True,
        "option_0_strike": 170.0,
        "option_0_bid": 5.60,
        "option_0_ask": 5.70,
        "option_0_volume": 1250,
        "option_0_open_interest": 3400,
        "option_0_implied_volatility": 0.285,
        "option_1_strike": 175.0,
        "option_1_bid": 2.80,
        "option_1_ask": 2.90,
        "option_1_volume": 2100,
        "option_1_open_interest": 5600,
        "option_1_implied_volatility": 0.263,
    }

def yahoo_finance_server_get_option_chain(ticker: str, expiration_date: str, option_type: str) -> Dict[str, Any]:
    """
    Fetch the option chain for a given ticker symbol, expiration date, and option type.
    
    Args:
        ticker (str): The ticker symbol of the stock to get option chain for, e.g. "AAPL"
        expiration_date (str): The expiration date for the options chain (format: 'YYYY-MM-DD')
        option_type (str): The type of option to fetch ('calls' or 'puts')
    
    Returns:
        Dict containing:
        - options (List[Dict]): List of option contract details with strike, bid/ask, volume, 
          open interest, implied volatility, and expiration
        - underlying_price (float): Current market price of the underlying stock
        - expiration_date (str): Expiration date of the fetched options (format: 'YYYY-MM-DD')
        - option_type (str): Type of options returned — either 'calls' or 'puts'
        - ticker (str): The ticker symbol for which the option chain was retrieved
        - last_updated (str): Timestamp (ISO format) indicating when the data was fetched
        - metadata (Dict): Additional context including source, status, and quality flags
    
    Raises:
        ValueError: If option_type is not 'calls' or 'puts', or if expiration_date format is invalid
    """
    # Input validation
    if not ticker:
        raise ValueError("Ticker symbol is required")
    
    if option_type not in ['calls', 'puts']:
        raise ValueError("option_type must be either 'calls' or 'puts'")
    
    # Basic date format validation
    try:
        datetime.strptime(expiration_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("expiration_date must be in YYYY-MM-DD format")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("yahoo-finance-server-get_option_chain")
    
    # Construct options list from indexed fields
    options = [
        {
            "strike": api_data["option_0_strike"],
            "bid": api_data["option_0_bid"],
            "ask": api_data["option_0_ask"],
            "volume": api_data["option_0_volume"],
            "open_interest": api_data["option_0_open_interest"],
            "implied_volatility": api_data["option_0_implied_volatility"],
            "expiration": api_data["expiration_date"]
        },
        {
            "strike": api_data["option_1_strike"],
            "bid": api_data["option_1_bid"],
            "ask": api_data["option_1_ask"],
            "volume": api_data["option_1_volume"],
            "open_interest": api_data["option_1_open_interest"],
            "implied_volatility": api_data["option_1_implied_volatility"],
            "expiration": api_data["expiration_date"]
        }
    ]
    
    # Construct metadata dictionary
    metadata = {
        "source": api_data["metadata_source"],
        "status": api_data["metadata_status"],
        "quality_flag": api_data["metadata_quality_flag"]
    }
    
    # Construct final result matching output schema
    result = {
        "options": options,
        "underlying_price": api_data["underlying_price"],
        "expiration_date": api_data["expiration_date"],
        "option_type": api_data["option_type"],
        "ticker": api_data["ticker"],
        "last_updated": api_data["last_updated"],
        "metadata": metadata
    }
    
    return result