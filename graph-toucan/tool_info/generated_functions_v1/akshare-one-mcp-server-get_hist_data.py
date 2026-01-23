from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching historical stock market data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - historical_data_0_timestamp (str): Timestamp for first record
        - historical_data_0_open (float): Open price for first record
        - historical_data_0_high (float): High price for first record
        - historical_data_0_low (float): Low price for first record
        - historical_data_0_close (float): Close price for first record
        - historical_data_0_volume (int): Volume for first record
        - historical_data_1_timestamp (str): Timestamp for second record
        - historical_data_1_open (float): Open price for second record
        - historical_data_1_high (float): High price for second record
        - historical_data_1_low (float): Low price for second record
        - historical_data_1_close (float): Close price for second record
        - historical_data_1_volume (int): Volume for second record
    """
    return {
        "historical_data_0_timestamp": "2023-01-01T00:00:00",
        "historical_data_0_open": 15.2,
        "historical_data_0_high": 15.8,
        "historical_data_0_low": 15.0,
        "historical_data_0_close": 15.6,
        "historical_data_0_volume": 1000000,
        "historical_data_1_timestamp": "2023-01-02T00:00:00",
        "historical_data_1_open": 15.7,
        "historical_data_1_high": 16.1,
        "historical_data_1_low": 15.5,
        "historical_data_1_close": 15.9,
        "historical_data_1_volume": 1200000,
    }

def akshare_one_mcp_server_get_hist_data(
    symbol: str,
    adjust: Optional[str] = None,
    end_date: Optional[str] = None,
    indicators_list: Optional[Any] = None,
    interval: Optional[str] = None,
    interval_multiplier: Optional[int] = None,
    recent_n: Optional[Any] = None,
    source: Optional[str] = None,
    start_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get historical stock market data for a given symbol.
    
    Args:
        symbol (str): Stock symbol/ticker (e.g. '000001') - required
        adjust (str, optional): Adjustment type (e.g., 'qfq' for pre-adjustment, 'hfq' for post-adjustment)
        end_date (str, optional): End date in YYYY-MM-DD format
        indicators_list (Any, optional): Technical indicators to add (not used in simulation)
        interval (str, optional): Time interval (e.g., '1d' for daily, '1w' for weekly)
        interval_multiplier (int, optional): Interval multiplier (e.g., 2 for every 2 days)
        recent_n (Any, optional): Number of most recent records to return (not used in simulation)
        source (str, optional): Data source (e.g., 'eastmoney_direct')
        start_date (str, optional): Start date in YYYY-MM-DD format
    
    Returns:
        Dict containing:
            - historical_data (List[Dict]): List of historical market data entries with:
                - timestamp (str): Time of the record
                - open (float): Opening price
                - high (float): Highest price
                - low (float): Lowest price
                - close (float): Closing price
                - volume (int): Trading volume
    
    Raises:
        ValueError: If symbol is not provided
    """
    if not symbol:
        raise ValueError("Symbol is required")

    # Fetch simulated data from external API
    api_data = call_external_api("akshare-one-mcp-server-get_hist_data")
    
    # Construct the nested structure matching the output schema
    historical_data = [
        {
            "timestamp": api_data["historical_data_0_timestamp"],
            "open": api_data["historical_data_0_open"],
            "high": api_data["historical_data_0_high"],
            "low": api_data["historical_data_0_low"],
            "close": api_data["historical_data_0_close"],
            "volume": api_data["historical_data_0_volume"]
        },
        {
            "timestamp": api_data["historical_data_1_timestamp"],
            "open": api_data["historical_data_1_open"],
            "high": api_data["historical_data_1_high"],
            "low": api_data["historical_data_1_low"],
            "close": api_data["historical_data_1_close"],
            "volume": api_data["historical_data_1_volume"]
        }
    ]
    
    return {
        "historical_data": historical_data
    }