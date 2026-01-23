from typing import List, Dict, Any
from datetime import datetime

def cal_server_batchGetDateByTimestamp(tsList: List[int]) -> Dict[str, Any]:
    """
    Batch convert the provided list of timestamps to date format.
    
    This function takes a list of Unix timestamps and converts each timestamp
    into a human-readable date-time string in the format "M/D/YYYY, H:MM:SS AM/PM".
    
    Args:
        tsList (List[int]): A list of Unix timestamps (in seconds) to be converted.
        
    Returns:
        Dict[str, Any]: A dictionary containing:
            - dates (List[str]): List of formatted date-time strings corresponding to each input timestamp.
            
    Raises:
        ValueError: If any timestamp is invalid or out of range.
    """
    dates = []
    
    for ts in tsList:
        try:
            # Convert timestamp to datetime object
            dt = datetime.fromtimestamp(ts)
            # Format datetime as "M/D/YYYY, H:MM:SS AM/PM"
            formatted_date = dt.strftime("%-m/%-d/%Y, %-I:%M:%S %p")
            dates.append(formatted_date)
        except (OSError, ValueError, OverflowError) as e:
            raise ValueError(f"Invalid timestamp: {ts}") from e
    
    return {"dates": dates}