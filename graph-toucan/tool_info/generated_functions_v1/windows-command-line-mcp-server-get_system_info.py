from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching system information from an external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if tool cannot run outside Windows
        - platform (str): Operating system platform where the tool was executed
    """
    return {
        "error": "This tool can only be executed in a Windows environment.",
        "platform": "Linux"
    }

def windows_command_line_mcp_server_get_system_info(detail: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve system information including OS, hardware, and user details.
    
    This function simulates retrieving system information by calling an external API.
    The level of detail can be specified via the 'detail' parameter.
    
    Args:
        detail (Optional[str]): Level of detail for the system information. 
                               Can be 'basic' or 'full'. Defaults to 'basic'.
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - error (str): Error message if tool cannot run outside Windows environment
            - platform (str): Current operating system platform where the tool was executed
    
    Note:
        This tool is designed to run on Windows systems. When executed elsewhere,
        it will return an error indicating the incompatible environment.
    """
    # Validate input
    if detail is not None and detail not in ['basic', 'full']:
        return {
            "error": "Invalid detail level. Use 'basic' or 'full'.",
            "platform": "Unknown"
        }
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("windows-command-line-mcp-server-get_system_info")
    
    # Construct result matching output schema
    result = {
        "error": api_data["error"],
        "platform": api_data["platform"]
    }
    
    return result