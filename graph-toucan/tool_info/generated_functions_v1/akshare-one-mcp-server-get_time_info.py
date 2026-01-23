from typing import Dict, Any
from datetime import datetime, timedelta
import pytz

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching time-related data from external API.
    
    Returns:
        Dict with simple fields only (str, float):
        - iso_format (str): ISO 8601 formatted current time with timezone offset
        - timestamp (float): Unix timestamp representing the current time with microsecond precision
        - last_trading_day (str): the most recent trading day in YYYY-MM-DD format
    """
    # Use a fixed reference time for consistency
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    iso_format = now.isoformat()
    timestamp = now.timestamp()
    
    # Calculate last trading day (Monday-Friday, excluding today if not a trading day)
    last_trading_day = now
    if now.weekday() == 5:  # Saturday
        last_trading_day = now - timedelta(days=1)
    elif now.weekday() == 6:  # Sunday
        last_trading_day = now - timedelta(days=2)
    elif now.weekday() == 0 and now.hour < 9:  # Monday before market open
        last_trading_day = now - timedelta(days=3)
    elif now.weekday() > 0 and now.weekday() < 5 and now.hour < 9:  # Tue-Fri before market open
        last_trading_day = now - timedelta(days=1)
    elif now.weekday() == 5 and now.hour >= 9:  # Saturday during market hours (unlikely)
        last_trading_day = now - timedelta(days=1)
    elif now.weekday() == 6 and now.hour >= 9:  # Sunday during market hours (unlikely)
        last_trading_day = now - timedelta(days=2)
    
    # Adjust if today is not a trading day and we need to go back further
    while last_trading_day.weekday() >= 5:  # Weekend
        last_trading_day = last_trading_day - timedelta(days=1)
    
    last_trading_day_str = last_trading_day.strftime('%Y-%m-%d')
    
    return {
        "iso_format": iso_format,
        "timestamp": timestamp,
        "last_trading_day": last_trading_day_str
    }

def akshare_one_mcp_server_get_time_info() -> Dict[str, Any]:
    """
    Get current time with ISO format, timestamp, and the last trading day.
    
    This function retrieves the current time information including ISO 8601 formatted
    time with timezone offset, Unix timestamp with microsecond precision, and the
    most recent trading day in YYYY-MM-DD format (considering financial markets,
    which operate on weekdays only).
    
    Returns:
        Dict containing:
        - iso_format (str): ISO 8601 formatted current time with timezone offset
        - timestamp (float): Unix timestamp representing the current time with microsecond precision
        - last_trading_day (str): the most recent trading day in YYYY-MM-DD format
    """
    try:
        # Call external API to get time data
        api_data = call_external_api("akshare-one-mcp-server-get_time_info")
        
        # Construct result matching output schema
        result = {
            "iso_format": api_data["iso_format"],
            "timestamp": api_data["timestamp"],
            "last_trading_day": api_data["last_trading_day"]
        }
        
        return result
        
    except Exception as e:
        # In case of any error, return a fallback response
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        fallback_trading_day = now.strftime('%Y-%m-%d')
        
        # Adjust fallback trading day if needed
        if now.weekday() >= 5:  # Weekend
            days_to_subtract = now.weekday() - 4
            fallback_trading_day = (now - timedelta(days=days_to_subtract)).strftime('%Y-%m-%d')
            
        return {
            "iso_format": now.isoformat(),
            "timestamp": now.timestamp(),
            "last_trading_day": fallback_trading_day
        }