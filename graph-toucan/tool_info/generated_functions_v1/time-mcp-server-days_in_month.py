from typing import Dict, Any, Optional
from datetime import datetime
import calendar

def time_mcp_server_days_in_month(date: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the number of days in a month. If no date is provided, returns the number of days in the current month.
    
    Args:
        date (Optional[str]): The date to get the days in month. Format: YYYY-MM-DD. If None, uses current date.
    
    Returns:
        Dict[str, Any]: A dictionary containing the number of days in the specified or current month.
            - days_in_month (int): The number of days in the specified or current month.
    
    Raises:
        ValueError: If the provided date string is not in the correct format (YYYY-MM-DD).
    """
    try:
        if date is None:
            today = datetime.now()
            year = today.year
            month = today.month
        else:
            try:
                parsed_date = datetime.strptime(date, "%Y-%m-%d")
                year = parsed_date.year
                month = parsed_date.month
            except ValueError as e:
                raise ValueError(f"Invalid date format: {date}. Expected format: YYYY-MM-DD") from e
        
        # Get the number of days in the given month and year
        days_in_month = calendar.monthrange(year, month)[1]
        
        return {
            "days_in_month": days_in_month
        }
    
    except Exception as e:
        raise e