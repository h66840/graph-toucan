from typing import Dict, List, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching artifact data from external API for the given tool.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - error (str): Error message if any, otherwise empty string
        - name (str): Name of the artifact set
        - two_piece_effect (str): Effect description for 2-piece set
        - five_piece_effect (str): Effect description for 5-piece set
        - corresponding_area (str): Name of the Anomaly Zone where the artifact drops
        - cost_4_harmonies_0 (str): First 4-harmony cost 声骸 name
        - cost_4_harmonies_1 (str): Second 4-harmony cost 声骸 name
        - cost_3_harmonies_0 (str): First 3-harmony cost 声骸 name
        - cost_3_harmonies_1 (str): Second 3-harmony cost 声骸 name
        - cost_1_harmonies_0 (str): First 1-harmony cost 声骸 name
        - cost_1_harmonies_1 (str): Second 1-harmony cost 声骸 name
    """
    # Simulated response data with flat structure
    return {
        "error": "",
        "name": "幽锁深涧",
        "two_piece_effect": "提升15%攻击力。",
        "five_piece_effect": "施放共鸣技能后，提升30%共鸣技能伤害，持续10秒。",
        "corresponding_area": "无音区·深谷回响",
        "cost_4_harmonies_0": "幽锁之主·头骨",
        "cost_4_harmonies_1": "幽锁之主·脊椎",
        "cost_3_harmonies_0": "深涧守望者·利齿",
        "cost_3_harmonies_1": "深涧守望者·利爪",
        "cost_1_harmonies_0": "回响残音·触须",
        "cost_1_harmonies_1": "回响残音·碎片"
    }

def 鸣潮_mcp_server_get_artifact_info(artifact_name: str) -> Dict[str, Any]:
    """
    获取库街区上的声骸详细信息并以 Markdown 格式返回。

    Args:
        artifact_name (str): 要查询的声骸套装的中文名称。

    Returns:
        Dict containing the following keys:
        - error (str): 错误消息，若未找到声骸或获取失败
        - name (str): 声骸套装名称
        - two_piece_effect (str): 两件套效果描述
        - five_piece_effect (str): 五件套效果描述
        - corresponding_area (str): 掉落区域（无音区）名称
        - cost_4_harmonies (List[str]): 消耗4点协音的声骸名称列表
        - cost_3_harmonies (List[str]): 消耗3点协音的声骸名称列表
        - cost_1_harmonies (List[str]): 消耗1点协音的声骸名称列表
    """
    # Input validation
    if not artifact_name or not isinstance(artifact_name, str):
        return {
            "error": "Invalid input: artifact_name must be a non-empty string.",
            "name": "",
            "two_piece_effect": "",
            "five_piece_effect": "",
            "corresponding_area": "",
            "cost_4_harmonies": [],
            "cost_3_harmonies": [],
            "cost_1_harmonies": []
        }

    # Fetch data from simulated external API
    try:
        api_data = call_external_api("鸣潮-mcp-server-get_artifact_info", **locals())
    except Exception as e:
        return {
            "error": f"Failed to retrieve data: {str(e)}",
            "name": "",
            "two_piece_effect": "",
            "five_piece_effect": "",
            "corresponding_area": "",
            "cost_4_harmonies": [],
            "cost_3_harmonies": [],
            "cost_1_harmonies": []
        }

    # Extract and construct nested output structure
    error = api_data.get("error", "")
    if error:
        return {
            "error": error,
            "name": "",
            "two_piece_effect": "",
            "five_piece_effect": "",
            "corresponding_area": "",
            "cost_4_harmonies": [],
            "cost_3_harmonies": [],
            "cost_1_harmonies": []
        }

    # Construct lists from indexed fields
    cost_4_harmonies = []
    if api_data.get("cost_4_harmonies_0"): cost_4_harmonies.append(api_data["cost_4_harmonies_0"])
    if api_data.get("cost_4_harmonies_1"): cost_4_harmonies.append(api_data["cost_4_harmonies_1"])

    cost_3_harmonies = []
    if api_data.get("cost_3_harmonies_0"): cost_3_harmonies.append(api_data["cost_3_harmonies_0"])
    if api_data.get("cost_3_harmonies_1"): cost_3_harmonies.append(api_data["cost_3_harmonies_1"])

    cost_1_harmonies = []
    if api_data.get("cost_1_harmonies_0"): cost_1_harmonies.append(api_data["cost_1_harmonies_0"])
    if api_data.get("cost_1_harmonies_1"): cost_1_harmonies.append(api_data["cost_1_harmonies_1"])

    # Final structured output
    result = {
        "error": "",
        "name": api_data.get("name", ""),
        "two_piece_effect": api_data.get("two_piece_effect", ""),
        "five_piece_effect": api_data.get("five_piece_effect", ""),
        "corresponding_area": api_data.get("corresponding_area", ""),
        "cost_4_harmonies": cost_4_harmonies,
        "cost_3_harmonies": cost_3_harmonies,
        "cost_1_harmonies": cost_1_harmonies
    }

    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
