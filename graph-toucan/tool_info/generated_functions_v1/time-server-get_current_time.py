from typing import Dict, Any
from datetime import datetime
import pytz


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for getting current time in a specific timezone.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - timezone (str): IANA timezone name for which the time is provided
        - datetime (str): ISO 8601 formatted date and time with timezone offset
        - is_dst (bool): whether Daylight Saving Time is currently in effect
    """
    # Since we cannot make real API calls, simulate realistic response using pytz
    tz = pytz.timezone('UTC')  # Default fallback
    # In real case, this would be based on input, but here we simulate static response
    now = datetime.now(tz)
    is_dst_flag = False
    if hasattr(now.tzinfo, '_dst'):
        is_dst_flag = bool(now.tzinfo._dst(datetime.now()))

    return {
        "timezone": "UTC",
        "datetime": now.isoformat(),
        "is_dst": is_dst_flag
    }


def time_server_get_current_time(timezone: str = "UTC") -> Dict[str, Any]:
    """
    Get current time in a specific timezone.

    Args:
        timezone (str): IANA timezone name (e.g., 'America/New_York', 'Europe/London').
                        Use 'UTC' as default if not provided.

    Returns:
        Dict with the following keys:
        - timezone (str): IANA timezone name for which the time is provided
        - datetime (str): ISO 8601 formatted date and time with timezone offset, e.g. '2025-08-07T00:19:41+02:00'
        - is_dst (bool): whether Daylight Saving Time is currently in effect for the given timezone

    Raises:
        pytz.exceptions.UnknownTimeZoneError: If the provided timezone is invalid.
        ValueError: If timezone is empty or None.
    """
    if not timezone:
        timezone = "UTC"

    try:
        tz = pytz.timezone(timezone)
    except Exception as e:
        raise pytz.exceptions.UnknownTimeZoneError(timezone) from e

    # Get current time in the specified timezone
    now = datetime.now(tz)

    # Check if DST is in effect
    is_dst_flag = False
    if tz.localize(datetime(now.year, 1, 1)).dst() != tz.localize(datetime(now.year, 6, 1)).dst():
        # DST observed in this timezone
        is_dst_flag = bool(now.dst())

    return {
        "timezone": timezone,
        "datetime": now.isoformat(),
        "is_dst": is_dst_flag
    }