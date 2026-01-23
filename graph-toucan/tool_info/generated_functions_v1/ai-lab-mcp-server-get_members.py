from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - member_0 (str): Name of the first AI Lab member
        - member_1 (str): Name of the second AI Lab member
    """
    return {
        "member_0": "Zhang San",
        "member_1": "Li Si"
    }

def ai_lab_mcp_server_get_members() -> List[str]:
    """
    获取AI实验室的成员列表。
    
    Returns:
        List[str]: AI实验室成员姓名列表
    """
    try:
        # 调用外部API获取数据（模拟）
        api_data = call_external_api("ai-lab-mcp-server-get_members")
        
        # 构造符合输出schema的列表结构
        members = [
            api_data["member_0"],
            api_data["member_1"]
        ]
        
        return members
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching AI Lab members: {e}")