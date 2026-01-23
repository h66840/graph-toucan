from typing import Dict, List, Any

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
    Simulates fetching data from external API for the command-line MCP server.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - platform_info (str): Information about the current operating platform
        - command_availability_note (str): Note about available command types
        - available_commands_0_name (str): Name of the first allowed command
        - available_commands_0_description (str): Description of the first allowed command
        - available_commands_1_name (str): Name of the second allowed command
        - available_commands_1_description (str): Description of the second allowed command
        - execution_privilege_note (str): Note about execution privilege level
    """
    return {
        "platform_info": "Windows Server 2022",
        "command_availability_note": "Only Windows CMD and PowerShell commands are supported; Unix shell commands are not available.",
        "available_commands_0_name": "dir",
        "available_commands_0_description": "Lists files and directories in the current directory.",
        "available_commands_1_name": "ipconfig",
        "available_commands_1_description": "Displays IP configuration details for all network interfaces.",
        "execution_privilege_note": "All commands are executed with standard user privileges unless elevated explicitly."
    }

def windows_command_line_mcp_server_list_allowed_commands() -> Dict[str, Any]:
    """
    List all commands that are allowed to be executed by this server. This helps understand what operations are permitted.

    Returns:
        Dict containing:
        - platform_info (str): information about the current operating platform, including whether it is non-Windows and the specific OS name
        - command_availability_note (str): note explaining which types of commands are generally available or unavailable (e.g., Unix vs Windows)
        - available_commands (List[Dict]): list of allowed commands, each with 'name' and 'description' fields indicating the command and its purpose
        - execution_privilege_note (str): note specifying the privilege level at which all commands are executed
    """
    # Fetch data from simulated external API
    api_data = call_external_api("windows-command-line-mcp-server-list_allowed_commands", **locals())

    # Construct the list of available commands from indexed fields
    available_commands = [
        {
            "name": api_data["available_commands_0_name"],
            "description": api_data["available_commands_0_description"]
        },
        {
            "name": api_data["available_commands_1_name"],
            "description": api_data["available_commands_1_description"]
        }
    ]

    # Build final result dictionary matching the output schema
    result = {
        "platform_info": api_data["platform_info"],
        "command_availability_note": api_data["command_availability_note"],
        "available_commands": available_commands,
        "execution_privilege_note": api_data["execution_privilege_note"]
    }

    return result

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
