from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for shell command execution.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - exit_code (int): exit code of the executed shell command (0 for success, non-zero for errors)
        - execution_output (str): captured output or message from the command execution
    """
    return {
        "exit_code": 0,
        "execution_output": "Command executed successfully"
    }

def lilith_shell_execute_command(command: str, directory: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute a shell command in the specified directory.
    
    Args:
        command (str): Command to execute
        directory (Optional[str]): Working directory (optional)
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - exit_code (int): exit code of the executed shell command (0 for success, non-zero for errors)
            - execution_output (str): captured output or message from the command execution, if any
    
    Raises:
        ValueError: If command is empty or not a string
        RuntimeError: If there's an error during command execution
    """
    # Input validation
    if not command:
        raise ValueError("Command is required and cannot be empty")
    
    if not isinstance(command, str):
        raise ValueError("Command must be a string")
    
    if directory is not None:
        if not isinstance(directory, str):
            raise ValueError("Directory must be a string")
        # Note: Without os.path, we can't validate directory existence or type
        # This is a limitation of removing dangerous imports, but we maintain interface
    
    try:
        # Simulate command execution using the external API helper
        api_result = call_external_api("shell_command")
        
        # Return structured output with simulated results
        return {
            "exit_code": api_result["exit_code"],
            "execution_output": api_result["execution_output"]
        }
        
    except Exception as e:
        return {
            "exit_code": -1,
            "execution_output": f"Error executing command: {str(e)}"
        }