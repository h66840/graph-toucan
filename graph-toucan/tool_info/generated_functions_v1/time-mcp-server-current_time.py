from typing import Dict, Any, Optional
from datetime import datetime
import pytz
from typing import Dict, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for current time.

    Returns:
        Dict with simple fields only (str):
        - current_time (str): The current date or datetime string in the requested format
        - timezone (str): The timezone for which the time is provided, if specified
    """
    # Simulated response with placeholder values
    return {
        "current_time": "2023-10-05 14:30:45",
        "timezone": "Asia/Shanghai"
    }


def time_mcp_server_current_time(format: str = "", timezone: Optional[str] = None) -> Dict[str, str]:
    """
    Get the current date and time in the specified format and timezone.

    Args:
        format (str): The format of the time (required, default is empty string).
                      If empty, defaults to ISO format.
        timezone (Optional[str]): The IANA timezone name (e.g., 'Asia/Shanghai').
                                  If not provided, uses UTC.

    Returns:
        Dict[str, str]: A dictionary containing:
            - current_time (str): The current date or datetime string in the requested format.
            - timezone (str): The timezone for which the time is provided.

    Raises:
        ValueError: If the provided timezone is not a valid IANA timezone name.
    """
    # Validate and set timezone
    if timezone:
        try:
            tz = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            raise ValueError(f"Invalid timezone: {timezone}")
    else:
        tz = pytz.UTC

    # Get current time in the specified timezone
    now = datetime.now(tz)

    # Determine format
    if not format:
        formatted_time = now.isoformat()
    else:
        try:
            formatted_time = now.strftime(format)
        except ValueError as e:
            raise ValueError(f"Invalid format string: {format}") from e

    # Call external API (simulated) to get data (even though we compute it)
    api_data = call_external_api("time-mcp-server-current_time")

    # Construct result using computed values (api_data is only for schema compliance)
    result = {
        "current_time": formatted_time,
        "timezone": timezone if timezone else "UTC"
    }

    return result