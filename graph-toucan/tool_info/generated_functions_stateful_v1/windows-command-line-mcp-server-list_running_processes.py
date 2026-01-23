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
    Simulates fetching data from external API for listing running processes.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - process_0_pid (int): PID of first process
        - process_0_user (str): User running first process
        - process_0_time (str): CPU time used by first process
        - process_0_command (str): Command line of first process
        - process_1_pid (int): PID of second process
        - process_1_user (str): User running second process
        - process_1_time (str): CPU time used by second process
        - process_1_command (str): Command line of second process
    """
    return {
        "process_0_pid": 1234,
        "process_0_user": "SYSTEM",
        "process_0_time": "00:00:15",
        "process_0_command": "System Idle Process",
        "process_1_pid": 5678,
        "process_1_user": "Alice",
        "process_1_time": "00:01:30",
        "process_1_command": "chrome.exe --type=renderer"
    }

def windows_command_line_mcp_server_list_running_processes(filter: Optional[str] = None) -> Dict[str, Any]:
    """
    List all running processes on the system. Can be filtered by providing an optional filter string 
    that will match against process names.
    
    Args:
        filter (Optional[str]): Optional filter string to match against process names. 
                               If provided, only processes whose command contains this string will be returned.
    
    Returns:
        Dict containing a list of running processes, each with 'pid', 'user', 'time', and 'command' fields.
    
    Example:
        {
            "processes": [
                {
                    "pid": 1234,
                    "user": "SYSTEM",
                    "time": "00:00:15",
                    "command": "System Idle Process"
                },
                {
                    "pid": 5678,
                    "user": "Alice",
                    "time": "00:01:30",
                    "command": "chrome.exe --type=renderer"
                }
            ]
        }
    """
    # Fetch raw data from simulated external API
    api_data = call_external_api("windows-command-line-mcp-server-list_running_processes", **locals())
    
    # Construct list of processes from flattened API response
    processes = []
    
    # Process index 0
    if "process_0_pid" in api_data:
        process_0 = {
            "pid": api_data["process_0_pid"],
            "user": api_data["process_0_user"],
            "time": api_data["process_0_time"],
            "command": api_data["process_0_command"]
        }
        processes.append(process_0)
    
    # Process index 1
    if "process_1_pid" in api_data:
        process_1 = {
            "pid": api_data["process_1_pid"],
            "user": api_data["process_1_user"],
            "time": api_data["process_1_time"],
            "command": api_data["process_1_command"]
        }
        processes.append(process_1)
    
    # Apply filter if provided
    if filter is not None:
        filtered_processes = []
        for proc in processes:
            if filter.lower() in proc["command"].lower():
                filtered_processes.append(proc)
        processes = filtered_processes
    
    return {"processes": processes}

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
