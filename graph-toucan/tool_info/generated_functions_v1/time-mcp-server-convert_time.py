from typing import Dict, Any
from datetime import datetime
import pytz

def time_mcp_server_convert_time(sourceTimezone: str, targetTimezone: str, time: str) -> Dict[str, Any]:
    """
    Convert time between timezones.

    Args:
        sourceTimezone (str): The source timezone. IANA timezone name, e.g. Asia/Shanghai
        targetTimezone (str): The target timezone. IANA timezone name, e.g. Europe/London
        time (str): Date and time in 24-hour format. e.g. 2025-03-23 12:30:00

    Returns:
        Dict[str, Any]: A dictionary containing:
            - source_time (str): the date and time in the source timezone in "YYYY-MM-DD HH:MM:SS" format
            - target_time (str): the converted date and time in the target timezone in "YYYY-MM-DD HH:MM:SS" format
            - source_timezone (str): the IANA timezone name of the source location
            - target_timezone (str): the IANA timezone name of the target location
            - time_difference_hours (int): the time difference in hours between the source and target timezones
    """
    try:
        # Validate inputs
        if not sourceTimezone or not targetTimezone or not time:
            raise ValueError("All parameters are required")

        # Parse the input time string
        try:
            naive_dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            raise ValueError(f"Invalid time format: {e}")

        # Get timezone objects
        try:
            source_tz = pytz.timezone(sourceTimezone)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Unknown source timezone: {sourceTimezone}")

        try:
            target_tz = pytz.timezone(targetTimezone)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Unknown target timezone: {targetTimezone}")

        # Localize the source time (handle DST automatically)
        source_dt = source_tz.localize(naive_dt)
        
        # Convert to target timezone
        target_dt = source_dt.astimezone(target_tz)

        # Format the output times
        source_time_str = source_dt.strftime("%Y-%m-%d %H:%M:%S")
        target_time_str = target_dt.strftime("%Y-%m-%d %H:%M:%S")

        # Calculate time difference in hours
        time_difference = target_dt.utcoffset() - source_dt.utcoffset()
        time_difference_hours = int(time_difference.total_seconds() // 3600)

        return {
            "source_time": source_time_str,
            "target_time": target_time_str,
            "source_timezone": sourceTimezone,
            "target_timezone": targetTimezone,
            "time_difference_hours": time_difference_hours
        }

    except Exception as e:
        return {
            "source_time": "",
            "target_time": "",
            "source_timezone": sourceTimezone,
            "target_timezone": targetTimezone,
            "time_difference_hours": 0,
            "error": str(e)
        }