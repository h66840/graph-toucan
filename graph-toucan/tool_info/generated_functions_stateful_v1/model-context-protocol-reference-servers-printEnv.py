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
    Simulates fetching environment variables from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - env_0_key (str): First environment variable name
        - env_0_value (str): First environment variable value
        - env_1_key (str): Second environment variable name
        - env_1_value (str): Second environment variable value
    """
    return {
        "env_0_key": "PATH",
        "env_0_value": "/usr/local/bin:/usr/bin:/bin",
        "env_1_key": "HOME",
        "env_1_value": "/home/user"
    }


def model_context_protocol_reference_servers_printEnv() -> Dict[str, Dict[str, str]]:
    """
    Prints all environment variables, helpful for debugging MCP server configuration.

    Returns:
        Dict containing a single key 'environment_variables' mapping environment variable names to their string values.
    """
    try:
        # Use the external API simulation to get environment variables instead of os.environ
        api_data = call_external_api("model-context-protocol-reference-servers-printEnv", **locals())
        env_vars = {
            api_data["env_0_key"]: api_data["env_0_value"],
            api_data["env_1_key"]: api_data["env_1_value"]
        }

        return {
            "environment_variables": env_vars
        }

    except Exception as e:
        # In case of any error, return empty environment variables dict
        return {
            "environment_variables": {}
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
