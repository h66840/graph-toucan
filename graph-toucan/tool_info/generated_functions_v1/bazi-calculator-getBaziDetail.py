from typing import Dict, Any, Optional
from datetime import datetime, timezone
import re

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching BaZi calculation data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - gender_str (str): Gender as string, e.g., "男" or "女"
        - solar_date (str): Solar date in format "YYYY年MM月DD日 HH:mm:ss"
        - lunar_date (str): Lunar date with stem-branch and hour, e.g., "庚辰年五月初五 巳时"
        - eight_char (str): Four pillars, e.g., "庚辰 壬午 丁未 乙巳"
        - zodiac (str): Chinese zodiac animal, e.g., "龙"
        - day_master (str): Day stem representing self, e.g., "丁"
        - year_gan (str): Heavenly stem of year pillar
        - year_zhi (str): Earthly branch of year pillar
        - year_nayin (str): NAYIN of year pillar
        - year_xun (str): Xun of year pillar
        - year_kongwang (str): Kongwang of year pillar
        - year_xingyun (str): Xingyun of year pillar
        - year_zizuo (str): Zizuo of year pillar
        - year_zhi_canggan_zhugan (str): Primary hidden stem of year branch
        - year_zhi_canggan_zhugan_shishen (str): Shishen of primary hidden stem
        - year_zhi_canggan_zhongqi (str): Middle hidden stem of year branch
        - year_zhi_canggan_zhongqi_shishen (str): Shishen of middle hidden stem
        - year_zhi_canggan_yuqi (str): Remaining hidden stem of year branch
        - year_zhi_canggan_yuqi_shishen (str): Shishen of remaining hidden stem
        - month_gan (str): Heavenly stem of month pillar
        - month_zhi (str): Earthly branch of month pillar
        - month_nayin (str): NAYIN of month pillar
        - month_xun (str): Xun of month pillar
        - month_kongwang (str): Kongwang of month pillar
        - month_xingyun (str): Xingyun of month pillar
        - month_zizuo (str): Zizuo of month pillar
        - month_zhi_canggan_zhugan (str): Primary hidden stem of month branch
        - month_zhi_canggan_zhugan_shishen (str): Shishen of primary hidden stem
        - month_zhi_canggan_zhongqi (str): Middle hidden stem of month branch
        - month_zhi_canggan_zhongqi_shishen (str): Shishen of middle hidden stem
        - month_zhi_canggan_yuqi (str): Remaining hidden stem of month branch
        - month_zhi_canggan_yuqi_shishen (str): Shishen of remaining hidden stem
        - day_gan (str): Heavenly stem of day pillar
        - day_zhi (str): Earthly branch of day pillar
        - day_nayin (str): NAYIN of day pillar
        - day_xun (str): Xun of day pillar
        - day_kongwang (str): Kongwang of day pillar
        - day_xingyun (str): Xingyun of day pillar
        - day_zizuo (str): Zizuo of day pillar
        - day_zhi_canggan_zhugan (str): Primary hidden stem of day branch
        - day_zhi_canggan_zhugan_shishen (str): Shishen of primary hidden stem
        - day_zhi_canggan_zhongqi (str): Middle hidden stem of day branch
        - day_zhi_canggan_zhongqi_shishen (str): Shishen of middle hidden stem
        - day_zhi_canggan_yuqi (str): Remaining hidden stem of day branch
        - day_zhi_canggan_yuqi_shishen (str): Shishen of remaining hidden stem
        - hour_gan (str): Heavenly stem of hour pillar
        - hour_zhi (str): Earthly branch of hour pillar
        - hour_nayin (str): NAYIN of hour pillar
        - hour_xun (str): Xun of hour pillar
        - hour_kongwang (str): Kongwang of hour pillar
        - hour_xingyun (str): Xingyun of hour pillar
        - hour_zizuo (str): Zizuo of hour pillar
        - hour_zhi_canggan_zhugan (str): Primary hidden stem of hour branch
        - hour_zhi_canggan_zhugan_shishen (str): Shishen of primary hidden stem
        - hour_zhi_canggan_zhongqi (str): Middle hidden stem of hour branch
        - hour_zhi_canggan_zhongqi_shishen (str): Shishen of middle hidden stem
        - hour_zhi_canggan_yuqi (str): Remaining hidden stem of hour branch
        - hour_zhi_canggan_yuqi_shishen (str): Shishen of remaining hidden stem
        - taiyuan (str): Taiyuan stem-branch
        - taixi (str): Taixi stem-branch
        - minggong (str): Minggong stem-branch
        - shengong (str): Shengong stem-branch
        - shensha_year_0 (str): First shensha in year pillar
        - shensha_month_0 (str): First shensha in month pillar
        - shensha_day_0 (str): First shensha in day pillar
        - shensha_hour_0 (str): First shensha in hour pillar
        - daliu_start_date (str): Start date of first da-liu
        - daliu_start_age (int): Start age of first da-liu
        - daliu_end_age (int): End age of first da-liu
        - daliu_ganzhi (str): Stem-branch of da-liu
        - daliu_tianganshishen (str): Tian-gan shishen of da-liu
        - daliu_dizhishishen (str): Di-zhi shishen of da-liu
        - daliu_dizhi_canggan_zhugan (str): Primary hidden stem in da-liu di-zhi
        - daliu_dizhi_canggan_zhongqi (str): Middle hidden stem in da-liu di-zhi
        - daliu_dizhi_canggan_yuqi (str): Remaining hidden stem in da-liu di-zhi
        - daliu_start_year (int): Start year of da-liu
        - daliu_end_year (int): End year of da-liu
        - xingchonghehui_nian_tian (str): Tian relationship in year pillar
        - xingchonghehui_nian_di (str): Di relationship in year pillar
        - xingchonghehui_yue_tian (str): Tian relationship in month pillar
        - xingchonghehui_yue_di (str): Di relationship in month pillar
        - xingchonghehui_ri_tian (str): Tian relationship in day pillar
        - xingchonghehui_ri_di (str): Di relationship in day pillar
        - xingchonghehui_shi_tian (str): Tian relationship in hour pillar
        - xingchonghehui_shi_di (str): Di relationship in hour pillar
    """
    return {
        "gender_str": "男",
        "solar_date": "2008年03月01日 13:00:00",
        "lunar_date": "丁亥年正月廿五 未时",
        "eight_char": "丁亥 壬寅 丁未 丁未",
        "zodiac": "猪",
        "day_master": "丁",
        "year_gan": "丁",
        "year_zhi": "亥",
        "year_nayin": "屋上土",
        "year_xun": "甲申",
        "year_kongwang": "辰巳",
        "year_xingyun": "冠带",
        "year_zizuo": "胎",
        "year_zhi_canggan_zhugan": "壬",
        "year_zhi_canggan_zhugan_shishen": "正官",
        "year_zhi_canggan_zhongqi": "甲",
        "year_zhi_canggan_zhongqi_shishen": "正印",
        "year_zhi_canggan_yuqi": "",
        "year_zhi_canggan_yuqi_shishen": "",
        "month_gan": "壬",
        "month_zhi": "寅",
        "month_nayin": "金箔金",
        "month_xun": "甲辰",
        "month_kongwang": "午未",
        "month_xingyun": "长生",
        "month_zizuo": "养",
        "month_zhi_canggan_zhugan": "甲",
        "month_zhi_canggan_zhugan_shishen": "正印",
        "month_zhi_canggan_zhongqi": "丙",
        "month_zhi_canggan_zhongqi_shishen": "劫财",
        "month_zhi_canggan_yuqi": "戊",
        "month_zhi_canggan_yuqi_shishen": "伤官",
        "day_gan": "丁",
        "day_zhi": "未",
        "day_nayin": "天河水",
        "day_xun": "甲辰",
        "day_kongwang": "午未",
        "day_xingyun": "冠带",
        "day_zizuo": "冠带",
        "day_zhi_canggan_zhugan": "己",
        "day_zhi_canggan_zhugan_shishen": "食神",
        "day_zhi_canggan_zhongqi": "丁",
        "day_zhi_canggan_zhongqi_shishen": "比肩",
        "day_zhi_canggan_yuqi": "乙",
        "day_zhi_canggan_yuqi_shishen": "偏印",
        "hour_gan": "丁",
        "hour_zhi": "未",
        "hour_nayin": "天河水",
        "hour_xun": "甲辰",
        "hour_kongwang": "午未",
        "hour_xingyun": "冠带",
        "hour_zizuo": "冠带",
        "hour_zhi_canggan_zhugan": "己",
        "hour_zhi_canggan_zhugan_shishen": "食神",
        "hour_zhi_canggan_zhongqi": "丁",
        "hour_zhi_canggan_zhongqi_shishen": "比肩",
        "hour_zhi_canggan_yuqi": "乙",
        "hour_zhi_canggan_yuqi_shishen": "偏印",
        "taiyuan": "癸卯",
        "taixi": "辛丑",
        "minggong": "己酉",
        "shengong": "乙巳",
        "shensha_year_0": "国印",
        "shensha_month_0": "文昌",
        "shensha_day_0": "红鸾",
        "shensha_hour_0": "寡宿",
        "daliu_start_date": "2015-03-01",
        "daliu_start_age": 7,
        "daliu_end_age": 16,
        "daliu_ganzhi": "癸卯",
        "daliu_tianganshishen": "七杀",
        "daliu_dizhishishen": "偏印",
        "daliu_dizhi_canggan_zhugan": "乙",
        "daliu_dizhi_canggan_zhongqi": "",
        "daliu_dizhi_canggan_yuqi": "",
        "daliu_start_year": 2015,
        "daliu_end_year": 2024,
        "xingchonghehui_nian_tian": "丁壬合化木",
        "xingchonghehui_nian_di": "寅亥合木",
        "xingchonghehui_yue_tian": "",
        "xingchonghehui_yue_di": "寅亥合木",
        "xingchonghehui_ri_tian": "",
        "xingchonghehui_ri_di": "午未合火",
        "xingchonghehui_shi_tian": "",
        "xingchonghehui_shi_di": "午未合火"
    }

def bazi_calculator_getBaziDetail(
    gender: int,
    solarDatetime: Optional[str] = None,
    lunarDatetime: Optional[str] = None,
    eightCharProviderSect: Optional[int] = None
) -> Dict[str, Any]:
    """
    根据时间（公历或农历）、性别来获取八字信息。solarDatetime和lunarDatetime必须传且只传其中一个。

    Args:
        gender (int): 传0表示女性，传1表示男性。
        solarDatetime (str, optional): 用ISO时间格式表示的公历时间. 例如：`2008-03-01T13:00:00+08:00`。
        lunarDatetime (str, optional): 农历时间。例如农历2000年5月初五中午12点整表示为：`2000-5-5 12:00:00`。
        eightCharProviderSect (int, optional): 早晚子时配置。传1表示23:00-23:59日干支为明天，传2表示23:00-23:59日干支为当天。

    Returns:
        Dict[str, Any]: 包含性别、阳历、农历、八字、生肖、日主、四柱详细信息、胎元、胎息、命宫、身宫、神煞、大运、刑冲合会等信息。

    Raises:
        ValueError: 如果solarDatetime和lunarDatetime都未提供或都提供了，或者gender不在0-1范围内。
    """
    # Input validation
    if not (solarDatetime or lunarDatetime):
        raise ValueError("solarDatetime 和 lunarDatetime 必须提供其中一个。")
    if solarDatetime and lunarDatetime:
        raise ValueError("solarDatetime 和 lunarDatetime 不能同时提供。")
    if gender not in (0, 1):
        raise ValueError("gender 必须为0（女性）或1（男性）。")

    # Simulate external API call to get BaZi data
    api_data = call_external_api("bazi-calculator-getBaziDetail")

    # Construct year pillar
    year_pillar = {
        "天干": api_data["year_gan"],
        "地支": api_data["year_zhi"],
        "纳音": api_data["year_nayin"],
        "旬": api_data["year_xun"],
        "空亡": api_data["year_kongwang"],
        "星运": api_data["year_xingyun"],
        "自坐": api_data["year_zizuo"],
        "地支藏干": {
            "主气": {
                "天干": api_data["year_zhi_canggan_zhugan"],
                "十神": api_data["year_zhi_canggan_zhugan_shishen"]
            },
            "中气": {
                "天干": api_data["year_zhi_canggan_zhongqi"],
                "十神": api_data["year_zhi_canggan_zhongqi_shishen"]
            },
            "余气": {
                "天干": api_data["year_zhi_canggan_yuqi"],
                "十神": api_data["year_zhi_canggan_yuqi_shishen"]
            }
        }
    }

    # Construct month pillar
    month_pillar = {
        "天干": api_data["month_gan"],
        "地支": api_data["month_zhi"],
        "纳音": api_data["month_nayin"],
        "旬": api_data["month_xun"],
        "空亡": api_data["month_kongwang"],
        "星运": api_data["month_xingyun"],
        "自坐": api_data["month_zizuo"],
        "地支藏干": {
            "主气": {
                "天干": api_data["month_zhi_canggan_zhugan"],
                "十神": api_data["month_zhi_canggan_zhugan_shishen"]
            },
            "中气": {
                "天干": api_data["month_zhi_canggan_zhongqi"],
                "十神": api_data["month_zhi_canggan_zhongqi_shishen"]
            },
            "余气": {
                "天干": api_data["month_zhi_canggan_yuqi"],
                "十神": api_data["month_zhi_canggan_yuqi_shishen"]
            }
        }
    }

    # Construct day pillar
    day_pillar = {
        "天干": api_data["day_gan"],
        "地支": api_data["day_zhi"],
        "纳音": api_data["day_nayin"],
        "旬": api_data["day_xun"],
        "空亡": api_data["day_kongwang"],
        "星运": api_data["day_xingyun"],
        "自坐": api_data["day_zizuo"],
        "地支藏干": {
            "主气": {
                "天干": api_data["day_zhi_canggan_zhugan"],
                "十神": api_data["day_zhi_canggan_zhugan_shishen"]
            },
            "中气": {
                "天干": api_data["day_zhi_canggan_zhongqi"],
                "十神": api_data["day_zhi_canggan_zhongqi_shishen"]
            },
            "余气": {
                "天干": api_data["day_zhi_canggan_yuqi"],
                "十神": api_data["day_zhi_canggan_yuqi_shishen"]
            }
        }
    }

    # Construct hour pillar
    hour_pillar = {
        "天干": api_data["hour_gan"],
        "地支": api_data["hour_zhi"],
        "纳音": api_data["hour_nayin"],
        "旬": api_data["hour_xun"],
        "空亡": api_data["hour_kongwang"],
        "星运": api_data["hour_xingyun"],
        "自坐": api_data["hour_zizuo"],
        "地支藏干": {
            "主气": {
                "天干": api_data["hour_zhi_canggan_zhugan"],
                "十神": api_data["hour_zhi_canggan_zhugan_shishen"]
            },
            "中气": {
                "天干": api_data["hour_zhi_canggan_zhongqi"],
                "十神": api_data["hour_zhi_canggan_zhongqi_shishen"]
            },
            "余气": {
                "天干": api_data["hour_zhi_canggan_yuqi"],
                "十神": api_data["hour_zhi_canggan_yuqi_shishen"]
            }
        }
    }

    # Construct shensha
    shensha = {
        "年柱": [api_data["shensha_year_0"]] if api_data["shensha_year_0"] else [],
        "月柱": [api_data["shensha_month_0"]] if api_data["shensha_month_0"] else [],
        "日柱": [api_data["shensha_day_0"]] if api_data["shensha_day_0"] else [],
        "时柱": [api_data["shensha_hour_0"]] if api_data["shensha_hour_0"] else []
    }

    # Construct daliu
    daliu_item = {
        "干支": api_data["daliu_ganzhi"],
        "开始年份": api_data["daliu_start_year"],
        "结束年份": api_data["daliu_end_year"],
        "天干十神": api_data["daliu_tianganshishen"],
        "地支十神": api_data["daliu_dizhishishen"],
        "地支藏干": {
            "主气": api_data["daliu_dizhi_canggan_zhugan"],
            "中气": api_data["daliu_dizhi_canggan_zhongqi"],
            "余气": api_data["daliu_dizhi_canggan_yuqi"]
        },
        "开始年龄": api_data["daliu_start_age"],
        "结束年龄": api_data["daliu_end_age"]
    }
    daliu_list = [daliu_item]

    daliu = {
        "起运日期": api_data["daliu_start_date"],
        "起运年龄": api_data["daliu_start_age"],
        "大运列表": daliu_list
    }

    # Construct xingchonghehui
    xingchonghehui = {
        "年": {
            "天干": api_data["xingchonghehui_nian_tian"],
            "地支": api_data["xingchonghehui_nian_di"]
        },
        "月": {
            "天干": api_data["xingchonghehui_yue_tian"],
            "地支": api_data["xingchonghehui_yue_di"]
        },
        "日": {
            "天干": api_data["xingchonghehui_ri_tian"],
            "地支": api_data["xingchonghehui_ri_di"]
        },
        "时": {
            "天干": api_data["xingchonghehui_shi_tian"],
            "地支": api_data["xingchonghehui_shi_di"]
        }
    }

    # Final result
    result = {
        "性别": api_data["gender_str"],
        "阳历": api_data["solar_date"],
        "农历": api_data["lunar_date"],
        "八字": api_data["eight_char"],
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
        "大运": daliu,
        "刑冲合会": xingchonghehui
    }

    return result