from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PowerShell execution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - stdout (str): Standard output from the PowerShell script execution
        - stderr (str): Error output from the PowerShell script execution
        - exit_code (int): Exit code of the PowerShell process
        - success (bool): Whether the PowerShell command executed successfully
    """
    return {
        "stdout": "PowerShell script executed successfully.",
        "stderr": "",
        "exit_code": 0,
        "success": True
    }

def windows_command_line_mcp_server_execute_powershell(
    script: str, 
    timeout: Optional[int] = None, 
    workingDir: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute a PowerShell script and return its output.
    
    This function simulates the execution of a PowerShell script by calling an external API
    that returns the result of the script execution, including standard output, error output,
    exit code, and success status.
    
    Args:
        script (str): PowerShell script to execute (required)
        timeout (Optional[int]): Timeout in milliseconds (optional)
        workingDir (Optional[str]): Working directory for the script (optional)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - stdout (str): Standard output from the PowerShell script execution
            - stderr (str): Error output from the PowerShell script execution, if any
            - exit_code (int): Exit code of the PowerShell process; 0 typically indicates success
            - success (bool): Whether the PowerShell command executed successfully based on exit code and absence of critical errors
    
    Raises:
        ValueError: If script is empty or None
    """
    # Input validation
    if not script:
        raise ValueError("Script parameter is required and cannot be empty")
    
    if not isinstance(script, str):
        raise ValueError("Script parameter must be a string")
    
    if timeout is not None and (not isinstance(timeout, int) or timeout <= 0):
        raise ValueError("Timeout must be a positive integer if specified")
    
    if workingDir is not None and not isinstance(workingDir, str):
        raise ValueError("Working directory must be a string if specified")
    
    # Call external API to simulate PowerShell execution
    api_data = call_external_api("windows-command-line-mcp-server-execute_powershell")
    
    # Construct result matching output schema
    result = {
        "stdout": api_data["stdout"],
        "stderr": api_data["stderr"],
        "exit_code": api_data["exit_code"],
        "success": api_data["success"]
    }
    
    return result