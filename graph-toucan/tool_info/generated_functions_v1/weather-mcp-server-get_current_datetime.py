from typing import Dict, Any
from datetime import datetime, timezone
import zoneinfo


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - timezone (str): IANA timezone name
        - datetime (str): ISO 8601 formatted date and time with timezone offset
    """
    # Since we cannot make real API calls, we simulate current time in UTC
    # and use the provided timezone name from input (passed via tool_name context)
    # However, tool_name is not used here since we need to generate based on input
    # This function will be called with fixed tool name, so we return placeholder
    # values that will be overridden by actual logic in main function.
    # Returning dummy values to satisfy structure; actual values are computed.
    return {
        "timezone": "UTC",
        "datetime": "2025-08-06T01:05:21+00:00"
    }


def weather_mcp_server_get_current_datetime(timezone_name: str) -> Dict[str, str]:
    """
    Get current time in specified timezone.

    Args:
        timezone_name (str): IANA timezone name (e.g., 'America/New_York', 'Europe/London').
                             Use UTC if not provided.

    Returns:
        Dict containing:
            - timezone (str): IANA timezone name
            - datetime (str): ISO 8601 formatted date and time with timezone offset

    Raises:
        ValueError: If the provided timezone_name is not a valid IANA timezone.
    """
    if not timezone_name:
        timezone_name = "UTC"

    try:
        tz = zoneinfo.ZoneInfo(timezone_name)
    except zoneinfo.ZoneInfoKeyError:
        raise ValueError(f"Invalid timezone name: {timezone_name}")

    now = datetime.now(tz)
    iso_datetime = now.isoformat()

    return {
        "timezone": timezone_name,
        "datetime": iso_datetime
    }