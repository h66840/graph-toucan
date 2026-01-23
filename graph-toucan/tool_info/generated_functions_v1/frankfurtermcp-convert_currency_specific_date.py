from typing import Dict, Any
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching currency conversion data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - from_currency (str): Source currency code used in the conversion
        - to_currency (str): Target currency code used in the conversion
        - amount (float): Original amount in the source currency
        - converted_amount (float): Resulting amount in the target currency after conversion
        - exchange_rate (float): Exchange rate applied for the conversion
        - rate_date (str): Date of the exchange rate used in YYYY-MM-DD format
    """
    return {
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 100.0,
        "converted_amount": 92.5,
        "exchange_rate": 0.925,
        "rate_date": "2023-10-15"
    }

def frankfurtermcp_convert_currency_specific_date(
    amount: float,
    from_currency: str,
    specific_date: str,
    to_currency: str
) -> Dict[str, Any]:
    """
    Convert an amount from one currency to another using the exchange rates for a specific date.
    If there is no exchange rate available for the specific date, the rate for the closest available date before
    the specified date will be used.

    Args:
        amount (float): The amount in the source currency to convert.
        from_currency (str): The source currency code.
        specific_date (str): The specific date for which the conversion is requested in the YYYY-MM-DD format.
        to_currency (str): The target currency code.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - from_currency (str): source currency code used in the conversion
            - to_currency (str): target currency code used in the conversion
            - amount (float): original amount in the source currency
            - converted_amount (float): resulting amount in the target currency after conversion
            - exchange_rate (float): exchange rate applied for the conversion
            - rate_date (str): date of the exchange rate used in YYYY-MM-DD format

    Raises:
        ValueError: If amount is negative or date format is invalid.
        TypeError: If input types are incorrect.
    """
    # Input validation
    if not isinstance(amount, (int, float)) or amount < 0:
        raise ValueError("Amount must be a non-negative number.")
    if not isinstance(from_currency, str) or not from_currency.strip():
        raise ValueError("From currency must be a non-empty string.")
    if not isinstance(to_currency, str) or not to_currency.strip():
        raise ValueError("To currency must be a non-empty string.")
    if not isinstance(specific_date, str):
        raise TypeError("Specific date must be a string in YYYY-MM-DD format.")
    
    try:
        requested_date = datetime.strptime(specific_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Specific date must be in YYYY-MM-DD format.")
    
    # Normalize currency codes
    from_currency = from_currency.strip().upper()
    to_currency = to_currency.strip().upper()

    # Simulate fetching data from external API
    api_data = call_external_api("frankfurtermcp-convert_currency_specific_date")
    
    # Apply business logic: if exact date not available, use closest previous date
    # For simulation, we assume the API returns a valid rate_date
    rate_date = api_data["rate_date"]
    rate_date_obj = datetime.strptime(rate_date, "%Y-%m-%d")
    
    # Ensure rate_date is not after the requested date
    if rate_date_obj > requested_date:
        # Simulate finding the closest previous date by subtracting one day
        adjusted_rate_date = requested_date - timedelta(days=1)
        rate_date = adjusted_rate_date.strftime("%Y-%m-%d")
    else:
        rate_date = rate_date  # use as-is
    
    # Construct result using API data with proper field mapping
    result = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": float(amount),
        "converted_amount": api_data["converted_amount"],
        "exchange_rate": api_data["exchange_rate"],
        "rate_date": rate_date
    }
    
    return result