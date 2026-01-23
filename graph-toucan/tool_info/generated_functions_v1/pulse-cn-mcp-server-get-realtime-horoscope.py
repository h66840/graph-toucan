from typing import Dict, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching horoscope data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - horoscope_data_overall (int): Overall fortune rating (1-10)
        - horoscope_data_love (int): Love fortune rating (1-10)
        - horoscope_data_career (int): Career fortune rating (1-10)
        - horoscope_data_health (int): Health fortune rating (1-10)
        - horoscope_data_summary (str): Textual summary of horoscope
        - horoscope_data_compatibility (str): Most compatible zodiac sign
        - horoscope_data_color (str): Lucky color for the period
        - horoscope_data_lucky_number (int): Lucky number for the period
        - horoscope_data_mood (str): General mood keyword
        - timestamp (str): ISO 8601 formatted timestamp
        - zodiac_sign (str): English name of zodiac sign (e.g., "aries", "leo")
        - period (str): Time period ("today", "nextday", "week", "month")
    """
    return {
        "horoscope_data_overall": 7,
        "horoscope_data_love": 8,
        "horoscope_data_career": 6,
        "horoscope_data_health": 9,
        "horoscope_data_summary": "A great day for new beginnings and social connections. Trust your instincts.",
        "horoscope_data_compatibility": "libra",
        "horoscope_data_color": "blue",
        "horoscope_data_lucky_number": 3,
        "horoscope_data_mood": "optimistic",
        "timestamp": datetime.now().isoformat(),
        "zodiac_sign": "leo",
        "period": "today"
    }


def pulse_cn_mcp_server_get_realtime_horoscope(time: Optional[str] = None, type: Optional[str] = None) -> Dict[str, Any]:
    """
    获取今日、明日、本周、本月十二星座运势，返回包含运势内容的实时数据。

    Args:
        time (Optional[str]): 运势时段，可选值为 "today", "nextday", "week", "month"
        type (Optional[str]): 星座名称（英文），如 "aries", "leo" 等

    Returns:
        Dict containing:
        - horoscope_data (Dict): 包含整体、爱情、事业、健康等方面的运势详情
        - timestamp (str): ISO 8601 格式的时间戳
        - zodiac_sign (str): 所查询的星座英文名称
        - period (str): 运势周期
        - compatibility (str): 本周期最匹配星座
        - color (str): 幸运颜色
        - lucky_number (int): 幸运数字
        - mood (str): 心情关键词
        - overall (int): 整体运势评分 (1-10)
        - love (int): 爱情运势评分 (1-10)
        - career (int): 事业运势评分 (1-10)
        - health (int): 健康运势评分 (1-10)
        - summary (str): 运势简要文字描述
    """
    # Validate input parameters
    valid_periods = {"today", "nextday", "week", "month"}
    if time and time not in valid_periods:
        raise ValueError(f"Invalid time period: {time}. Must be one of {valid_periods}")

    # Default to "today" if not provided
    period = time or "today"
    
    # Default to "leo" if type not provided
    zodiac_sign = type.lower() if type else "leo"

    # Fetch data from external API (simulated)
    api_data = call_external_api("pulse-cn-mcp-server-get-realtime-horoscope")

    # Construct the horoscope data structure from flat API response
    result = {
        "horoscope_data": {
            "overall": api_data["horoscope_data_overall"],
            "love": api_data["horoscope_data_love"],
            "career": api_data["horoscope_data_career"],
            "health": api_data["horoscope_data_health"],
            "summary": api_data["horoscope_data_summary"],
            "compatibility": api_data["horoscope_data_compatibility"],
            "color": api_data["horoscope_data_color"],
            "lucky_number": api_data["horoscope_data_lucky_number"],
            "mood": api_data["horoscope_data_mood"]
        },
        "timestamp": api_data["timestamp"],
        "zodiac_sign": zodiac_sign,
        "period": period,
        "compatibility": api_data["horoscope_data_compatibility"],
        "color": api_data["horoscope_data_color"],
        "lucky_number": api_data["horoscope_data_lucky_number"],
        "mood": api_data["horoscope_data_mood"],
        "overall": api_data["horoscope_data_overall"],
        "love": api_data["horoscope_data_love"],
        "career": api_data["horoscope_data_career"],
        "health": api_data["horoscope_data_health"],
        "summary": api_data["horoscope_data_summary"]
    }

    return result