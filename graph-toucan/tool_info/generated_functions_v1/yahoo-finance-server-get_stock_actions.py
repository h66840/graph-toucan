from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching stock actions data from Yahoo Finance API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - dividend_0_date (str): Date of first dividend event in ISO format
        - dividend_0_amount (float): Amount of first dividend
        - dividend_0_currency (str): Currency of first dividend
        - dividend_1_date (str): Date of second dividend event in ISO format
        - dividend_1_amount (float): Amount of second dividend
        - dividend_1_currency (str): Currency of second dividend
        - split_0_date (str): Date of first stock split in ISO format
        - split_0_split_ratio (str): Ratio of first stock split (e.g., "3:1")
        - split_0_multiplier (float): Multiplier of first stock split (e.g., 3.0)
        - split_1_date (str): Date of second stock split in ISO format
        - split_1_split_ratio (str): Ratio of second stock split (e.g., "2:1")
        - split_1_multiplier (float): Multiplier of second stock split (e.g., 2.0)
        - ticker (str): Ticker symbol for which data was retrieved
        - last_updated (str): ISO 8601 timestamp when data was fetched
        - metadata_source (str): Source of the data
        - metadata_data_quality (str): Quality indicator of the data
        - metadata_warnings (str): Any warnings (e.g., "No actions found" or "OK")
    """
    return {
        "dividend_0_date": "2023-05-10",
        "dividend_0_amount": 0.24,
        "dividend_0_currency": "USD",
        "dividend_1_date": "2023-02-10",
        "dividend_1_amount": 0.23,
        "dividend_1_currency": "USD",
        "split_0_date": "2020-08-31",
        "split_0_split_ratio": "4:1",
        "split_0_multiplier": 4.0,
        "split_1_date": "2014-06-09",
        "split_1_split_ratio": "7:1",
        "split_1_multiplier": 7.0,
        "ticker": "AAPL",
        "last_updated": "2024-01-15T10:30:00Z",
        "metadata_source": "Yahoo Finance",
        "metadata_data_quality": "high",
        "metadata_warnings": "OK"
    }

def yahoo_finance_server_get_stock_actions(ticker: str) -> Dict[str, Any]:
    """
    Get stock dividends and stock splits for a given ticker symbol from Yahoo Finance.
    
    Args:
        ticker (str): The ticker symbol of the stock to get stock actions for, e.g. "AAPL"
    
    Returns:
        Dict containing:
        - dividends (List[Dict]): List of dividend events with keys 'date', 'amount', and 'currency'
        - splits (List[Dict]): List of stock split events with keys 'date', 'split_ratio', and 'multiplier'
        - ticker (str): The ticker symbol for which stock actions were retrieved
        - last_updated (str): ISO 8601 timestamp indicating when the data was last updated or fetched
        - metadata (Dict): Additional context such as source, data quality, or warnings
    
    Raises:
        ValueError: If ticker is empty or not a string
    """
    if not ticker or not isinstance(ticker, str):
        raise ValueError("Ticker must be a non-empty string")
    
    # Call external API to get flattened data
    api_data = call_external_api("yahoo-finance-server-get_stock_actions")
    
    # Construct dividends list
    dividends = [
        {
            "date": api_data["dividend_0_date"],
            "amount": api_data["dividend_0_amount"],
            "currency": api_data["dividend_0_currency"]
        },
        {
            "date": api_data["dividend_1_date"],
            "amount": api_data["dividend_1_amount"],
            "currency": api_data["dividend_1_currency"]
        }
    ]
    
    # Construct splits list
    splits = [
        {
            "date": api_data["split_0_date"],
            "split_ratio": api_data["split_0_split_ratio"],
            "multiplier": api_data["split_0_multiplier"]
        },
        {
            "date": api_data["split_1_date"],
            "split_ratio": api_data["split_1_split_ratio"],
            "multiplier": api_data["split_1_multiplier"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "source": api_data["metadata_source"],
        "data_quality": api_data["metadata_data_quality"],
        "warnings": api_data["metadata_warnings"]
    }
    
    # Return structured response matching output schema
    return {
        "dividends": dividends,
        "splits": splits,
        "ticker": api_data["ticker"],
        "last_updated": api_data["last_updated"],
        "metadata": metadata
    }