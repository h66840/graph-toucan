from typing import Dict, List, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching real-time stock market data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_0_symbol (str): Stock symbol for the first entry
        - data_0_price (float): Current price of the first stock
        - data_0_change (float): Price change of the first stock
        - data_0_pct_change (float): Percentage change of the first stock
        - data_0_volume (int): Trading volume of the first stock
        - data_0_amount (float): Trading amount of the first stock
        - data_0_open (float): Opening price of the first stock
        - data_0_high (float): Highest price of the first stock
        - data_0_low (float): Lowest price of the first stock
        - data_0_prev_close (float): Previous closing price of the first stock
        - data_0_timestamp (int): Timestamp of the first stock data
        - data_1_symbol (str): Stock symbol for the second entry
        - data_1_price (float): Current price of the second stock
        - data_1_change (float): Price change of the second stock
        - data_1_pct_change (float): Percentage change of the second stock
        - data_1_volume (int): Trading volume of the second stock
        - data_1_amount (float): Trading amount of the second stock
        - data_1_open (float): Opening price of the second stock
        - data_1_high (float): Highest price of the second stock
        - data_1_low (float): Lowest price of the second stock
        - data_1_prev_close (float): Previous closing price of the second stock
        - data_1_timestamp (int): Timestamp of the second stock data
    """
    current_timestamp = int(time.time())
    return {
        "data_0_symbol": "000001",
        "data_0_price": round(15.67 + random.uniform(-1.0, 1.0), 2),
        "data_0_change": round(random.uniform(-1.0, 1.0), 2),
        "data_0_pct_change": round(random.uniform(-5.0, 5.0), 2),
        "data_0_volume": random.randint(1_000_000, 10_000_000),
        "data_0_amount": round(random.uniform(10_000_000, 100_000_000), 2),
        "data_0_open": round(15.67 + random.uniform(-0.5, 0.5), 2),
        "data_0_high": round(16.0 + random.uniform(0, 0.5), 2),
        "data_0_low": round(15.0 + random.uniform(0, 0.5), 2),
        "data_0_prev_close": round(15.67, 2),
        "data_0_timestamp": current_timestamp,

        "data_1_symbol": "600036",
        "data_1_price": round(25.89 + random.uniform(-1.5, 1.5), 2),
        "data_1_change": round(random.uniform(-1.5, 1.5), 2),
        "data_1_pct_change": round(random.uniform(-6.0, 6.0), 2),
        "data_1_volume": random.randint(2_000_000, 15_000_000),
        "data_1_amount": round(random.uniform(20_000_000, 150_000_000), 2),
        "data_1_open": round(25.89 + random.uniform(-0.8, 0.8), 2),
        "data_1_high": round(26.5 + random.uniform(0, 0.8), 2),
        "data_1_low": round(25.0 + random.uniform(0, 0.8), 2),
        "data_1_prev_close": round(25.89, 2),
        "data_1_timestamp": current_timestamp,
    }


def akshare_one_mcp_server_get_realtime_data(source: Optional[str] = None, symbol: Optional[str] = None) -> Dict[str, Any]:
    """
    Get real-time stock market data from the specified source for the given symbol.

    Args:
        source (Optional[str]): Data source (e.g., 'eastmoney_direct'). Defaults to None.
        symbol (Optional[unknown]): Stock symbol/ticker (e.g. '000001'). Defaults to None.

    Returns:
        Dict containing a list of stock data entries. Each entry is a dictionary with the following keys:
        - symbol (str): Stock symbol
        - price (float): Current trading price
        - change (float): Absolute price change
        - pct_change (float): Percentage price change
        - volume (int): Trading volume
        - amount (float): Trading amount
        - open (float): Opening price
        - high (float): Highest price
        - low (float): Lowest price
        - prev_close (float): Previous closing price
        - timestamp (int): Unix timestamp of the data

    Note:
        This function simulates real-time data retrieval by calling an external API simulation
        and transforming flat response into the required nested structure.
    """
    try:
        # Call the simulated external API
        api_data = call_external_api("akshare-one-mcp-server-get_realtime_data")

        # Construct the result list by mapping flat fields to nested structure
        data_entries: List[Dict[str, Any]] = [
            {
                "symbol": api_data["data_0_symbol"],
                "price": api_data["data_0_price"],
                "change": api_data["data_0_change"],
                "pct_change": api_data["data_0_pct_change"],
                "volume": api_data["data_0_volume"],
                "amount": api_data["data_0_amount"],
                "open": api_data["data_0_open"],
                "high": api_data["data_0_high"],
                "low": api_data["data_0_low"],
                "prev_close": api_data["data_0_prev_close"],
                "timestamp": api_data["data_0_timestamp"],
            },
            {
                "symbol": api_data["data_1_symbol"],
                "price": api_data["data_1_price"],
                "change": api_data["data_1_change"],
                "pct_change": api_data["data_1_pct_change"],
                "volume": api_data["data_1_volume"],
                "amount": api_data["data_1_amount"],
                "open": api_data["data_1_open"],
                "high": api_data["data_1_high"],
                "low": api_data["data_1_low"],
                "prev_close": api_data["data_1_prev_close"],
                "timestamp": api_data["data_1_timestamp"],
            }
        ]

        # If a specific symbol is requested, filter the results
        if symbol is not None:
            data_entries = [entry for entry in data_entries if entry["symbol"] == symbol]

        return {"data": data_entries}

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process real-time stock data: {e}")