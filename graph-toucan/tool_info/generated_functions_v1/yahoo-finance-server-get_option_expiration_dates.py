from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for option expiration dates.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - expiration_date_0 (str): First available option expiration date in "YYYY-MM-DD" format
        - expiration_date_1 (str): Second available option expiration date in "YYYY-MM-DD" format
    """
    # Simulated response with two expiration dates for the given ticker
    return {
        "expiration_date_0": "2023-12-15",
        "expiration_date_1": "2024-01-19"
    }

def yahoo_finance_server_get_option_expiration_dates(ticker: str) -> Dict[str, Any]:
    """
    Fetch the available options expiration dates for a given ticker symbol.
    
    Args:
        ticker (str): The ticker symbol of the stock to get option expiration dates for, e.g. "AAPL"
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - expiration_dates (List[str]): List of available options expiration dates in "YYYY-MM-DD" format
        
    Raises:
        ValueError: If ticker is empty or not a string
    """
    # Input validation
    if not isinstance(ticker, str):
        raise ValueError("Ticker must be a string")
    if not ticker.strip():
        raise ValueError("Ticker cannot be empty")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("yahoo-finance-server-get_option_expiration_dates")
    
    # Construct the result structure matching the output schema
    expiration_dates: List[str] = [
        api_data["expiration_date_0"],
        api_data["expiration_date_1"]
    ]
    
    # Return result in the expected format
    return {
        "expiration_dates": expiration_dates
    }