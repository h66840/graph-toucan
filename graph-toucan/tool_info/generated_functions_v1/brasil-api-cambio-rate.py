from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching exchange rate data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - currency (str): Currency symbol (e.g., USD, EUR)
        - date (str): Date of exchange rate in YYYY-MM-DD format
        - quotation_0_time (str): Time of first quotation
        - quotation_0_type (str): Type of first quotation
        - quotation_0_buy_rate (float): Buy rate of first quotation
        - quotation_0_sell_rate (float): Sell rate of first quotation
        - quotation_0_buy_parity (float): Buy parity of first quotation
        - quotation_0_sell_parity (float): Sell parity of first quotation
        - quotation_1_time (str): Time of second quotation
        - quotation_1_type (str): Type of second quotation
        - quotation_1_buy_rate (float): Buy rate of second quotation
        - quotation_1_sell_rate (float): Sell rate of second quotation
        - quotation_1_buy_parity (float): Buy parity of second quotation
        - quotation_1_sell_parity (float): Sell parity of second quotation
    """
    return {
        "currency": "USD",
        "date": "2023-10-05",
        "quotation_0_time": "10:00",
        "quotation_0_type": "commercial",
        "quotation_0_buy_rate": 4.95,
        "quotation_0_sell_rate": 5.05,
        "quotation_0_buy_parity": 1.0,
        "quotation_0_sell_parity": 1.0,
        "quotation_1_time": "14:00",
        "quotation_1_type": "tourism",
        "quotation_1_buy_rate": 4.90,
        "quotation_1_sell_rate": 5.10,
        "quotation_1_buy_parity": 1.0,
        "quotation_1_sell_parity": 1.0,
    }

def brasil_api_cambio_rate(currency: str, date: str) -> Dict[str, Any]:
    """
    Get exchange rates for a specific currency on a specific date.
    
    Args:
        currency (str): Currency symbol (e.g., USD, EUR, GBP)
        date (str): Date in YYYY-MM-DD format. For weekends and holidays, 
                   the returned date will be the last available business day.
    
    Returns:
        Dict containing:
        - currency (str): the currency symbol for which exchange rates are provided
        - date (str): the date of the exchange rate in YYYY-MM-DD format
        - quotations (List[Dict]): list of quotation records with time, type, 
          buy_rate, sell_rate, buy_parity, and sell_parity fields
    
    Raises:
        ValueError: If currency is empty or date is not in valid format
    """
    if not currency:
        raise ValueError("Currency parameter is required")
    
    if not date:
        raise ValueError("Date parameter is required")
    
    # Simulate API call to get data
    api_data = call_external_api("brasil-api-cambio-rate")
    
    # Construct quotations list from flattened API response
    quotations = [
        {
            "time": api_data["quotation_0_time"],
            "type": api_data["quotation_0_type"],
            "buy_rate": api_data["quotation_0_buy_rate"],
            "sell_rate": api_data["quotation_0_sell_rate"],
            "buy_parity": api_data["quotation_0_buy_parity"],
            "sell_parity": api_data["quotation_0_sell_parity"]
        },
        {
            "time": api_data["quotation_1_time"],
            "type": api_data["quotation_1_type"],
            "buy_rate": api_data["quotation_1_buy_rate"],
            "sell_rate": api_data["quotation_1_sell_rate"],
            "buy_parity": api_data["quotation_1_buy_parity"],
            "sell_parity": api_data["quotation_1_sell_parity"]
        }
    ]
    
    # Return structured response matching output schema
    return {
        "currency": currency,
        "date": date,
        "quotations": quotations
    }