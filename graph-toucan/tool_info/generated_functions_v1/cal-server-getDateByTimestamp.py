from typing import Dict, Any
from datetime import datetime

def cal_server_getDateByTimestamp(ts: float) -> Dict[str, str]:
    """
    Convert the provided Unix timestamp to a formatted date and time string.
    
    Args:
        ts (float): Unix timestamp (number of seconds since January 1, 1970).
        
    Returns:
        Dict[str, str]: A dictionary containing:
            - date (str): The calendar date in MM/DD/YYYY format.
            - time (str): The time in 12-hour format with AM/PM (e.g., 10:40:02 AM).
            
    Raises:
        ValueError: If the timestamp is negative or otherwise invalid.
    """
    if not isinstance(ts, (int, float)) or ts < 0:
        raise ValueError("Timestamp must be a non-negative number.")
    
    # Convert timestamp to datetime object
    dt = datetime.fromtimestamp(ts)
    
    # Format date as MM/DD/YYYY
    date_str = dt.strftime("%m/%d/%Y")
    
    # Format time as 12-hour with AM/PM
    time_str = dt.strftime("%I:%M:%S %p")
    
    return {
        "date": date_str,
        "time": time_str
    }