from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Windows service information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error_message (str): Error message indicating platform incompatibility
        - platform (str): The current operating system platform
    """
    return {
        "error_message": "This tool is only available on Windows operating systems.",
        "platform": "Linux"
    }

def windows_command_line_mcp_server_get_service_info(action: Optional[str] = None, serviceName: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve information about Windows services. Can query all services or get detailed status of a specific service.
    
    This function simulates interaction with a Windows command-line tool to retrieve service information.
    Since the actual tool is not available on non-Windows platforms, it returns a simulated error response.
    
    Args:
        action (Optional[str]): Action to perform (e.g., 'list', 'status'). Defaults to None.
        serviceName (Optional[str]): Service name to get info about. Defaults to None.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error_message (str): Error message indicating the tool is not available on the current platform
            - platform (str): The current operating system platform where the tool was attempted to run
    """
    # Call external API to get flat data
    api_data = call_external_api("windows-command-line-mcp-server-get_service_info")
    
    # Construct result matching output schema
    result = {
        "error_message": api_data["error_message"],
        "platform": api_data["platform"]
    }
    
    return result