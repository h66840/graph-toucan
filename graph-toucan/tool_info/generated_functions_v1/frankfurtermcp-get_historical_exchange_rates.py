from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching historical exchange rate data from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - amount (float): the base amount for which exchange rates are calculated
        - base (str): the base currency code used for the exchange rate calculation
        - date (str): the specific date for which exchange rates are provided
        - start_date (str): the start date of the date range for historical rates
        - end_date (str): the end date of the date range for historical rates
        - rates_2023_12_01_usd (float): USD rate on 2023-12-01
        - rates_2023_12_01_eur (float): EUR rate on 2023-12-01
        - rates_2023_12_02_usd (float): USD rate on 2023-12-02
        - rates_2023_12_02_eur (float): EUR rate on 2023-12-02
    """
    return {
        "amount": 1.0,
        "base": "EUR",
        "date": "2023-12-01",
        "start_date": "2023-12-01",
        "end_date": "2023-12-02",
        "rates_2023_12_01_usd": 1.10,
        "rates_2023_12_01_eur": 1.00,
        "rates_2023_12_02_usd": 1.11,
        "rates_2023_12_02_eur": 1.00
    }

def frankfurtermcp_get_historical_exchange_rates(
    base_currency: str,
    end_date: Optional[str] = None,
    specific_date: Optional[str] = None,
    start_date: Optional[str] = None,
    symbols: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Returns historical exchange rates for a specific date or date range.
    
    If the exchange rates for a specified date are not available, the rates available 
    for the closest date before the specified date will be provided.
    Either a specific date, a start date, or a date range must be provided.
    The symbols can be used to filter the results to specific currencies.
    If symbols are not provided, all supported currencies will be returned.
    
    Args:
        base_currency (str): A base currency code for which rates are to be requested.
        end_date (Optional[str]): The end date of a date range in YYYY-MM-DD format.
        specific_date (Optional[str]): The specific date for which rates are requested in YYYY-MM-DD format.
        start_date (Optional[str]): The start date of a date range in YYYY-MM-DD format.
        symbols (Optional[List[str]]): List of target currency codes to filter results.
    
    Returns:
        Dict containing:
        - amount (float): the base amount for which exchange rates are calculated
        - base (str): the base currency code
        - date (str): the specific date (if single date requested)
        - start_date (str): the start date of range (if range requested)
        - end_date (str): the end date of range (if range requested)
        - rates (Dict): mapping of dates to currency rate objects
    
    Raises:
        ValueError: If required parameters are missing or dates are invalid
    """
    # Input validation
    if not base_currency:
        raise ValueError("base_currency is required")
    
    # Validate date format and logic
    def validate_date(date_str: Optional[str], label: str) -> None:
        if date_str is None:
            return
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid {label} format: {date_str}. Expected YYYY-MM-DD")
    
    validate_date(specific_date, "specific_date")
    validate_date(start_date, "start_date")
    validate_date(end_date, "end_date")
    
    # Check that at least one date parameter is provided
    if not any([specific_date, start_date, end_date]):
        raise ValueError("Either specific_date, start_date, or end_date must be provided")
    
    # If specific_date is provided, ignore range parameters
    if specific_date:
        start_date = specific_date
        end_date = specific_date
    
    # If only start_date provided, set end_date to start_date
    if start_date and not end_date:
        end_date = start_date
    
    # If only end_date provided, set start_date to end_date
    if end_date and not start_date:
        start_date = end_date
    
    # Ensure start_date <= end_date
    if start_date and end_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if start_dt > end_dt:
            raise ValueError("start_date cannot be after end_date")
    
    # Call external API to get data
    api_data = call_external_api("frankfurtermcp-get_historical_exchange_rates")
    
    # Default symbols if not provided
    target_symbols = symbols or ["USD", "EUR"]
    
    # Construct the rates structure
    rates = {}
    
    # Determine dates to include
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Generate rates for each date in range
    while current_date <= end_dt:
        date_str = current_date.strftime("%Y-%m-%d")
        date_key = date_str.replace("-", "_")
        
        date_rates = {}
        for symbol in target_symbols:
            # Create a predictable rate based on date and symbol
            # Base rate increases slightly each day, with variation by symbol
            base_rate = 1.0 if symbol == base_currency else 1.10
            day_offset = (current_date - datetime(2023, 12, 1)).days
            symbol_factor = 1.0 + (ord(symbol[0]) % 10) * 0.01
            rate = round(base_rate + (day_offset * 0.01) * symbol_factor, 6)
            
            # Use API data if available for this date and symbol
            api_rate_key = f"rates_{date_key}_{symbol.lower()}"
            if api_rate_key in api_data:
                rate = api_data[api_rate_key]
                
            date_rates[symbol] = rate
        
        rates[date_str] = date_rates
        current_date += timedelta(days=1)
    
    # Construct result
    result: Dict[str, Any] = {
        "amount": float(api_data.get("amount", 1.0)),
        "base": base_currency,
        "rates": rates
    }
    
    # Add date fields based on request type
    if specific_date or (start_date == end_date):
        result["date"] = start_date
    else:
        result["start_date"] = start_date
        result["end_date"] = end_date
    
    return result