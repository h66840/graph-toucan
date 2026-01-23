from typing import Dict, Any
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching currency conversion data from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - from_currency (str): Source currency code (e.g., "USD")
        - to_currency (str): Target currency code (e.g., "EUR")
        - amount (float): Original amount in the source currency
        - converted_amount (float): Resulting amount in the target currency
        - exchange_rate (float): Exchange rate used for conversion (target per source)
        - rate_date (str): Date of the exchange rate in YYYY-MM-DD format
    """
    return {
        "from_currency": "USD",
        "to_currency": "EUR",
        "amount": 100.0,
        "converted_amount": 92.5,
        "exchange_rate": 0.925,
        "rate_date": "2023-10-05"
    }

def frankfurtermcp_convert_currency_latest(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """
    Converts an amount from one currency to another using the latest exchange rates.
    
    This function simulates a currency conversion by calling an external API to get
    the current exchange rate and then applying it to the provided amount.
    
    Args:
        amount (float): The amount in the source currency to convert.
        from_currency (str): The source currency code (e.g., "USD").
        to_currency (str): The target currency code (e.g., "EUR").
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - from_currency (str): Source currency code
            - to_currency (str): Target currency code
            - amount (float): Original amount in source currency
            - converted_amount (float): Converted amount in target currency
            - exchange_rate (float): Exchange rate used (target per source)
            - rate_date (str): Date of the exchange rate in YYYY-MM-DD format
    
    Raises:
        ValueError: If amount is negative or currencies are not provided.
    """
    # Input validation
    if amount < 0:
        raise ValueError("Amount must be non-negative")
    if not from_currency or not to_currency:
        raise ValueError("Both from_currency and to_currency must be provided")
    
    # Get exchange rate data from external API
    api_data = call_external_api("frankfurtermcp-convert_currency_latest")
    
    # Construct result using the API data, but override with input parameters
    # For simulation purposes, we'll calculate a realistic converted amount
    # based on the input currencies and a deterministic exchange rate
    
    # Generate a deterministic exchange rate based on currency codes
    currency_pairs = {
        ("USD", "EUR"): 0.925,
        ("EUR", "USD"): 1.081,
        ("USD", "GBP"): 0.78,
        ("GBP", "USD"): 1.28,
        ("EUR", "GBP"): 0.84,
        ("GBP", "EUR"): 1.19,
    }
    
    # Default rate if pair not in map
    exchange_rate = currency_pairs.get((from_currency, to_currency), 1.0)
    
    # Calculate converted amount
    converted_amount = amount * exchange_rate
    
    # Use current date as rate date
    rate_date = datetime.now().strftime("%Y-%m-%d")
    
    result = {
        "from_currency": from_currency,
        "to_currency": to_currency,
        "amount": float(amount),
        "converted_amount": round(converted_amount, 2),
        "exchange_rate": round(exchange_rate, 4),
        "rate_date": rate_date
    }
    
    return result