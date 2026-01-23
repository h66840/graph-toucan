from typing import Dict, Any, Optional
import sys


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PowerShell execution.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - output (str): Simulated raw output from PowerShell command execution
        - error (str): Simulated error message if execution failed
    """
    # Simulate successful command output
    return {
        "output": "Command executed successfully\nValue: 42\nStatus: OK",
        "error": ""
    }


def powershell_exec_server_run_powershell(code: str, ctx: Optional[Any] = None, timeout: Optional[int] = 60) -> Dict[str, str]:
    """
    Execute PowerShell commands securely.

    Args:
        code (str): PowerShell code to execute (required)
        ctx (Any, optional): MCP context for logging and progress reporting
        timeout (int, optional): Command timeout in seconds (1-300, default 60)

    Returns:
        Dict[str, str]: Dictionary containing:
            - output (str): Raw output from the PowerShell command execution, including any printed messages, errors, or results
            - error (str): Error message if the PowerShell execution failed, such as system-level errors

    Raises:
        ValueError: If code is empty or timeout is not in valid range
        RuntimeError: If subprocess fails to start
    """
    # Input validation
    if not code or not code.strip():
        return {
            "output": "",
            "error": "PowerShell code is required and cannot be empty"
        }

    if timeout is None:
        timeout = 60
    elif not isinstance(timeout, int) or timeout < 1 or timeout > 300:
        return {
            "output": "",
            "error": "Timeout must be an integer between 1 and 300 seconds"
        }

    try:
        # Use the simulated API call instead of actual subprocess execution
        api_result = call_external_api("powershell_exec")
        
        # Return the simulated output and error
        return {
            "output": api_result["output"],
            "error": api_result["error"]
        }

    except Exception as e:
        return {
            "output": "",
            "error": f"Failed to execute PowerShell command: {str(e)}"
        }