from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching character data from external API for the given tool.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - character_name (str): The queried character's Chinese name
        - error_message (str): Error message if data retrieval failed
        - markdown_content (str): Full Markdown-formatted content with character details when successful
    """
    # Simulated API response with only flat, simple fields
    return {
        "character_name": "湮灭者",
        "error_message": "",
        "markdown_content": (
            "# 湮灭者\n\n"
            "## 角色简介\n"
            "湮灭者是一位来自深渊的神秘战士，掌控着毁灭之力。\n\n"
            "## 技能介绍\n"
            "- **普通攻击：裂空斩**\n  连续挥砍造成物理伤害。\n"
            "- **特殊技能：湮灭冲击**\n  释放能量波对前方敌人造成大量暗元素伤害。\n"
            "- **终极技：终焉降临**\n  召唤黑洞吞噬敌人，持续造成真实伤害。\n\n"
            "## 养成攻略\n"
            "- 推荐武器：虚空之刃\n"
            "- 推荐圣遗物：深渊套装\n"
            "- 属性加点优先级：攻击力 > 暴击率 > 穿透\n\n"
            "## 材料需求\n"
            "- 等级突破材料：暗核 ×40、黑曜石 ×60\n"
            "- 技能升级材料：毁灭之证 ×30、混沌精华 ×20"
        )
    }

def 鸣潮_mcp_server_get_character_info(character_name: str) -> Dict[str, Any]:
    """
    获取库街区上的角色详细信息包括角色技能，养成攻略等，并以 Markdown 格式返回。

    Args:
        character_name (str): 要查询的角色的中文名称。

    Returns:
        Dict containing:
        - character_name (str): name of the character in Chinese as queried
        - error_message (str, optional): error message when data retrieval fails
        - markdown_content (str, optional): full Markdown-formatted string with character details if successful
    """
    # Input validation
    if not character_name or not isinstance(character_name, str):
        return {
            "character_name": "",
            "error_message": "Invalid input: character_name must be a non-empty string."
        }

    # Call simulated external API
    api_data = call_external_api("鸣潮_mcp_server_get_character_info")

    # Construct result based on API response
    result: Dict[str, Any] = {
        "character_name": api_data.get("character_name", "")
    }

    error_message = api_data.get("error_message", "")
    markdown_content = api_data.get("markdown_content", "")

    if error_message:
        result["error_message"] = error_message
    else:
        result["markdown_content"] = markdown_content

    return result