from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for currency conversion.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - converted_amount (float): The amount after conversion to the target currency
        - exchange_rate (float): The exchange rate used for converting from the source to the target currency
        - from_currency (str): The currency code of the original amount (e.g., "EUR")
        - to_currency (str): The currency code of the target currency (e.g., "USD")
        - original_amount (float): The original amount provided before conversion
    """
    return {
        "converted_amount": 1.18,
        "exchange_rate": 1.18,
        "from_currency": "EUR",
        "to_currency": "USD",
        "original_amount": 1.0
    }

def currency_converter_mcp_convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
    """
    Converts an amount from one currency to another using a simulated exchange rate.
    
    This function simulates a currency conversion by using a fixed exchange rate
    based on the currency pair. The actual conversion logic is simplified and does
    not use real-time exchange rates.
    
    Args:
        amount (float): The amount to convert (must be non-negative)
        from_currency (str): The source currency code (e.g., "EUR")
        to_currency (str): The target currency code (e.g., "USD")
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - converted_amount (float): The amount after conversion to the target currency
            - exchange_rate (float): The exchange rate used for converting from the source to the target currency
            - from_currency (str): The currency code of the original amount
            - to_currency (str): The currency code of the target currency
            - original_amount (float): The original amount provided before conversion
    
    Raises:
        ValueError: If amount is negative or if from_currency equals to_currency
    """
    # Input validation
    if amount < 0:
        raise ValueError("Amount must be non-negative")
    
    if from_currency == to_currency:
        raise ValueError("Source and target currencies must be different")
    
    # Call external API to get conversion data (simulated)
    api_data = call_external_api("currency-converter-mcp-convert_currency")
    
    # Determine exchange rate based on currency pair (simplified logic)
    exchange_rate = 1.0
    if from_currency == "EUR" and to_currency == "USD":
        exchange_rate = 1.18
    elif from_currency == "USD" and to_currency == "EUR":
        exchange_rate = 0.85
    elif from_currency == "USD" and to_currency == "JPY":
        exchange_rate = 110.0
    elif from_currency == "JPY" and to_currency == "USD":
        exchange_rate = 0.0091
    elif from_currency == "EUR" and to_currency == "GBP":
        exchange_rate = 0.86
    elif from_currency == "GBP" and to_currency == "EUR":
        exchange_rate = 1.16
    else:
        # Default fallback rate for any other currency pair
        exchange_rate = 1.18
    
    # Calculate converted amount
    converted_amount = amount * exchange_rate
    
    # Construct result dictionary matching output schema
    result = {
        "converted_amount": float(round(converted_amount, 2)),
        "exchange_rate": float(exchange_rate),
        "from_currency": from_currency,
        "to_currency": to_currency,
        "original_amount": float(amount)
    }
    
    return result