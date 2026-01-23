from typing import Dict, Any, Optional
from datetime import datetime, timezone


def time_mcp_server_get_timestamp(time: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the timestamp for the given time string.

    If no time is provided, the current UTC time is used.
    The input time string should be in the format "YYYY-MM-DD HH:mm:ss".
    The time is parsed as UTC and converted to a Unix timestamp in milliseconds.

    Args:
        time (Optional[str]): The time string to convert. Format: "YYYY-MM-DD HH:mm:ss".
                              If None, current UTC time is used.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - timestamp_ms (int): Unix timestamp in milliseconds (UTC)
            - input_time (str): The original time string provided (or formatted current time if none provided)
            - parsed_as_timezone (str): Timezone context used for parsing, always "UTC"
    
    Raises:
        ValueError: If the provided time string is not in the correct format.
    """
    if time is None:
        dt = datetime.now(timezone.utc)
        time = dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        try:
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            dt = dt.replace(tzinfo=timezone.utc)
        except ValueError as e:
            raise ValueError(f"Invalid time format: {e}")

    timestamp_ms = int(dt.timestamp() * 1000)

    return {
        "timestamp_ms": timestamp_ms,
        "input_time": time,
        "parsed_as_timezone": "UTC"
    }