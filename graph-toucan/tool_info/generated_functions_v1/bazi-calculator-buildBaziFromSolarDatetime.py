from typing import Dict, Any, Optional
from datetime import datetime
import re

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching BaZi calculation data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - gender_str (str): Gender as "男" or "女"
        - solar_datetime_str (str): Solar datetime in format "YYYY年MM月DD日 HH:mm:ss"
        - lunar_info (str): Lunar date and time with stems, branches, and solar terms
        - bazi_str (str): Four pillars in format "Year Month Day Hour"
        - zodiac (str): Chinese zodiac animal
        - day_master (str): Day pillar's heavenly stem
        - year_gan (str): Year pillar's heavenly stem
        - year_zhi (str): Year pillar's earthly branch
        - year_nayin (str): Year pillar's NaYin
        - year_xun (str): Year pillar's xun
        - year_kongwang (str): Year pillar's kong wang
        - year_xingyun (str): Year pillar's xing yun
        - year_zizuo (str): Year pillar's zi zuo
        - year_zhi_main (str): Year branch's main hidden stem
        - year_zhi_middle (str): Year branch's middle hidden stem
        - year_zhi_remain (str): Year branch's remaining hidden stem
        - month_gan (str): Month pillar's heavenly stem
        - month_zhi (str): Month pillar's earthly branch
        - month_nayin (str): Month pillar's NaYin
        - month_xun (str): Month pillar's xun
        - month_kongwang (str): Month pillar's kong wang
        - month_xingyun (str): Month pillar's xing yun
        - month_zizuo (str): Month pillar's zi zuo
        - month_zhi_main (str): Month branch's main hidden stem
        - month_zhi_middle (str): Month branch's middle hidden stem
        - month_zhi_remain (str): Month branch's remaining hidden stem
        - day_gan (str): Day pillar's heavenly stem
        - day_zhi (str): Day pillar's earthly branch
        - day_nayin (str): Day pillar's NaYin
        - day_xun (str): Day pillar's xun
        - day_kongwang (str): Day pillar's kong wang
        - day_xingyun (str): Day pillar's xing yun
        - day_zizuo (str): Day pillar's zi zuo
        - day_zhi_main (str): Day branch's main hidden stem
        - day_zhi_middle (str): Day branch's middle hidden stem
        - day_zhi_remain (str): Day branch's remaining hidden stem
        - hour_gan (str): Hour pillar's heavenly stem
        - hour_zhi (str): Hour pillar's earthly branch
        - hour_nayin (str): Hour pillar's NaYin
        - hour_xun (str): Hour pillar's xun
        - hour_kongwang (str): Hour pillar's kong wang
        - hour_xingyun (str): Hour pillar's xing yun
        - hour_zizuo (str): Hour pillar's zi zuo
        - hour_zhi_main (str): Hour branch's main hidden stem
        - hour_zhi_middle (str): Hour branch's middle hidden stem
        - hour_zhi_remain (str): Hour branch's remaining hidden stem
        - taiyuan (str): Fetal origin stem-branch
        - taixi (str): Fetal breath stem-branch
        - minggong (str): Ming Palace branch
        - shengong (str): Shen Palace branch
        - shensha_year_0 (str): First shensha for year pillar
        - shensha_month_0 (str): First shensha for month pillar
        - shensha_day_0 (str): First shensha for day pillar
        - shensha_hour_0 (str): First shensha for hour pillar
        - daliuqi_date (str): Start date of Da Yun
        - daliuqi_age (int): Start age of Da Yun
        - daliuqi_ganzhi_0 (str): First Da Yun pillar
        - daliuqi_start_year_0 (int): Start year of first Da Yun
        - daliuqi_end_year_0 (int): End year of first Da Yun
        - daliuqi_tian_gan_0 (str): Heavenly stem shishen of first Da Yun
        - daliuqi_di_zhi_0 (str): Earthly branch shishen of first Da Yun
        - daliuqi_canggan_0 (str): Hidden stems of first Da Yun
        - daliuqi_start_age_0 (int): Start age of first Da Yun
        - daliuqi_end_age_0 (int): End age of first Da Yun
        - xingchongheyi_year_tian (str): Year pillar's heavenly stem interactions
        - xingchongheyi_year_di (str): Year pillar's earthly branch interactions
        - xingchongheyi_month_tian (str): Month pillar's heavenly stem interactions
        - xingchongheyi_month_di (str): Month pillar's earthly branch interactions
        - xingchongheyi_day_tian (str): Day pillar's heavenly stem interactions
        - xingchongheyi_day_di (str): Day pillar's earthly branch interactions
        - xingchongheyi_hour_tian (str): Hour pillar's heavenly stem interactions
        - xingchongheyi_hour_di (str): Hour pillar's earthly branch interactions
    """
    return {
        "gender_str": "男",
        "solar_datetime_str": "2008年03月01日 13:00:00",
        "lunar_info": "戊子年正月廿三 未时 【惊蛰:2008-03-05】",
        "bazi_str": "戊子 甲寅 壬戌 戊申",
        "zodiac": "鼠",
        "day_master": "壬",
        "year_gan": "戊", "year_zhi": "子", "year_nayin": "霹雳火", "year_xun": "甲申", "year_kongwang": "寅卯", "year_xingyun": "沐浴", "year_zizuo": "胎",
        "year_zhi_main": "癸", "year_zhi_middle": "", "year_zhi_remain": "",
        "month_gan": "甲", "month_zhi": "寅", "month_nayin": "大溪水", "month_xun": "壬戌", "month_kongwang": "申酉", "month_xingyun": "长生", "month_zizuo": "临官",
        "month_zhi_main": "甲", "month_zhi_middle": "丙", "month_zhi_remain": "戊",
        "day_gan": "壬", "day_zhi": "戌", "day_nayin": "大海水", "day_xun": "壬戌", "day_kongwang": "子丑", "day_xingyun": "冠带", "day_zizuo": "墓",
        "day_zhi_main": "戊", "day_zhi_middle": "辛", "day_zhi_remain": "丁",
        "hour_gan": "戊", "hour_zhi": "申", "hour_nayin": "大驿土", "hour_xun": "甲辰", "hour_kongwang": "戌亥", "hour_xingyun": "长生", "hour_zizuo": "长生",
        "hour_zhi_main": "庚", "hour_zhi_middle": "壬", "hour_zhi_remain": "戊",
        "taiyuan": "乙巳",
        "taixi": "癸亥",
        "minggong": "酉",
        "shengong": "亥",
        "shensha_year_0": "将星",
        "shensha_month_0": "羊刃",
        "shensha_day_0": "华盖",
        "shensha_hour_0": "天乙贵人",
        "daliuqi_date": "2015-07-01",
        "daliuqi_age": 7,
        "daliuqi_ganzhi_0": "乙卯",
        "daliuqi_start_year_0": 2015,
        "daliuqi_end_year_0": 2024,
        "daliuqi_tian_gan_0": "伤官",
        "daliuqi_di_zhi_0": "劫财",
        "daliuqi_canggan_0": "乙",
        "daliuqi_start_age_0": 7,
        "daliuqi_end_age_0": 16,
        "xingchongheyi_year_tian": "戊克壬",
        "xingchongheyi_year_di": "子午冲",
        "xingchongheyi_month_tian": "甲壬合",
        "xingchongheyi_month_di": "寅亥合",
        "xingchongheyi_day_tian": "",
        "xingchongheyi_day_di": "戌辰冲",
        "xingchongheyi_hour_tian": "戊壬克",
        "xingchongheyi_hour_di": "申子辰合水局"
    }

def bazi_calculator_buildBaziFromSolarDatetime(
    solarDatetime: str,
    gender: int,
    eightCharProviderSect: Optional[int] = None
) -> Dict[str, Any]:
    """
    根据阳历时间、性别来获取八字信息。
    
    Args:
        solarDatetime (str): 用ISO时间格式表示的阳历时间，例如：'2008-03-01T13:00:00+08:00'
        gender (int): 性别，传0表示女性，传1表示男性
        eightCharProviderSect (int, optional): 早晚子时配置。1表示23:00-23:59日干支为明天，2表示为当天。默认为None
    
    Returns:
        Dict[str, Any]: 包含完整的八字命盘信息，包括四柱、神煞、大运、刑冲合会等详细信息
        
    Raises:
        ValueError: 当输入参数无效时抛出异常
    """
    # Input validation
    if not solarDatetime:
        raise ValueError("solarDatetime is required")
    
    if gender not in [0, 1]:
        raise ValueError("gender must be 0 (female) or 1 (male)")
    
    if eightCharProviderSect is not None and eightCharProviderSect not in [1, 2]:
        raise ValueError("eightCharProviderSect must be 1 or 2 if provided")
    
    # Validate ISO datetime format
    iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2}|Z)$"
    if not re.match(iso_pattern, solarDatetime):
        raise ValueError("solarDatetime must be in valid ISO format (e.g., 2008-03-01T13:00:00+08:00)")
    
    try:
        # Parse datetime (we don't need actual BaZi calculation, just simulate)
        dt = datetime.fromisoformat(solarDatetime.replace("Z", "+00:00"))
        if dt.year < 1900 or dt.year > 2100:
            raise ValueError("Year must be between 1900 and 2100")
    except Exception as e:
        raise ValueError(f"Invalid datetime format: {str(e)}")
    
    # Call external API to get raw data
    api_data = call_external_api("bazi-calculator-buildBaziFromSolarDatetime")
    
    # Construct year pillar
    year_pillar = {
        "天干": {"干": api_data["year_gan"]},
        "地支": {
            "支": api_data["year_zhi"],
            "藏干": {
                "主气": api_data["year_zhi_main"],
                "中气": api_data["year_zhi_middle"],
                "余气": api_data["year_zhi_remain"]
            }
        },
        "纳音": api_data["year_nayin"],
        "旬": api_data["year_xun"],
        "空亡": api_data["year_kongwang"],
        "星运": api_data["year_xingyun"],
        "自坐": api_data["year_zizuo"]
    }
    
    # Construct month pillar
    month_pillar = {
        "天干": {"干": api_data["month_gan"]},
        "地支": {
            "支": api_data["month_zhi"],
            "藏干": {
                "主气": api_data["month_zhi_main"],
                "中气": api_data["month_zhi_middle"],
                "余气": api_data["month_zhi_remain"]
            }
        },
        "纳音": api_data["month_nayin"],
        "旬": api_data["month_xun"],
        "空亡": api_data["month_kongwang"],
        "星运": api_data["month_xingyun"],
        "自坐": api_data["month_zizuo"]
    }
    
    # Construct day pillar
    day_pillar = {
        "天干": {"干": api_data["day_gan"]},
        "地支": {
            "支": api_data["day_zhi"],
            "藏干": {
                "主气": api_data["day_zhi_main"],
                "中气": api_data["day_zhi_middle"],
                "余气": api_data["day_zhi_remain"]
            }
        },
        "纳音": api_data["day_nayin"],
        "旬": api_data["day_xun"],
        "空亡": api_data["day_kongwang"],
        "星运": api_data["day_xingyun"],
        "自坐": api_data["day_zizuo"]
    }
    
    # Construct hour pillar
    hour_pillar = {
        "天干": {"干": api_data["hour_gan"]},
        "地支": {
            "支": api_data["hour_zhi"],
            "藏干": {
                "主气": api_data["hour_zhi_main"],
                "中气": api_data["hour_zhi_middle"],
                "余气": api_data["hour_zhi_remain"]
            }
        },
        "纳音": api_data["hour_nayin"],
        "旬": api_data["hour_xun"],
        "空亡": api_data["hour_kongwang"],
        "星运": api_data["hour_xingyun"],
        "自坐": api_data["hour_zizuo"]
    }
    
    # Construct shensha
    shensha = {
        "年柱": [api_data["shensha_year_0"]] if api_data["shensha_year_0"] else [],
        "月柱": [api_data["shensha_month_0"]] if api_data["shensha_month_0"] else [],
        "日柱": [api_data["shensha_day_0"]] if api_data["shensha_day_0"] else [],
        "时柱": [api_data["shensha_hour_0"]] if api_data["shensha_hour_0"] else []
    }
    
    # Construct daliuqi (da yun)
    daliuqi = {
        "起运日期": api_data["daliuqi_date"],
        "起运年龄": api_data["daliuqi_age"],
        "大运列表": [
            {
                "干支": api_data["daliuqi_ganzhi_0"],
                "开始年份": api_data["daliuqi_start_year_0"],
                "结束年份": api_data["daliuqi_end_year_0"],
                "天干十神": api_data["daliuqi_tian_gan_0"],
                "地支十神": api_data["daliuqi_di_zhi_0"],
                "地支藏干": api_data["daliuqi_canggan_0"],
                "开始年龄": api_data["daliuqi_start_age_0"],
                "结束年龄": api_data["daliuqi_end_age_0"]
            }
        ]
    }
    
    # Construct xingchongheyi
    xingchongheyi = {
        "年柱": {
            "天干": api_data["xingchongheyi_year_tian"] if api_data["xingchongheyi_year_tian"] else "",
            "地支": api_data["xingchongheyi_year_di"] if api_data["xingchongheyi_year_di"] else ""
        },
        "月柱": {
            "天干": api_data["xingchongheyi_month_tian"] if api_data["xingchongheyi_month_tian"] else "",
            "地支": api_data["xingchongheyi_month_di"] if api_data["xingchongheyi_month_di"] else ""
        },
        "日柱": {
            "天干": api_data["xingchongheyi_day_tian"] if api_data["xingchongheyi_day_tian"] else "",
            "地支": api_data["xingchongheyi_day_di"] if api_data["xingchongheyi_day_di"] else ""
        },
        "时柱": {
            "天干": api_data["xingchongheyi_hour_tian"] if api_data["xingchongheyi_hour_tian"] else "",
            "地支": api_data["xingchongheyi_hour_di"] if api_data["xingchongheyi_hour_di"] else ""
        }
    }
    
    # Final result construction
    result = {
        "性别": api_data["gender_str"],
        "阳历": api_data["solar_datetime_str"],
        "农历": api_data["lunar_info"],
        "八字": api_data["bazi_str"],
        "生肖": api_data["zodiac"],
        "日主": api_data["day_master"],
        "年柱": year_pillar,
        "月柱": month_pillar,
        "日柱": day_pillar,
        "时柱": hour_pillar,
        "胎元": api_data["taiyuan"],
        "胎息": api_data["taixi"],
        "命宫": api_data["minggong"],
        "身宫": api_data["shengong"],
        "神煞": shensha,
        "大运": daliuqi,
        "刑冲合会": xingchongheyi
    }
    
    return result