from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for terminal command execution.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - stdout (str): Standard output from command execution
        - stderr (str): Standard error output from command execution
        - exit_code (int): Exit status code of the executed command
    """
    return {
        "stdout": "Command executed successfully",
        "stderr": "",
        "exit_code": 0
    }

def terminal_mcp_server_execute_command(
    command: str,
    env: Optional[Dict[str, str]] = None,
    host: Optional[str] = None,
    session: Optional[str] = None,
    username: Optional[str] = None
) -> Dict[str, Any]:
    """
    Execute commands on remote hosts or locally.
    
    This function simulates executing a shell command either locally or on a remote host
    via SSH. It returns the standard output, standard error, and exit code of the command.
    
    Args:
        command (str): Command to execute. Before running commands, it's best to determine the system type (Mac, Linux, etc.)
        env (Optional[Dict[str, str]]): Environment variables to set for the command execution
        host (Optional[str]): Host to connect to (if not provided, command runs locally)
        session (Optional[str]): Session name, defaults to 'default'. Reusing the same session name maintains terminal environment for 20 minutes.
        username (Optional[str]): Username for SSH connection (required when host is specified)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - stdout (str): Output from the command's standard output stream
            - stderr (str): Output from the command's standard error stream
            - exit_code (int): Exit status code of the executed command; 0 indicates success
    
    Raises:
        ValueError: If host is provided but username is missing
    """
    # Input validation
    if host is not None and not username:
        raise ValueError("Username is required when specifying a host for SSH connection")
    
    if not command.strip():
        raise ValueError("Command cannot be empty or whitespace")
    
    # Default session name
    if session is None:
        session = "default"
    
    # Call external API to simulate command execution
    api_data = call_external_api("terminal-mcp-server-execute_command")
    
    # Construct result matching output schema
    result = {
        "stdout": api_data["stdout"],
        "stderr": api_data["stderr"],
        "exit_code": api_data["exit_code"]
    }
    
    return result