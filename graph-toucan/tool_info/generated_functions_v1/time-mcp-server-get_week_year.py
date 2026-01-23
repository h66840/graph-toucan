from typing import Dict, Any, Optional
from datetime import datetime

def time_mcp_server_get_week_year(date: Optional[str] = None) -> Dict[str, int]:
    """
    Get the week and ISO week of the year for a given date.
    
    If no date is provided, the current date is used.
    
    Args:
        date (Optional[str]): The date in 'YYYY-MM-DD' format. If None, uses current date.
        
    Returns:
        Dict[str, int]: A dictionary containing:
            - week_of_year (int): The week number of the year (standard calendar week numbering)
            - iso_week_of_year (int): The ISO 8601 week number of the year
            
    Raises:
        ValueError: If the provided date string is not in valid 'YYYY-MM-DD' format
    """
    # Use current date if no date is provided
    if date is None:
        target_date = datetime.now().date()
    else:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError(f"Invalid date format: {date}. Expected format: YYYY-MM-DD") from e
    
    # Calculate standard week of year (1-53)
    # Week 1 starts on January 1st, regardless of the day of the week
    jan1 = datetime(target_date.year, 1, 1).date()
    week_of_year = (target_date - jan1).days // 7 + 1
    
    # Calculate ISO week of year (1-53)
    # ISO week starts on Monday, week 1 is the first week with at least 4 days in the new year
    iso_year, iso_week, iso_weekday = target_date.isocalendar()
    
    return {
        "week_of_year": week_of_year,
        "iso_week_of_year": iso_week
    }