from typing import Dict, List, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching OHLC data from external CoinGecko API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ohlc_data_0_timestamp (int): Timestamp in milliseconds for first OHLC entry
        - ohlc_data_0_open (float): Open price for first entry
        - ohlc_data_0_high (float): High price for first entry
        - ohlc_data_0_low (float): Low price for first entry
        - ohlc_data_0_close (float): Close price for first entry
        - ohlc_data_1_timestamp (int): Timestamp in milliseconds for second OHLC entry
        - ohlc_data_1_open (float): Open price for second entry
        - ohlc_data_1_high (float): High price for second entry
        - ohlc_data_1_low (float): Low price for second entry
        - ohlc_data_1_close (float): Close price for second entry
    """
    current_time_ms = int(time.time() * 1000)
    one_hour_ms = 60 * 60 * 1000

    # Generate two realistic OHLC entries
    base_price = random.uniform(1000, 50000)

    return {
        "ohlc_data_0_timestamp": current_time_ms - one_hour_ms,
        "ohlc_data_0_open": round(base_price, 2),
        "ohlc_data_0_high": round(base_price * random.uniform(1.01, 1.03), 2),
        "ohlc_data_0_low": round(base_price * random.uniform(0.97, 0.99), 2),
        "ohlc_data_0_close": round(base_price * random.uniform(0.99, 1.02), 2),

        "ohlc_data_1_timestamp": current_time_ms,
        "ohlc_data_1_open": round(base_price * random.uniform(0.99, 1.01), 2),
        "ohlc_data_1_high": round(base_price * random.uniform(1.01, 1.04), 2),
        "ohlc_data_1_low": round(base_price * random.uniform(0.96, 0.99), 2),
        "ohlc_data_1_close": round(base_price * random.uniform(0.98, 1.03), 2),
    }


def coingecko_api_server_API_coins_id_ohlc(
    days: str,
    id: str,
    precision: Optional[str] = None,
    vs_currency: str = "usd"
) -> Dict[str, Any]:
    """
    Fetches OHLC (Open, High, Low, Close) chart data for a specific cryptocurrency by its ID.

    This function simulates querying the CoinGecko API for OHLC data over a specified number of days
    and in a target currency. It returns a list of OHLC entries with timestamp and price values.

    Args:
        days (str): Number of days ago to fetch data for (e.g., "1", "7", "30").
        id (str): The coin ID (e.g., "bitcoin", "ethereum") as per CoinGecko's coins list.
        precision (Optional[str]): Decimal places for price values. If not provided, defaults to 2.
        vs_currency (str): The target currency for price data (e.g., "usd", "eur"). Default is "usd".

    Returns:
        Dict[str, Any]: A dictionary containing:
            - ohlc_data (List[List]): List of OHLC entries, each as [timestamp_ms, open, high, low, close]

    Raises:
        ValueError: If required parameters are missing or invalid.
    """
    # Input validation
    if not days:
        raise ValueError("Parameter 'days' is required.")
    if not id:
        raise ValueError("Parameter 'id' is required.")
    if not vs_currency:
        raise ValueError("Parameter 'vs_currency' is required.")

    try:
        days_int = int(days)
        if days_int <= 0:
            raise ValueError("Parameter 'days' must be a positive integer.")
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Parameter 'days' must be an integer string.")
        else:
            raise e

    # Set precision
    decimal_places = int(precision) if precision else 2
    if decimal_places < 0:
        raise ValueError("Parameter 'precision' must be non-negative.")

    # Fetch simulated external data
    api_data = call_external_api("coingecko-api-server-API-coins-id-ohlc")

    # Construct OHLC data list from flattened API response
    ohlc_data: List[List] = [
        [
            api_data["ohlc_data_0_timestamp"],
            round(api_data["ohlc_data_0_open"], decimal_places),
            round(api_data["ohlc_data_0_high"], decimal_places),
            round(api_data["ohlc_data_0_low"], decimal_places),
            round(api_data["ohlc_data_0_close"], decimal_places),
        ],
        [
            api_data["ohlc_data_1_timestamp"],
            round(api_data["ohlc_data_1_open"], decimal_places),
            round(api_data["ohlc_data_1_high"], decimal_places),
            round(api_data["ohlc_data_1_low"], decimal_places),
            round(api_data["ohlc_data_1_close"], decimal_places),
        ],
    ]

    return {
        "ohlc_data": ohlc_data
    }