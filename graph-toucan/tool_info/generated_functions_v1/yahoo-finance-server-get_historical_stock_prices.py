from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching historical stock prices from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - ticker_symbol (str): The ticker symbol for which historical prices were retrieved
        - interval (str): The time interval used for the historical data points
        - period (str): The historical period covered by the data
        - metadata_fetched_at (str): ISO format timestamp when data was fetched
        - metadata_currency (str): Currency of the stock prices
        - metadata_timezone (str): Timezone of the data
        - metadata_disclaimer (str): Disclaimer from the data source
        - historical_prices_0_Date (str): Date of first historical price entry
        - historical_prices_0_Open (float): Open price of first entry
        - historical_prices_0_High (float): High price of first entry
        - historical_prices_0_Low (float): Low price of first entry
        - historical_prices_0_Close (float): Close price of first entry
        - historical_prices_0_Volume (int): Volume of first entry
        - historical_prices_0_Adj_Close (float): Adjusted close price of first entry
        - historical_prices_1_Date (str): Date of second historical price entry
        - historical_prices_1_Open (float): Open price of second entry
        - historical_prices_1_High (float): High price of second entry
        - historical_prices_1_Low (float): Low price of second entry
        - historical_prices_1_Close (float): Close price of second entry
        - historical_prices_1_Volume (int): Volume of second entry
        - historical_prices_1_Adj_Close (float): Adjusted close price of second entry
    """
    now = datetime.now()
    return {
        "ticker_symbol": "AAPL",
        "interval": "1d",
        "period": "1mo",
        "metadata_fetched_at": now.isoformat(),
        "metadata_currency": "USD",
        "metadata_timezone": "America/New_York",
        "metadata_disclaimer": "Data provided for informational purposes only",
        "historical_prices_0_Date": (now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "historical_prices_0_Open": round(random.uniform(150, 180), 2),
        "historical_prices_0_High": round(random.uniform(155, 185), 2),
        "historical_prices_0_Low": round(random.uniform(145, 155), 2),
        "historical_prices_0_Close": round(random.uniform(150, 180), 2),
        "historical_prices_0_Volume": random.randint(50000000, 100000000),
        "historical_prices_0_Adj_Close": round(random.uniform(150, 180), 2),
        "historical_prices_1_Date": now.strftime("%Y-%m-%d"),
        "historical_prices_1_Open": round(random.uniform(150, 180), 2),
        "historical_prices_1_High": round(random.uniform(155, 185), 2),
        "historical_prices_1_Low": round(random.uniform(145, 155), 2),
        "historical_prices_1_Close": round(random.uniform(150, 180), 2),
        "historical_prices_1_Volume": random.randint(50000000, 100000000),
        "historical_prices_1_Adj_Close": round(random.uniform(150, 180), 2),
    }


def yahoo_finance_server_get_historical_stock_prices(
    ticker: str, period: Optional[str] = "1mo", interval: Optional[str] = "1d"
) -> Dict[str, Any]:
    """
    Get historical stock prices for a given ticker symbol from yahoo finance.

    Args:
        ticker (str): The ticker symbol of the stock to get historical prices for, e.g. "AAPL"
        period (str, optional): Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end. Default is "1mo"
        interval (str, optional): Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days. Default is "1d"

    Returns:
        Dict containing:
        - historical_prices (List[Dict]): List of dictionaries with keys: 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'
        - ticker_symbol (str): The ticker symbol for which historical prices were retrieved
        - interval (str): The time interval used for the historical data points
        - period (str): The historical period covered by the data
        - metadata (Dict): Additional information about the request and response

    Raises:
        ValueError: If ticker is not provided
    """
    if not ticker:
        raise ValueError("Ticker symbol is required")

    # Validate period
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    if period and period not in valid_periods:
        raise ValueError(f"Invalid period. Must be one of {valid_periods}")

    # Validate interval
    valid_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    if interval and interval not in valid_intervals:
        raise ValueError(f"Invalid interval. Must be one of {valid_intervals}")

    # Call external API to get data (simulated)
    api_data = call_external_api("yahoo-finance-server-get_historical_stock_prices")

    # Construct historical prices list from indexed fields
    historical_prices = [
        {
            "Date": api_data["historical_prices_0_Date"],
            "Open": api_data["historical_prices_0_Open"],
            "High": api_data["historical_prices_0_High"],
            "Low": api_data["historical_prices_0_Low"],
            "Close": api_data["historical_prices_0_Close"],
            "Volume": api_data["historical_prices_0_Volume"],
            "Adj Close": api_data["historical_prices_0_Adj_Close"],
        },
        {
            "Date": api_data["historical_prices_1_Date"],
            "Open": api_data["historical_prices_1_Open"],
            "High": api_data["historical_prices_1_High"],
            "Low": api_data["historical_prices_1_Low"],
            "Close": api_data["historical_prices_1_Close"],
            "Volume": api_data["historical_prices_1_Volume"],
            "Adj Close": api_data["historical_prices_1_Adj_Close"],
        },
    ]

    # Construct metadata
    metadata = {
        "fetched_at": api_data["metadata_fetched_at"],
        "currency": api_data["metadata_currency"],
        "timezone": api_data["metadata_timezone"],
        "disclaimer": api_data["metadata_disclaimer"],
    }

    # Return final structured response
    return {
        "historical_prices": historical_prices,
        "ticker_symbol": ticker,
        "interval": interval or "1d",
        "period": period or "1mo",
        "metadata": metadata,
    }