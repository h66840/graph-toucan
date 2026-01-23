from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import re

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bazi solar time calculation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - solar_times_0 (str): First matching solar datetime string in "YYYY-MM-DD hh:mm:ss" format
        - solar_times_1 (str): Second matching solar datetime string in "YYYY-MM-DD hh:mm:ss" format
    """
    return {
        "solar_times_0": "1998-07-31 14:00:00",
        "solar_times_1": "1938-08-01 13:30:00"
    }

def bazi_calculator_getSolarTimes(bazi: str) -> Dict[str, Any]:
    """
    根据八字获取公历时间列表。返回的时间格式为：YYYY-MM-DD hh:mm:ss。
    
    该函数模拟根据输入的四柱八字（年柱、月柱、日柱、时柱）推算出可能对应的公历时间。
    由于八字存在周期性重复（60年一甲子，日柱60日一循环，时柱5日一循环），同一个八字组合
    可能对应多个公历时间点。本函数返回两个最可能的匹配时间作为示例。
    
    Args:
        bazi (str): 八字，按年柱、月柱、日柱、时柱顺序，用空格隔开。例如：戊寅 己未 己卯 辛未
        
    Returns:
        Dict[str, Any]: 包含 solar_times 字段的字典，solar_times 是匹配该八字的公历时间字符串列表，
                        每个时间字符串格式为 "YYYY-MM-DD hh:mm:ss"
                        
    Raises:
        ValueError: 当输入的八字格式不正确或不符合天干地支规则时抛出异常
    """
    # Input validation
    if not bazi or not isinstance(bazi, str):
        raise ValueError("八字输入不能为空且必须为字符串类型")
    
    # Split the bazi string
    pillars = bazi.strip().split()
    if len(pillars) != 4:
        raise ValueError("八字必须包含四个柱（年柱、月柱、日柱、时柱），用空格隔开")
    
    # Validate each pillar contains valid heavenly stem and earthly branch
    heavenly_stems = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    earthly_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    for i, pillar in enumerate(pillars):
        if len(pillar) != 2:
            raise ValueError(f"{['年柱', '月柱', '日柱', '时柱'][i]}必须由两个汉字组成")
        
        stem, branch = pillar[0], pillar[1]
        if stem not in heavenly_stems:
            raise ValueError(f"{['年柱', '月柱', '日柱', '时柱'][i]}天干不合法：{stem}")
        if branch not in earthly_branches:
            raise ValueError(f"{['年柱', '月柱', '日柱', '时柱'][i]}地支不合法：{branch}")
    
    # In a real implementation, this would involve complex astronomical calculations
    # and historical calendar conversions. Here we simulate the result.
    api_data = call_external_api("bazi-calculator-getSolarTimes")
    
    # Construct the result structure
    solar_times: List[str] = []
    
    # Add times from API data if they exist
    if "solar_times_0" in api_data:
        solar_times.append(api_data["solar_times_0"])
    if "solar_times_1" in api_data:
        solar_times.append(api_data["solar_times_1"])
    
    return {
        "solar_times": solar_times
    }