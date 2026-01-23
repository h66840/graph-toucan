from typing import Dict, Any
from datetime import datetime

def time_mcp_server_relative_time(time: str) -> Dict[str, str]:
    """
    Get the relative time from now.
    
    Args:
        time (str): The time to get the relative time from now. Format: YYYY-MM-DD HH:mm:ss
    
    Returns:
        Dict[str, str]: A dictionary containing the relative time expression from the current moment.
                       Example: {"relative_time": "in 2 hours"}
    
    Raises:
        ValueError: If the time string is not in the correct format or represents an invalid date/time.
    """
    try:
        # Parse the input time string
        given_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        
        # Calculate the difference
        diff = given_time - now
        total_seconds = int(diff.total_seconds())
        
        # Determine if the time is in the past or future
        suffix = "ago" if total_seconds < 0 else "in"
        total_seconds = abs(total_seconds)
        
        # Calculate time components
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        
        # Build relative time string
        if days > 0:
            value = days
            unit = "day" if value == 1 else "days"
        elif hours > 0:
            value = hours
            unit = "hour" if value == 1 else "hours"
        elif minutes > 0:
            value = minutes
            unit = "minute" if value == 1 else "minutes"
        else:
            value = seconds
            unit = "second" if value == 1 else "seconds"
        
        relative_time = f"{suffix} {value} {unit}"
        
        return {"relative_time": relative_time}
        
    except ValueError as e:
        raise ValueError(f"Invalid time format or value: {e}")