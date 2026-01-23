from typing import Dict, Any

def time_server_readableTime(timestamp: float) -> Dict[str, Any]:
    """
    Convert a Unix timestamp to a human-readable date and time string.
    
    Args:
        timestamp (float): A Unix timestamp (seconds since epoch) to convert.
            Can be obtained from the getTime() function.
            
    Returns:
        Dict[str, Any]: A dictionary containing:
            - readable_time (str): full human-readable date and time string in the format "Weekday, Day Month Year Hour:Minute:Second"
            - weekday (str): name of the weekday
            - day (int): day of the month as a number
            - month (str): full name of the month
            - year (int): four-digit year
            - hour (int): hour in 24-hour format (0–23)
            - minute (int): minute (0–59)
            - second (int): second (0–59)
            - timestamp_input (float): the Unix timestamp provided as input
    """
    import datetime
    
    # Input validation
    if not isinstance(timestamp, (int, float)):
        raise TypeError("Timestamp must be a number")
    if timestamp < 0:
        raise ValueError("Timestamp cannot be negative")
    
    try:
        # Convert timestamp to datetime object
        dt = datetime.datetime.fromtimestamp(timestamp)
        
        # Extract components
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                        "Friday", "Saturday", "Sunday"]
        month_names = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
        
        weekday = weekday_names[dt.weekday()]
        day = dt.day
        month = month_names[dt.month - 1]
        year = dt.year
        hour = dt.hour
        minute = dt.minute
        second = dt.second
        
        # Format the readable time string
        readable_time = f"{weekday}, {day} {month} {year} {hour:02d}:{minute:02d}:{second:02d}"
        
        return {
            "readable_time": readable_time,
            "weekday": weekday,
            "day": day,
            "month": month,
            "year": year,
            "hour": hour,
            "minute": minute,
            "second": second,
            "timestamp_input": float(timestamp)
        }
        
    except Exception as e:
        raise ValueError(f"Failed to convert timestamp: {str(e)}")