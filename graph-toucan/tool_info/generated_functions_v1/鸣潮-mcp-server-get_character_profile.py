from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching character profile data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - character_name (str): Character's Chinese name
        - key_attributes_共鸣类型 (str): Resonance type
        - key_attributes_超频诊断结果 (str): Overclock diagnosis result
        - key_attributes_体温特征 (str): Body temperature characteristic
        - profile_sections_0_title (str): First section title
        - profile_sections_0_content (str): First section content in Markdown
        - profile_sections_1_title (str): Second section title
        - profile_sections_1_content (str): Second section content in Markdown
        - valuable_items_0_name (str): First valued item name
        - valuable_items_0_description (str): Description of first valued item
        - valuable_items_1_name (str): Second valued item name
        - valuable_items_1_description (str): Description of second valued item
        - background_stories_0_title (str): First background story title
        - background_stories_0_narrative (str): Narrative of first background story
        - background_stories_1_title (str): Second background story title
        - background_stories_1_narrative (str): Narrative of second background story
        - special_ability_name (str): Name of special ability or dish
        - special_ability_effect (str): Effect description
        - special_ability_scope (str): Scope of effect
        - special_ability_duration (str): Duration of effect
    """
    return {
        "character_name": "凌夜",
        "key_attributes_共鸣类型": "湮灭",
        "key_attributes_超频诊断结果": "稳定",
        "key_attributes_体温特征": "低温",
        "profile_sections_0_title": "基础信息",
        "profile_sections_0_content": "**姓名**：凌夜\n\n**代号**：影刃\n\n**所属势力**：黑核研究所",
        "profile_sections_1_title": "战斗特性",
        "profile_sections_1_content": "擅长暗影突袭，可在短时间内连续闪现三次，对敌人造成多段伤害。",
        "valuable_items_0_name": "旧式怀表",
        "valuable_items_0_description": "据说是母亲留下的唯一遗物，即使停摆也始终带在身边。",
        "valuable_items_1_name": "黑色护腕",
        "valuable_items_1_description": "由前队友赠送，内嵌微型共振装置，用于稳定共鸣频率。",
        "background_stories_0_title": "孤影往事",
        "background_stories_0_narrative": "凌夜曾是秘密实验的幸存者，在一次黑核暴走事件中失去了整个小队。",
        "background_stories_1_title": "觉醒之刻",
        "background_stories_1_narrative": "在濒死之际，体内的湮灭共鸣被意外激活，吞噬了周围所有能量。",
        "special_ability_name": "影袭",
        "special_ability_effect": "短时间内提升移动速度与攻击频率",
        "special_ability_scope": "自身",
        "special_ability_duration": "10秒"
    }

def 鸣潮_mcp_server_get_character_profile(character_name: str) -> Dict[str, Any]:
    """
    获取库街区上的角色档案信息并以 Markdown 格式返回。

    Args:
        character_name (str): 要查询的角色的中文名称。

    Returns:
        Dict containing:
        - character_name (str): 角色的中文名称
        - profile_sections (List[Dict]): 包含角色档案各个部分的列表，每个部分为一个字典，包含 'title' 和 'content'
        - key_attributes (Dict): 角色关键属性摘要
        - valuable_items (List[Dict]): 角色珍视之物的列表
        - background_stories (List[Dict]): 角色背景故事章节列表
        - special_ability (Dict): 角色特殊能力或料理效果
    """
    if not character_name or not isinstance(character_name, str):
        return {
            "error": "角色名称不能为空且必须为字符串"
        }

    try:
        api_data = call_external_api("鸣潮-mcp-server-get_character_profile")
        
        # 构建嵌套结构
        result = {
            "character_name": api_data["character_name"],
            "key_attributes": {
                "共鸣类型": api_data["key_attributes_共鸣类型"],
                "超频诊断结果": api_data["key_attributes_超频诊断结果"],
                "体温特征": api_data["key_attributes_体温特征"]
            },
            "profile_sections": [
                {
                    "title": api_data["profile_sections_0_title"],
                    "content": api_data["profile_sections_0_content"]
                },
                {
                    "title": api_data["profile_sections_1_title"],
                    "content": api_data["profile_sections_1_content"]
                }
            ],
            "valuable_items": [
                {
                    "name": api_data["valuable_items_0_name"],
                    "description": api_data["valuable_items_0_description"]
                },
                {
                    "name": api_data["valuable_items_1_name"],
                    "description": api_data["valuable_items_1_description"]
                }
            ],
            "background_stories": [
                {
                    "title": api_data["background_stories_0_title"],
                    "narrative": api_data["background_stories_0_narrative"]
                },
                {
                    "title": api_data["background_stories_1_title"],
                    "narrative": api_data["background_stories_1_narrative"]
                }
            ],
            "special_ability": {
                "name": api_data["special_ability_name"],
                "effect": api_data["special_ability_effect"],
                "scope": api_data["special_ability_scope"],
                "duration": api_data["special_ability_duration"]
            }
        }
        
        return result
        
    except Exception as e:
        return {
            "error": f"获取角色档案失败: {str(e)}"
        }