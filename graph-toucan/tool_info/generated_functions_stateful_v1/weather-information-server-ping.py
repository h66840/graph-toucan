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
        - response (str): the server's response indicating its availability, typically "pong" when reachable
    """
    return {
        "response": "pong"
    }


def weather_information_server_ping() -> Dict[str, Any]:
    """
    Simple ping tool to test server responsiveness and prevent timeouts.

    This function simulates a ping to the weather information server by calling an external API
    and returning the server's response. It is used to check if the server is reachable and responsive.

    Returns:
        Dict[str, Any]: A dictionary containing the server's response with the following structure:
            - response (str): the server's response indicating its availability, typically "pong" when reachable
    """
    try:
        # Call external API to get the response
        api_data = call_external_api("weather-information-server-ping", **locals())

        # Construct the result dictionary matching the output schema
        result = {
            "response": api_data["response"]
        }

        return result

    except Exception as e:
        # In case of any error, return an error response
        return {
            "response": f"error: {str(e)}"
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
