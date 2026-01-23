from typing import Dict, Any, Optional
from datetime import datetime, timezone
import re
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching option contract data from an external cryptocurrency exchange API via CCXT.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - ticker_data_symbol (str): Contract symbol
        - ticker_data_timestamp (int): Unix timestamp in milliseconds
        - ticker_data_datetime (str): ISO 8601 datetime string
        - ticker_data_last (float): Last traded price
        - ticker_data_bid (float): Best bid price
        - ticker_data_ask (float): Best ask price
        - ticker_data_high (float): 24h high price
        - ticker_data_low (float): 24h low price
        - ticker_data_baseVolume (float): Base currency volume
        - ticker_data_quoteVolume (float): Quote currency volume
        - ticker_data_openInterest (float): Open interest in contracts
        - underlying_asset (str): Underlying asset (e.g., BTC)
        - strike_price (float): Strike price of the option
        - contract_type (str): 'call' or 'put'
        - expiry_date (str): Expiration date in ISO 8601 format
        - time_to_expiration (float): Time to expiry in fractional days
        - mark_price (float): Current mark/fair price
        - index_price (float): Index price of underlying
        - implied_volatility (float): Implied volatility (e.g., 0.85 for 85%)
        - funding_rate (float): Funding rate if applicable
        - exchange_info_rateLimit (bool): Whether rate limiting is active
        - exchange_info_success (bool): Whether request was successful
        - exchange_info_responseTimeMs (int): Response time in milliseconds
        - raw_response_json (str): JSON string of raw response
    """
    now = datetime.now(timezone.utc)
    expiry = now.replace(year=2025, month=6, day=27, hour=8, minute=0, second=0, microsecond=0)
    time_diff_days = (expiry - now).total_seconds() / (24 * 3600)

    # Generate synthetic but realistic values
    spot_price = 60000.0 + random.uniform(-5000, 5000)
    strike_price = round(random.choice([spot_price * 0.8, spot_price, spot_price * 1.2]), -3)
    contract_type = random.choice(['call', 'put'])
    mark_price = abs((spot_price - strike_price) * (0.5 + random.uniform(-0.2, 0.3))) + random.uniform(100, 500)
    implied_vol = round(random.uniform(0.5, 1.5), 4)
    index_price = spot_price * (1 + random.uniform(-0.005, 0.005))

    return {
        "ticker_data_symbol": "BTC-27JUN25-60000-C",
        "ticker_data_timestamp": int(now.timestamp() * 1000),
        "ticker_data_datetime": now.isoformat().replace('+00:00', 'Z'),
        "ticker_data_last": round(mark_price * (1 + random.uniform(-0.02, 0.02)), 2),
        "ticker_data_bid": round(mark_price * 0.99, 2),
        "ticker_data_ask": round(mark_price * 1.01, 2),
        "ticker_data_high": round(mark_price * 1.05, 2),
        "ticker_data_low": round(mark_price * 0.95, 2),
        "ticker_data_baseVolume": round(random.uniform(100, 1000), 2),
        "ticker_data_quoteVolume": round(random.uniform(5000000, 50000000), 2),
        "ticker_data_openInterest": round(random.uniform(500, 5000), 2),
        "underlying_asset": "BTC",
        "strike_price": strike_price,
        "contract_type": contract_type,
        "expiry_date": expiry.isoformat().replace('+00:00', 'Z'),
        "time_to_expiration": round(time_diff_days, 4),
        "mark_price": round(mark_price, 4),
        "index_price": round(index_price, 2),
        "implied_volatility": implied_vol,
        "funding_rate": round(random.uniform(-0.001, 0.001), 6) if random.random() > 0.5 else 0.0,
        "exchange_info_rateLimit": False,
        "exchange_info_success": True,
        "exchange_info_responseTimeMs": random.randint(20, 200),
        "raw_response_json": f'{{"symbol":"BTC-27JUN25-60000-C","last":{round(mark_price, 2)},"bid":{round(mark_price * 0.99, 2)},"ask":{round(mark_price * 1.01, 2)},"openInterest":{round(random.uniform(500, 5000), 2)}}}'
    }

def ccxt_cryptocurrency_exchange_server_fetch_option_contract_data(
    exchange_id: str,
    symbol: str,
    api_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    passphrase: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Fetches market data for a specific options contract from a cryptocurrency exchange using CCXT.
    
    This function simulates interaction with a cryptocurrency exchange to retrieve ticker data
    and metadata for a given options contract. It parses the symbol to extract strike price,
    contract type, and expiry, and returns enriched data including derived fields.
    
    Args:
        exchange_id (str): The ID of the exchange that supports options trading (e.g., 'deribit', 'okx').
        symbol (str): The specific option contract symbol (e.g., 'BTC-28JUN24-70000-C').
        api_key (Optional[str]): Optional API key for authentication.
        secret_key (Optional[str]): Optional secret key for authentication.
        passphrase (Optional[str]): Optional passphrase required by some exchanges.
        params (Optional[Dict[str, Any]]): Optional parameters for client setup and API calls.
    
    Returns:
        Dict containing the following keys:
        - ticker_data (Dict): Standard ticker information (price, volume, bid/ask, etc.)
        - underlying_asset (str): The underlying cryptocurrency (e.g., 'BTC')
        - strike_price (float): The strike price of the option
        - contract_type (str): 'call' or 'put'
        - expiry_date (str): Expiration date in ISO 8601 format
        - time_to_expiration (float): Time remaining until expiration in days (fractional)
        - mark_price (float): Current fair/marked price of the option
        - index_price (float): Current price of the underlying index
        - implied_volatility (float): Implied volatility percentage
        - funding_rate (float): Current funding rate if applicable
        - exchange_info (Dict): Metadata about the exchange response
        - raw_response (Dict): Original unmodified JSON response
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not exchange_id:
        raise ValueError("exchange_id is required")
    if not symbol:
        raise ValueError("symbol is required")
    
    # Extract underlying asset from symbol using common patterns
    underlying_asset = "BTC"  # default fallback
    strike_price = 70000.0
    contract_type = "call"
    expiry_date = datetime.now(timezone.utc).replace(year=2024, month=12, day=25, hour=0, minute=0, second=0, microsecond=0).isoformat().replace('+00:00', 'Z')
    
    # Try to parse symbol (e.g., BTC-28JUN24-70000-C)
    match = re.match(r'^([A-Z]+)-(\d{2}[A-Z]{3}\d{2,4})-(\d+)-([CP])', symbol)
    if match:
        underlying_asset = match.group(1)
        expiry_str = match.group(2)
        strike_price = float(match.group(3))
        contract_type = 'call' if match.group(4) == 'C' else 'put'
        
        # Parse expiry string (e.g., 28JUN24)
        try:
            expiry_day = int(expiry_str[:2])
            month_abbr = expiry_str[2:5]
            year_suffix = expiry_str[5:]
            month_map = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
                       'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
            expiry_month = month_map[month_abbr]
            if len(year_suffix) == 2:
                expiry_year = 2000 + int(year_suffix)
            else:
                expiry_year = int(year_suffix)
            
            parsed_expiry = datetime(year=expiry_year, month=expiry_month, day=expiry_day,
                                   hour=8, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
            expiry_date = parsed_expiry.isoformat()
        except (KeyError, ValueError) as e:
            # If parsing fails, keep default expiry_date
            pass
    
    # Simulate API call
    raw_data = call_external_api("fetchTicker")
    
    # Extract and transform data
    ticker_data = {
        "symbol": raw_data["ticker_data_symbol"],
        "timestamp": raw_data["ticker_data_timestamp"],
        "datetime": raw_data["ticker_data_datetime"],
        "last": raw_data["ticker_data_last"],
        "bid": raw_data["ticker_data_bid"],
        "ask": raw_data["ticker_data_ask"],
        "high": raw_data["ticker_data_high"],
        "low": raw_data["ticker_data_low"],
        "baseVolume": raw_data["ticker_data_baseVolume"],
        "quoteVolume": raw_data["ticker_data_quoteVolume"],
        "openInterest": raw_data["ticker_data_openInterest"]
    }
    
    result = {
        "ticker_data": ticker_data,
        "underlying_asset": underlying_asset,
        "strike_price": strike_price,
        "contract_type": contract_type,
        "expiry_date": expiry_date,
        "time_to_expiration": raw_data["time_to_expiration"],
        "mark_price": raw_data["mark_price"],
        "index_price": raw_data["index_price"],
        "implied_volatility": raw_data["implied_volatility"],
        "funding_rate": raw_data["funding_rate"],
        "exchange_info": {
            "rateLimit": raw_data["exchange_info_rateLimit"],
            "success": raw_data["exchange_info_success"],
            "responseTimeMs": raw_data["exchange_info_responseTimeMs"]
        },
        "raw_response": raw_data["raw_response_json"]
    }
    
    return result