from typing import Dict, Any, Optional
from datetime import datetime, timezone as dt_timezone, timedelta
import pytz

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - current_time (str): The current time in the specified or default timezone, formatted as "YYYY-MM-DD HH:MM:SS"
    """
    # Since we cannot make real external calls, simulate current time
    # Default to UTC+8 if no timezone is specified in simulation
    now = datetime.now(dt_timezone.utc)
    # Simulate a default timezone (e.g., Asia/Shanghai)
    tz = pytz.timezone("Asia/Shanghai")
    localized = now.astimezone(tz)
    current_time_str = localized.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "current_time": current_time_str
    }

def server_time_get_current_time(timezone: Optional[str] = None) -> Dict[str, Any]:
    """
    获取当前时间
    
    Args:
        timezone (Optional[str]): 时区名称（如 'Asia/Shanghai'、'UTC' 等），默认为 None 表示使用系统默认时区（UTC+8）
    
    Returns:
        Dict[str, Any]: 包含当前时间的字典，格式如下：
            - currentTime (str): 指定时区或默认时区下的当前时间，格式为 "YYYY-MM-DD HH:MM:SS"
    
    Raises:
        ValueError: 当提供的时区名称无效时抛出
    """
    # 如果未指定时区，默认使用 Asia/Shanghai
    if timezone is None:
        tz = pytz.timezone("Asia/Shanghai")
    else:
        try:
            tz = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValueError(f"Unknown timezone: {timezone}")
    
    # 获取当前 UTC 时间并转换为指定时区
    now = datetime.now(dt_timezone.utc).astimezone(tz)
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # 构造输出结构
    result = {
        "currentTime": current_time_str
    }
    
    return result