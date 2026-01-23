from typing import Dict,Any,Optional
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching candlestick data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - candlestick_0_timestamp (str): Timestamp of first candlestick
        - candlestick_0_open (str): Open price of first candlestick
        - candlestick_0_high (str): High price of first candlestick
        - candlestick_0_low (str): Low price of first candlestick
        - candlestick_0_close (str): Close price of first candlestick
        - candlestick_0_volume (str): Volume of first candlestick
        - candlestick_0_volumeCurrency (str): Volume currency of first candlestick
        - candlestick_1_timestamp (str): Timestamp of second candlestick
        - candlestick_1_open (str): Open price of second candlestick
        - candlestick_1_high (str): High price of second candlestick
        - candlestick_1_low (str): Low price of second candlestick
        - candlestick_1_close (str): Close price of second candlestick
        - candlestick_1_volume (str): Volume of second candlestick
        - candlestick_1_volumeCurrency (str): Volume currency of second candlestick
    """
    return {
        "candlestick_0_timestamp": "2023-11-20T10:00:00Z",
        "candlestick_0_open": "35000.0",
        "candlestick_0_high": "35100.0",
        "candlestick_0_low": "34950.0",
        "candlestick_0_close": "35080.0",
        "candlestick_0_volume": "100.5",
        "candlestick_0_volumeCurrency": "BTC",
        "candlestick_1_timestamp": "2023-11-20T10:01:00Z",
        "candlestick_1_open": "35080.0",
        "candlestick_1_high": "35150.0",
        "candlestick_1_low": "35070.0",
        "candlestick_1_close": "35120.0",
        "candlestick_1_volume": "95.8",
        "candlestick_1_volumeCurrency": "BTC"
    }


def okx_server_get_candlesticks(bar: Optional[str] = None, instrument: str = "", limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Get candlestick data for an OKX instrument.

    Args:
        bar (Optional[str]): Time interval (e.g. 1m, 5m, 1H, 1D). Defaults to '1m' if not provided.
        instrument (str): Instrument ID (e.g. BTC-USDT). Required field.
        limit (Optional[int]): Number of candlesticks to retrieve (max 100). Defaults to 2 if not provided or out of range.

    Returns:
        Dict containing a list of candlestick data with the following structure:
        - candlesticks (List[Dict]): List of candlestick dictionaries, each containing:
            - timestamp (str): Time of the candlestick in ISO format
            - open (str): Opening price
            - high (str): Highest price
            - low (str): Lowest price
            - close (str): Closing price
            - volume (str): Trading volume
            - volumeCurrency (str): Currency of the volume

    Raises:
        ValueError: If instrument is empty or None
    """
    # Input validation
    if not instrument:
        raise ValueError("Instrument is required")

    # Set default values
    if not bar:
        bar = "1m"
    if not limit or limit <= 0 or limit > 100:
        limit = 2

    # Fetch simulated external data
    api_data = call_external_api("okx-server-get_candlesticks")

    # Construct candlesticks list based on limit (always generate at least one item)
    candlesticks = []

    # Add first candlestick
    candlesticks.append({
        "timestamp": api_data["candlestick_0_timestamp"],
        "open": api_data["candlestick_0_open"],
        "high": api_data["candlestick_0_high"],
        "low": api_data["candlestick_0_low"],
        "close": api_data["candlestick_0_close"],
        "volume": api_data["candlestick_0_volume"],
        "volumeCurrency": api_data["candlestick_0_volumeCurrency"]
    })

    # Add second candlestick if limit allows
    if limit >= 2:
        candlesticks.append({
            "timestamp": api_data["candlestick_1_timestamp"],
            "open": api_data["candlestick_1_open"],
            "high": api_data["candlestick_1_high"],
            "low": api_data["candlestick_1_low"],
            "close": api_data["candlestick_1_close"],
            "volume": api_data["candlestick_1_volume"],
            "volumeCurrency": api_data["candlestick_1_volumeCurrency"]
        })

    return {"candlesticks": candlesticks}