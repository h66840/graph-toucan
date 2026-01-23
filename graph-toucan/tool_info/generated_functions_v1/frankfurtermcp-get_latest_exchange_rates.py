from typing import Dict, Any, Optional, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for exchange rates.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - amount (float): the base amount for which exchange rates are calculated
        - base (str): the base currency code
        - date (str): the date of the exchange rates in YYYY-MM-DD format
        - rate_0_currency (str): first target currency code
        - rate_0_value (float): exchange rate value for first currency
        - rate_1_currency (str): second target currency code
        - rate_1_value (float): exchange rate value for second currency
    """
    return {
        "amount": 1.0,
        "base": "USD",
        "date": "2023-10-05",
        "rate_0_currency": "EUR",
        "rate_0_value": 0.92,
        "rate_1_currency": "CAD",
        "rate_1_value": 1.35
    }

def frankfurtermcp_get_latest_exchange_rates(base_currency: str, symbols: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Returns the latest exchange rates for specific currencies relative to a base currency.
    
    Args:
        base_currency (str): A base currency code for which rates are to be requested.
        symbols (Optional[List[str]]): A list of target currency codes for which rates 
            against the base currency will be provided. If not provided, all supported 
            currencies will be returned.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - amount (float): the base amount for which exchange rates are calculated
            - base (str): the base currency code
            - date (str): the date of the exchange rates in YYYY-MM-DD format
            - rates (Dict[str, float]): mapping of target currency codes to their exchange rates
    
    Raises:
        ValueError: If base_currency is empty or not a valid string
    """
    if not base_currency or not isinstance(base_currency, str):
        raise ValueError("base_currency must be a non-empty string")
    
    # Call external API to get exchange rate data
    api_data = call_external_api("frankfurtermcp-get_latest_exchange_rates")
    
    # Override base currency with input parameter
    base = base_currency.upper()
    
    # Construct rates dictionary from flattened API response
    rates = {}
    for i in range(2):  # We have two rate entries from the mock API
        currency_key = f"rate_{i}_currency"
        value_key = f"rate_{i}_value"
        if currency_key in api_data and value_key in api_data:
            currency = api_data[currency_key]
            value = api_data[value_key]
            # Apply filtering if symbols are provided
            if symbols is None or currency in symbols:
                rates[currency] = value
    
    # Construct final result matching output schema
    result = {
        "amount": api_data["amount"],
        "base": base,
        "date": api_data["date"],
        "rates": rates
    }
    
    return result