from typing import Dict, List, Any, Optional
from datetime import datetime, timezone, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching Chinese calendar data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - solar_date (str): Solar date with weekday
        - lunar_date (str): Lunar date string
        - gan_zhi_0 (str): Year pillar in Gan-Zhi
        - gan_zhi_1 (str): Month pillar in Gan-Zhi
        - gan_zhi_2 (str): Day pillar in Gan-Zhi
        - zodiac (str): Chinese zodiac animal
        - na_yin (str): Na Yin element
        - lunar_festival (str): Lunar festival name if any
        - solar_term (str): Solar term of the day
        - lunar_constellation (str): Lunar mansion with auspiciousness
        - peng_zu_bai_ji (str): Peng Zu Bai Ji taboo phrase
        - shen_directions_xi_shen (str): Xi Shen direction
        - shen_directions_yang_gui (str): Yang Gui Shen direction
        - shen_directions_yin_gui (str): Yin Gui Shen direction
        - shen_directions_fu_shen (str): Fu Shen direction
        - shen_directions_cai_shen (str): Cai Shen direction
        - conflict_animal_and_sha_chong (str): Animal in conflict
        - conflict_animal_and_sha_sha (str): Direction of Sha
        - yi_activities_0 (str): First recommended activity
        - yi_activities_1 (str): Second recommended activity
        - ji_activities_0 (str): First prohibited activity
        - ji_activities_1 (str): Second prohibited activity
    """
    return {
        "solar_date": "2025年04月05日 星期六",
        "lunar_date": "农历二零二五年三月初七",
        "gan_zhi_0": "乙巳",
        "gan_zhi_1": "庚辰",
        "gan_zhi_2": "壬戌",
        "zodiac": "蛇",
        "na_yin": "覆灯火",
        "lunar_festival": "清明节",
        "solar_term": "清明",
        "lunar_constellation": "角木蛟吉",
        "peng_zu_bai_ji": "壬不汲水更难提防，戌不吃犬作怪上床",
        "shen_directions_xi_shen": "正南",
        "shen_directions_yang_gui": "东北",
        "shen_directions_yin_gui": "西南",
        "shen_directions_fu_shen": "正东",
        "shen_directions_cai_shen": "正西",
        "conflict_animal_and_sha_chong": "龙",
        "conflict_animal_and_sha_sha": "北",
        "yi_activities_0": "祭祀",
        "yi_activities_1": "扫墓",
        "ji_activities_0": "嫁娶",
        "ji_activities_1": "开市"
    }

def bazi_calculator_getChineseCalendar(solarDatetime: Optional[str] = None) -> Dict[str, Any]:
    """
    获取指定公历时间（默认今天）的黄历信息。
    
    Args:
        solarDatetime (Optional[str]): 用ISO时间格式表示的公历时间，例如：'2008-03-01T13:00:00+08:00'。
            如果未提供，则使用当前时间（默认为北京时间）。
    
    Returns:
        Dict containing detailed Chinese calendar information with the following structure:
        - solar_date (str): 公历日期，包含年、月、日及星期信息
        - lunar_date (str): 农历日期，格式为“农历X年Y月Z日”
        - gan_zhi (List[str]): 年、月、日的干支组合，按顺序为年柱、月柱、日柱
        - zodiac (str): 生肖，如“蛇”、“猪”、“鼠”等
        - na_yin (str): 纳音五行，如“沙中土”、“金箔金”等
        - lunar_festival (str): 农历节日名称（如有），如“中秋节”
        - solar_term (str): 当日节气，如“寒露”、“白露”、“小暑”等
        - lunar_constellation (str): 二十八宿名称，含吉凶标记，如“轸水蚓吉”
        - peng_zu_bai_ji (str): 彭祖百忌宜忌口诀，描述当日不宜事项
        - shen_directions (Dict): 各类神煞方位，包括喜神、阳贵神、阴贵神、福神、财神的方位
        - conflict_animal_and_sha (Dict): 冲煞信息，包含冲的生肖（如“猪”）和煞的方向（如“东”）
        - yi_activities (List[str]): 宜进行的活动列表，如“嫁娶”、“求嗣”等
        - ji_activities (List[str]): 忌进行的活动列表，如“上梁”、“出行”等
    
    Example:
        >>> result = bazi_calculator_getChineseCalendar("2025-04-05T08:00:00+08:00")
        >>> print(result["lunar_date"])
        农历二零二五年三月初七
    """
    # Validate input format if provided
    if solarDatetime is not None:
        try:
            # Parse ISO format datetime
            dt = datetime.fromisoformat(solarDatetime.replace('Z', '+00:00'))
        except ValueError as e:
            raise ValueError(f"Invalid ISO format for solarDatetime: {solarDatetime}") from e
    else:
        # Use current time in +08:00 (China Standard Time)
        dt = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8)))
    
    # Fetch simulated external data
    api_data = call_external_api("bazi-calculator-getChineseCalendar")
    
    # Construct gan_zhi list from indexed fields
    gan_zhi = [
        api_data["gan_zhi_0"],
        api_data["gan_zhi_1"],
        api_data["gan_zhi_2"]
    ]
    
    # Construct shen_directions dict
    shen_directions = {
        "xi_shen": api_data["shen_directions_xi_shen"],
        "yang_gui": api_data["shen_directions_yang_gui"],
        "yin_gui": api_data["shen_directions_yin_gui"],
        "fu_shen": api_data["shen_directions_fu_shen"],
        "cai_shen": api_data["shen_directions_cai_shen"]
    }
    
    # Construct conflict_animal_and_sha dict
    conflict_animal_and_sha = {
        "chong": api_data["conflict_animal_and_sha_chong"],
        "sha": api_data["conflict_animal_and_sha_sha"]
    }
    
    # Construct yi_activities list
    yi_activities = [
        api_data["yi_activities_0"],
        api_data["yi_activities_1"]
    ]
    
    # Construct ji_activities list
    ji_activities = [
        api_data["ji_activities_0"],
        api_data["ji_activities_1"]
    ]
    
    # Final result construction
    result = {
        "solar_date": api_data["solar_date"],
        "lunar_date": api_data["lunar_date"],
        "gan_zhi": gan_zhi,
        "zodiac": api_data["zodiac"],
        "na_yin": api_data["na_yin"],
        "lunar_festival": api_data["lunar_festival"],
        "solar_term": api_data["solar_term"],
        "lunar_constellation": api_data["lunar_constellation"],
        "peng_zu_bai_ji": api_data["peng_zu_bai_ji"],
        "shen_directions": shen_directions,
        "conflict_animal_and_sha": conflict_animal_and_sha,
        "yi_activities": yi_activities,
        "ji_activities": ji_activities
    }
    
    return result