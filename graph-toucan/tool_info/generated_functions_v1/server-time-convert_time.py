from typing import Dict, Any
from datetime import datetime, timezone, timedelta
import re

def server_time_convert_time(source_timezone: str, target_timezone: str, time: str) -> Dict[str, Any]:
    """
    在时区之间转换时间。

    支持的时区格式：
    - UTC±[hh]:[mm] (例如: UTC+08:00, UTC-05:00)
    - UTC±[hh] (例如: UTC+8, UTC-5)
    - 简写如: UTC, GMT, EST, PST 等（有限支持常见时区缩写）

    参数:
        source_timezone (str): 源时区，格式如 'UTC+8' 或 'UTC+08:00'
        target_timezone (str): 目标时区，格式如 'UTC-5' 或 'UTC-05:00'
        time (str): ISO 8601 格式的时间字符串，如 '2023-10-15T14:30:00'

    返回:
        Dict[str, Any]: 包含转换后时间的字典，键为 'convertedTime'，值为 ISO 8601 字符串（含时区偏移）

    异常:
        ValueError: 当输入格式无效或不支持时区时抛出
    """
    # 解析输入时间
    try:
        dt = datetime.fromisoformat(time.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"Invalid ISO 8601 time format: {time}")

    def parse_timezone(tz_str: str) -> timezone:
        tz_str = tz_str.strip().upper()
        # 处理常见缩写
        abbreviations = {
            "UTC": timezone.utc,
            "GMT": timezone.utc,
            "EST": timezone(timedelta(hours=-5)),
            "PST": timezone(timedelta(hours=-8)),
            "CST": timezone(timedelta(hours=-6)),
            "MST": timezone(timedelta(hours=-7)),
            "EDT": timezone(timedelta(hours=-4)),
            "PDT": timezone(timedelta(hours=-7)),
            "CDT": timezone(timedelta(hours=-5)),
            "MDT": timezone(timedelta(hours=-6)),
        }
        if tz_str in abbreviations:
            return abbreviations[tz_str]

        # 匹配 UTC±hh:mm 或 UTC±hh
        match = re.match(r"^UTC([+-])(\d{1,2})(?::(\d{2}))?$", tz_str)
        if not match:
            raise ValueError(f"Unsupported timezone format: {tz_str}")
        sign, hours, minutes = match.groups()
        hours = int(hours)
        minutes = int(minutes) if minutes else 0
        if sign == "-":
            hours = -hours
            minutes = -minutes
        offset = timedelta(hours=hours, minutes=minutes)
        return timezone(offset)

    try:
        source_tz = parse_timezone(source_timezone)
        target_tz = parse_timezone(target_timezone)
    except ValueError as e:
        raise e

    # 如果原始时间没有时区信息，设置为源时区
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=source_tz)
    else:
        # 如果已有时区，则转换为源时区进行校准
        dt = dt.astimezone(source_tz)

    # 转换为目标时区
    converted_dt = dt.astimezone(target_tz)

    return {"convertedTime": converted_dt.isoformat()}