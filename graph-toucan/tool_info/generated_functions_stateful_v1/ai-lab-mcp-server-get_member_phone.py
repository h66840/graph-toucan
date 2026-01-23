from typing import Dict, Any

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
    Simulates fetching data from external API for AI Lab member phone information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - phone (str): The phone number of the specified AI Lab member
    """
    # Simulated response from external API
    return {
        "phone": "13800138000"
    }

def ai_lab_mcp_server_get_member_phone(name: str) -> Dict[str, Any]:
    """
    获取AI实验室的成员的手机号
    
    Args:
        name (str): 成员名，必须提供
    
    Returns:
        Dict[str, Any]: 包含成员手机号的字典，格式为 {"phone": "手机号"}
    
    Raises:
        ValueError: 当name为空或非字符串类型时抛出异常
    """
    # Input validation
    if not name:
        raise ValueError("Member name is required")
    if not isinstance(name, str):
        raise ValueError("Member name must be a string")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("ai-lab-mcp-server-get_member_phone", **locals())
    
    # Construct result matching output schema
    result = {
        "phone": api_data["phone"]
    }
    
    return result

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        pass
    except Exception:
        pass
    return result
