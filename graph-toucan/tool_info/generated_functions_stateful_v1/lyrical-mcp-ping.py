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
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - response (str): the response message from the server indicating its availability status
    """
    return {
        "response": "Server is responsive and operational"
    }


def lyrical_mcp_ping() -> Dict[str, str]:
    """
    Simple ping tool to test server responsiveness and prevent timeouts.

    This function simulates a ping to a server by calling an external API
    and retrieving a status message about the server's availability.

    Returns:
        Dict containing:
        - response (str): the response message from the server indicating its availability status
    """
    try:
        # Call external API to get ping response
        api_data = call_external_api("lyrical-mcp-ping", **locals())

        # Construct result matching output schema
        result = {
            "response": api_data["response"]
        }

        return result

    except KeyError as e:
        return {
            "response": f"Error: Missing expected data field {str(e)}"
        }
    except Exception as e:
        return {
            "response": f"Error occurred during ping: {str(e)}"
        }

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
