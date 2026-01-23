from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for remote shell command execution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - command (str): The shell command that was executed
        - working_directory (str): The working directory where the command was executed
        - success (bool): Whether the command executed successfully
        - stdout (str): Standard output from the command
        - stderr (str): Standard error output from the command
        - error_message (str): Detailed error message if command failed
    """
    return {
        "command": "ls -la",
        "working_directory": "/home/user",
        "success": True,
        "stdout": "total 24\ndrwxr-xr-x  5 user user 4096 Apr 10 10:00 .\ndrwxr-xr-x  3 root root 4096 Apr 10 09:00 ..\n-rw-r--r--  1 user user  220 Apr 10 09:00 .bash_logout",
        "stderr": "",
        "error_message": ""
    }

def remote_shell_server_shell_exec(command: str, cwd: Optional[str] = None, timeout: Optional[int] = 30000) -> Dict[str, Any]:
    """
    Execute shell commands remotely. This tool allows running shell commands on the remote system and returns the output.
    Use with caution as it can execute any command.
    
    Args:
        command (str): The shell command to execute (required)
        cwd (Optional[str]): Working directory for the command (optional)
        timeout (Optional[int]): Timeout in milliseconds (default: 30000)
    
    Returns:
        Dict containing:
        - command (str): the shell command that was executed
        - working_directory (str): the working directory where the command was executed
        - success (bool): whether the command executed successfully
        - stdout (str): standard output from the command, empty if none
        - stderr (str): standard error output from the command, empty if none
        - error_message (str): detailed error message if the command failed, otherwise empty
    
    Raises:
        ValueError: If command is empty or None
    """
    # Input validation
    if not command or not command.strip():
        raise ValueError("Command parameter is required and cannot be empty")
    
    # Prepare parameters for API call
    if cwd is None:
        cwd = ""
    
    # Call external API (simulation)
    api_data = call_external_api("remote-shell-server-shell-exec")
    
    # Construct result based on API data and inputs
    result = {
        "command": command.strip(),
        "working_directory": cwd if cwd else api_data["working_directory"],
        "success": api_data["success"],
        "stdout": api_data["stdout"],
        "stderr": api_data["stderr"],
        "error_message": api_data["error_message"]
    }
    
    return result