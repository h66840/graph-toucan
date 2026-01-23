from typing import Dict, List, Any, Optional
import time
import json

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
    Simulates fetching data from external API for PowerShell execution.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - output (str): Standard output from PowerShell command
        - error (str): Error message if any occurred
        - success (bool): True if command succeeded
        - execution_time (float): Duration of execution in seconds
        - timed_out (bool): True if command timed out
        - exit_code (int): Exit code of PowerShell process
        - progress_messages_0 (str): First progress message
        - progress_messages_1 (str): Second progress message
        - metadata_timestamp (str): Execution timestamp
        - metadata_server_id (str): Identifier of the server
        - metadata_session_id (str): Session identifier
    """
    return {
        "output": "Command executed successfully.\nTotal items processed: 100",
        "error": "",
        "success": True,
        "execution_time": 2.45,
        "timed_out": False,
        "exit_code": 0,
        "progress_messages_0": "Processing batch 1 of 5...",
        "progress_messages_1": "Processing batch 2 of 5...",
        "metadata_timestamp": "2023-10-15T14:30:00Z",
        "metadata_server_id": "PS-SRV-01",
        "metadata_session_id": "sess-abc123xyz"
    }

def powershell_exec_server_run_powershell_with_progress(
    code: str,
    ctx: Optional[Any] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Execute PowerShell commands with detailed progress reporting.

    Args:
        code (str): PowerShell code to execute
        timeout (Optional[int]): Command timeout in seconds (1-300, default 60)
        ctx (Optional[Any]): MCP context for logging and progress reporting

    Returns:
        Dict containing:
        - output (str): Standard output from the executed PowerShell command
        - error (str): Any error messages generated during execution
        - success (bool): Whether the command completed successfully
        - execution_time (float): Duration of command execution in seconds
        - timed_out (bool): Whether the command exceeded the timeout limit
        - progress_messages (List[str]): List of progress messages reported during execution
        - exit_code (int): Exit code returned by the PowerShell process
        - metadata (Dict): Additional structured information about execution environment

    Raises:
        ValueError: If timeout is not between 1 and 300 seconds
    """
    # Input validation
    if not code or not code.strip():
        raise ValueError("PowerShell code is required and cannot be empty")

    if timeout is None:
        timeout = 60
    elif not isinstance(timeout, int) or timeout < 1 or timeout > 300:
        raise ValueError("Timeout must be an integer between 1 and 300 seconds")

    # Start timing
    start_time = time.time()

    try:
        # Simulate context logging if ctx is provided
        if ctx is not None:
            try:
                if hasattr(ctx, "report_progress"):
                    ctx.report_progress("PowerShell execution started")
                if hasattr(ctx, "log"):
                    ctx.log(f"Executing PowerShell code: {code[:100]}...")
            except:
                pass  # Ignore context-related errors

        # Call external API to simulate PowerShell execution
        api_data = call_external_api("powershell-exec-server-run_powershell_with_progress", **locals())

        # Simulate execution time within timeout bounds
        simulated_duration = min(api_data["execution_time"], timeout - 0.1)
        time.sleep(min(simulated_duration, 0.1))  # Simulate minimal processing delay

        # Check if operation would have timed out (for testing purposes)
        would_timeout = simulated_duration >= timeout

        # Construct the result dictionary with proper nested structure
        result = {
            "output": api_data["output"],
            "error": api_data["error"],
            "success": api_data["success"] and not would_timeout,
            "execution_time": simulated_duration,
            "timed_out": would_timeout,
            "exit_code": api_data["exit_code"],
            "progress_messages": [
                api_data["progress_messages_0"],
                api_data["progress_messages_1"]
            ],
            "metadata": {
                "timestamp": api_data["metadata_timestamp"],
                "server_id": api_data["metadata_server_id"],
                "session_id": api_data["metadata_session_id"]
            }
        }

        # Update context with final progress if available
        if ctx is not None and hasattr(ctx, "report_progress"):
            status = "completed" if result["success"] else "failed"
            ctx.report_progress(f"PowerShell execution {status}")

        return result

    except Exception as e:
        # In case of unexpected error, return appropriate failure response
        elapsed = time.time() - start_time
        return {
            "output": "",
            "error": str(e),
            "success": False,
            "execution_time": elapsed,
            "timed_out": False,
            "progress_messages": [],
            "exit_code": -1,
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "server_id": "PS-SRV-UNKNOWN",
                "session_id": "sess-error-fallback"
            }
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
