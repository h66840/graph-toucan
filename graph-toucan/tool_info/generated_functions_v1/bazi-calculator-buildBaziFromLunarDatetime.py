from typing import Dict, Any, Optional

def bazi_calculator_buildBaziFromLunarDatetime(
    gender: int,
    lunarDatetime: str,
    eightCharProviderSect: Optional[int] = None
) -> Dict[str, Any]:
    """
    根据农历时间、性别来获取八字信息。

    参数:
        gender (int): 性别，传0表示女性，传1表示男性。
        lunarDatetime (str): 农历时间，格式为 'YYYY-MM-DD HH:MM:SS'，例如：'2000-5-15 12:00:00'。
        eightCharProviderSect (int, optional): 早晚子时配置。1表示23:00-23:59日干支为明天，2表示为当天。默认为None。

    返回:
        Dict[str, Any]: 包含性别、阳历、农历、八字、生肖、日主、四柱详细信息、胎元、胎息、命宫、身宫、神煞、大运、刑冲合会等信息的字典。
    """
    # 输入验证
    if gender not in [0, 1]:
        raise ValueError("gender must be 0 (female) or 1 (male).")
    if not isinstance(lunarDatetime, str) or not lunarDatetime.strip():
        raise ValueError("lunarDatetime must be a non-empty string in format 'YYYY-MM-DD HH:MM:SS'.")
    if eightCharProviderSect not in [None, 1, 2]:
        raise ValueError("eightCharProviderSect must be None, 1, or 2.")

    # 模拟外部API调用，返回扁平化的简单字段
    api_data = call_external_api("bazi-calculator-buildBaziFromLunarDatetime")

    # 构建年柱、月柱、日柱、时柱的结构
    def build_zhu(zhu_prefix: str) -> Dict[str, Any]:
        return {
            "天干": {
                "天干": api_data[f"{zhu_prefix}_天干_天干"],
                "五行": api_data[f"{zhu_prefix}_天干_五行"],
                "阴阳": api_data[f"{zhu_prefix}_天干_阴阳"],
                "十神": api_data[f"{zhu_prefix}_天干_十神"]
            },
            "地支": {
                "地支": api_data[f"{zhu_prefix}_地支_地支"],
                "五行": api_data[f"{zhu_prefix}_地支_五行"],
                "阴阳": api_data[f"{zhu_prefix}_地支_阴阳"],
                "藏干": api_data[f"{zhu_prefix}_地支_藏干"]
            },
            "纳音": api_data[f"{zhu_prefix}_纳音"],
            "旬": api_data[f"{zhu_prefix}_旬"],
            "空亡": api_data[f"{zhu_prefix}_空亡"],
            "星运": api_data[f"{zhu_prefix}_星运"],
            "自坐": api_data[f"{zhu_prefix}_自坐"]
        }

    # 构建神煞结构
    def build_shensha(zhu_name: str) -> list:
        return [
            api_data[f"神煞_{zhu_name}_0"]  # 只取第一个神煞
        ] if api_data.get(f"神煞_{zhu_name}_0") else []

    # 构建大运列表
    def build_daying_list() -> list:
        da_yun_list = []
        for i in range(1):  # 仅生成一条大运记录作为示例
            da_yun_list.append({
                "干支": api_data[f"大运_干支_{i}"],
                "开始年份": api_data[f"大运_开始年份_{i}"],
                "结束年份": api_data[f"大运_结束年份_{i}"],
                "天干十神": api_data[f"大运_天干十神_{i}"],
                "地支十神": api_data[f"大运_地支十神_{i}"],
                "地支藏干": api_data[f"大运_地支藏干_{i}"],
                "开始年龄": api_data[f"大运_开始年龄_{i}"],
                "结束年龄": api_data[f"大运_结束年龄_{i}"]
            })
        return da_yun_list

    # 构建刑冲合会结构
    def build_xing_chong_he_hui() -> Dict[str, Any]:
        return {
            "年柱": {
                "天干": api_data.get("刑冲合会_年柱_天干", ""),
                "地支": api_data.get("刑冲合会_年柱_地支", ""),
                "拱": api_data.get("刑冲合会_年柱_拱", ""),
                "双冲": api_data.get("刑冲合会_年柱_双冲", "")
            },
            "月柱": {
                "天干": api_data.get("刑冲合会_月柱_天干", ""),
                "地支": api_data.get("刑冲合会_月柱_地支", ""),
                "拱": api_data.get("刑冲合会_月柱_拱", ""),
                "双冲": api_data.get("刑冲合会_月柱_双冲", "")
            },
            "日柱": {
                "天干": api_data.get("刑冲合会_日柱_天干", ""),
                "地支": api_data.get("刑冲合会_日柱_地支", ""),
                "拱": api_data.get("刑冲合会_日柱_拱", ""),
                "双冲": api_data.get("刑冲合会_日柱_双冲", "")
            },
            "时柱": {
                "天干": api_data.get("刑冲合会_时柱_天干", ""),
                "地支": api_data.get("刑冲合会_时柱_地支", ""),
                "拱": api_data.get("刑冲合会_时柱_拱", ""),
                "双冲": api_data.get("刑冲合会_时柱_双冲", "")
            }
        }

    # 构建最终结果
    result = {
        "性别": api_data["性别"],
        "阳历": api_data["阳历"],
        "农历": api_data["农历"],
        "八字": api_data["八字"],
        "生肖": api_data["生肖"],
        "日主": api_data["日主"],
        "年柱": build_zhu("年柱"),
        "月柱": build_zhu("月柱"),
        "日柱": build_zhu("日柱"),
        "时柱": build_zhu("时柱"),
        "胎元": api_data["胎元"],
        "胎息": api_data["胎息"],
        "命宫": api_data["命宫"],
        "身宫": api_data["身宫"],
        "神煞": {
            "年柱": build_shensha("年柱"),
            "月柱": build_shensha("月柱"),
            "日柱": build_shensha("日柱"),
            "时柱": build_shensha("时柱")
        },
        "大运": {
            "起运日期": api_data["大运_起运日期"],
            "起运年龄": api_data["大运_起运年龄"],
            "大运列表": build_daying_list()
        },
        "刑冲合会": build_xing_chong_he_hui()
    }

    return result


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching BaZi data from external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - 性别 (str): Gender, either "男" or "女"
        - 阳历 (str): Gregorian birth datetime, format "YYYY-MM-DD HH:MM:SS"
        - 农历 (str): Lunar date and time description in Chinese
        - 八字 (str): Four pillars in Ganzhi format, e.g., "甲子 乙丑 丙寅 丁卯"
        - 生肖 (str): Chinese zodiac animal
        - 日主 (str): Day stem representing the self
        - 年柱_天干_天干 (str): Year pillar's heavenly stem character
        - 年柱_天干_五行 (str): Five element of year's stem
        - 年柱_天干_阴阳 (str): Yin/Yang of year's stem
        - 年柱_天干_十神 (str): Ten gods classification of year's stem
        - 年柱_地支_地支 (str): Year pillar's earthly branch character
        - 年柱_地支_五行 (str): Five element of year's branch
        - 年柱_地支_阴阳 (str): Yin/Yang of year's branch
        - 年柱_地支_藏干 (str): Hidden stems in year's branch
        - 年柱_纳音 (str): Naying (elemental resonance) of year pillar
        - 年柱_旬 (str): Xun (ten-day cycle) of year pillar
        - 年柱_空亡 (str): Kongwang (empty) of year pillar
        - 年柱_星运 (str): Star fortune of year pillar
        - 年柱_自坐 (str): Self-seat of year pillar
        - 月柱_天干_天干 (str): Month pillar's heavenly stem character
        - 月柱_天干_五行 (str): Five element of month's stem
        - 月柱_天干_阴阳 (str): Yin/Yang of month's stem
        - 月柱_天干_十神 (str): Ten gods classification of month's stem
        - 月柱_地支_地支 (str): Month pillar's earthly branch character
        - 月柱_地支_五行 (str): Five element of month's branch
        - 月柱_地支_阴阳 (str): Yin/Yang of month's branch
        - 月柱_地支_藏干 (str): Hidden stems in month's branch
        - 月柱_纳音 (str): Naying of month pillar
        - 月柱_旬 (str): Xun of month pillar
        - 月柱_空亡 (str): Kongwang of month pillar
        - 月柱_星运 (str): Star fortune of month pillar
        - 月柱_自坐 (str): Self-seat of month pillar
        - 日柱_天干_天干 (str): Day pillar's heavenly stem character
        - 日柱_天干_五行 (str): Five element of day's stem
        - 日柱_天干_阴阳 (str): Yin/Yang of day's stem
        - 日柱_天干_十神 (str): Ten gods classification of day's stem
        - 日柱_地支_地支 (str): Day pillar's earthly branch character
        - 日柱_地支_五行 (str): Five element of day's branch
        - 日柱_地支_阴阳 (str): Yin/Yang of day's branch
        - 日柱_地支_藏干 (str): Hidden stems in day's branch
        - 日柱_纳音 (str): Naying of day pillar
        - 日柱_旬 (str): Xun of day pillar
        - 日柱_空亡 (str): Kongwang of day pillar
        - 日柱_星运 (str): Star fortune of day pillar
        - 日柱_自坐 (str): Self-seat of day pillar
        - 时柱_天干_天干 (str): Hour pillar's heavenly stem character
        - 时柱_天干_五行 (str): Five element of hour's stem
        - 时柱_天干_阴阳 (str): Yin/Yang of hour's stem
        - 时柱_天干_十神 (str): Ten gods classification of hour's stem
        - 时柱_地支_地支 (str): Hour pillar's earthly branch character
        - 时柱_地支_五行 (str): Five element of hour's branch
        - 时柱_地支_阴阳 (str): Yin/Yang of hour's branch
        - 时柱_地支_藏干 (str): Hidden stems in hour's branch
        - 时柱_纳音 (str): Naying of hour pillar
        - 时柱_旬 (str): Xun of hour pillar
        - 时柱_空亡 (str): Kongwang of hour pillar
        - 时柱_星运 (str): Star fortune of hour pillar
        - 时柱_自坐 (str): Self-seat of hour pillar
        - 胎元 (str): Taiyuan (fetal origin) in Ganzhi
        - 胎息 (str): Taixi (fetal breath) in Ganzhi
        - 命宫 (str): Minggong (destiny palace) in Ganzhi
        - 身宫 (str): Shengong (body palace) in Ganzhi
        - 神煞_年柱_0 (str): First shensha for year pillar
        - 神煞_月柱_0 (str): First shensha for month pillar
        - 神煞_日柱_0 (str): First shensha for day pillar
        - 神煞_时柱_0 (str): First shensha for hour pillar
        - 大运_起运日期 (str): Start date of Da Yun
        - 大运_起运年龄 (int): Starting age of Da Yun
        - 大运_干支_0 (str): First Da Yun pillar
        - 大运_开始年份_0 (int): Start year of first Da Yun
        - 大运_结束年份_0 (int): End year of first Da Yun
        - 大运_天干十神_0 (str): Ten gods of stem for first Da Yun
        - 大运_地支十神_0 (str): Ten gods of branch for first Da Yun
        - 大运_地支藏干_0 (str): Hidden stems in branch of first Da Yun
        - 大运_开始年龄_0 (int): Starting age of first Da Yun
        - 大运_结束年龄_0 (int): Ending age of first Da Yun
        - 刑冲合会_年柱_天干 (str): Xing-Chong-He-Hui for year pillar's stem
        - 刑冲合会_年柱_地支 (str): Xing-Chong-He-Hui for year pillar's branch
        - 刑冲合会_年柱_拱 (str): Gua (arch) relation for year pillar
        - 刑冲合会_年柱_双冲 (str): Double clash for year pillar
        - 刑冲合会_月柱_天干 (str): Xing-Chong-He-Hui for month pillar's stem
        - 刑冲合会_月柱_地支 (str): Xing-Chong-He-Hui for month pillar's branch
        - 刑冲合会_月柱_拱 (str): Gua relation for month pillar
        - 刑冲合会_月柱_双冲 (str): Double clash for month pillar
        - 刑冲合会_日柱_天干 (str): Xing-Chong-He-Hui for day pillar's stem
        - 刑冲合会_日柱_地支 (str): Xing-Chong-He-Hui for day pillar's branch
        - 刑冲合会_日柱_拱 (str): Gua relation for day pillar
        - 刑冲合会_日柱_双冲 (str): Double clash for day pillar
        - 刑冲合会_时柱_天干 (str): Xing-Chong-He-Hui for hour pillar's stem
        - 刑冲合会_时柱_地支 (str): Xing-Chong-He-Hui for hour pillar's branch
        - 刑冲合会_时柱_拱 (str): Gua relation for hour pillar
        - 刑冲合会_时柱_双冲 (str): Double clash for hour pillar
    """
    return {
        "性别": "男" if gender == 1 else "女",
        "阳历": "2000-05-15 12:00:00",
        "农历": "二〇〇〇年五月十五 午时",
        "八字": "庚辰 癸未 丙午 甲午",
        "生肖": "龙",
        "日主": "丙",
        "年柱_天干_天干": "庚",
        "年柱_天干_五行": "金",
        "年柱_天干_阴阳": "阳",
        "年柱_天干_十神": "偏财",
        "年柱_地支_地支": "辰",
        "年柱_地支_五行": "土",
        "年柱_地支_阴阳": "阳",
        "年柱_地支_藏干": "戊乙癸",
        "年柱_纳音": "白蜡金",
        "年柱_旬": "甲戌旬",
        "年柱_空亡": "寅卯",
        "年柱_星运": "冠带",
        "年柱_自坐": "养",
        "月柱_天干_天干": "癸",
        "月柱_天干_五行": "水",
        "月柱_天干_阴阳": "阴",
        "月柱_天干_十神": "正官",
        "月柱_地支_地支": "未",
        "月柱_地支_五行": "土",
        "月柱_地支_阴阳": "阴",
        "月柱_地支_藏干": "己丁乙",
        "月柱_纳音": "杨柳木",
        "月柱_旬": "甲戌旬",
        "月柱_空亡": "午未",
        "月柱_星运": "墓",
        "月柱_自坐": "衰",
        "日柱_天干_天干": "丙",
        "日柱_天干_五行": "火",
        "日柱_天干_阴阳": "阳",
        "日柱_天干_十神": "日主",
        "日柱_地支_地支": "午",
        "日柱_地支_五行": "火",
        "日柱_地支_阴阳": "阳",
        "日柱_地支_藏干": "丁己",
        "日柱_纳音": "天河水",
        "日柱_旬": "甲辰旬",
        "日柱_空亡": "寅卯",
        "日柱_星运": "帝旺",
        "日柱_自坐": "帝旺",
        "时柱_天干_天干": "甲",
        "时柱_天干_五行": "木",
        "时柱_天干_阴阳": "阳",
        "时柱_天干_十神": "偏印",
        "时柱_地支_地支": "午",
        "时柱_地支_五行": "火",
        "时柱_地支_阴阳": "阳",
        "时柱_地支_藏干": "丁己",
        "时柱_纳音": "沙中金",
        "时柱_旬": "甲午旬",
        "时柱_空亡": "辰巳",
        "时柱_星运": "帝旺",
        "时柱_自坐": "死",
        "胎元": "甲戌",
        "胎息": "戊子",
        "命宫": "戊子",
        "身宫": "壬辰",
        "神煞_年柱_0": "国印",
        "神煞_月柱_0": "天乙贵人",
        "神煞_日柱_0": "文昌贵人",
        "神煞_时柱_0": "羊刃",
        "大运_起运日期": "2007-08-15",
        "大运_起运年龄": 7,
        "大运_干支_0": "壬午",
        "大运_开始年份_0": 2007,
        "大运_结束年份_0": 2016,
        "大运_天干十神_0": "七杀",
        "大运_地支十神_0": "劫财",
        "大运_地支藏干_0": "丁己",
        "大运_开始年龄_0": 7,
        "大运_结束年龄_0": 16,
        "刑冲合会_年柱_天干": "无",
        "刑冲合会_年柱_地支": "辰戌冲",
        "刑冲合会_年柱_拱": "申子辰合水",
        "刑冲合会_年柱_双冲": "无",
        "刑冲合会_月柱_天干": "癸丁克",
        "刑冲合会_月柱_地支": "丑未冲",
        "刑冲合会_月柱_拱": "亥卯未合木",
        "刑冲合会_月柱_双冲": "无",
        "刑冲合会_日柱_天干": "丙辛合水",
        "刑冲合会_日柱_地支": "午午自刑",
        "刑冲合会_日柱_拱": "寅午戌合火",
        "刑冲合会_日柱_双冲": "子午冲",
        "刑冲合会_时柱_天干": "甲己合土",
        "刑冲合会_时柱_地支": "午午自刑",
        "刑冲合会_时柱_拱": "寅午戌合火",
        "刑冲合会_时柱_双冲": "子午冲"
    }