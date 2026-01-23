from typing import Dict, Any
from datetime import datetime, timedelta
import pytz
from pytz import timezone as pytz_timezone

def time_server_convert_time(source_timezone: str, target_timezone: str, time: str) -> Dict[str, Any]:
    """
    Convert time between timezones.

    Args:
        source_timezone (str): Source IANA timezone name (e.g., 'America/New_York', 'Europe/London').
                               Use 'UTC' if not provided.
        target_timezone (str): Target IANA timezone name (e.g., 'Asia/Tokyo', 'America/San_Francisco').
                               Use 'UTC' if not provided.
        time (str): Time to convert in 24-hour format (HH:MM)

    Returns:
        Dict containing:
        - source (Dict): contains 'timezone', 'datetime', and 'is_dst' fields for the source time
        - target (Dict): contains 'timezone', 'datetime', and 'is_dst' fields for the converted target time
        - time_difference (str): formatted string indicating the time difference between source and target timezones (e.g., '+9.0h')
    """
    # Set default timezones if not provided
    if not source_timezone:
        source_timezone = 'UTC'
    if not target_timezone:
        target_timezone = 'UTC'

    # Validate time format
    try:
        time_parts = time.split(':')
        if len(time_parts) != 2:
            raise ValueError("Time must be in HH:MM format")
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            raise ValueError("Invalid time values")
    except Exception as e:
        raise ValueError(f"Invalid time format: {str(e)}")

    # Load timezone objects
    try:
        src_tz = pytz_timezone(source_timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Unknown source timezone: {source_timezone}")

    try:
        tgt_tz = pytz_timezone(target_timezone)
    except pytz.exceptions.UnknownTimeZoneError:
        raise ValueError(f"Unknown target timezone: {target_timezone}")

    # Use current date with given time for conversion
    now = datetime.now()
    source_dt = datetime(now.year, now.month, now.day, hour, minute)

    # Localize the source time (handle DST correctly)
    try:
        if hasattr(src_tz, 'localize'):
            source_dt = src_tz.localize(source_dt)
        else:
            source_dt = source_dt.replace(tzinfo=src_tz)
    except Exception as e:
        raise ValueError(f"Could not localize source time: {str(e)}")

    # Convert to target timezone
    try:
        target_dt = source_dt.astimezone(tgt_tz)
    except Exception as e:
        raise ValueError(f"Could not convert to target timezone: {str(e)}")

    # Calculate time difference in hours
    try:
        src_offset = source_dt.utcoffset().total_seconds() / 3600
        tgt_offset = target_dt.utcoffset().total_seconds() / 3600
        diff_hours = tgt_offset - src_offset
    except Exception as e:
        raise ValueError(f"Could not calculate time difference: {str(e)}")

    # Format time difference
    sign = '+' if diff_hours >= 0 else '-'
    time_difference = f"{sign}{abs(diff_hours):.1f}h"

    # Format datetime strings
    source_datetime_str = source_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    target_datetime_str = target_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    return {
        "source": {
            "timezone": source_timezone,
            "datetime": source_datetime_str,
            "is_dst": bool(source_dt.dst())
        },
        "target": {
            "timezone": target_timezone,
            "datetime": target_datetime_str,
            "is_dst": bool(target_dt.dst())
        },
        "time_difference": time_difference
    }