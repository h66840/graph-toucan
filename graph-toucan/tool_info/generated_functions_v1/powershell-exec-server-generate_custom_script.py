from typing import Dict, Any, Optional, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PowerShell script generation.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - script_path (str): Path where the generated PowerShell script was saved
    """
    return {
        "script_path": "C:\\scripts\\generated_script.ps1"
    }

def powershell_exec_server_generate_custom_script(
    description: str,
    script_type: str,
    parameters: Optional[List[str]] = None,
    include_logging: Optional[bool] = False,
    include_error_handling: Optional[bool] = False,
    output_path: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Generate a custom PowerShell script based on description and options.
    
    Args:
        description: Natural language description of what the script should do
        script_type: Type of script to generate (e.g., file_ops, service_mgmt)
        parameters: List of parameters the script should accept
        include_logging: Whether to include logging functions
        include_error_handling: Whether to include error handling
        output_path: Where to save the generated script (optional)
        timeout: Command timeout in seconds (1-300, default 60)
        
    Returns:
        Dictionary containing:
        - script_path (str): path where the generated PowerShell script was saved
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not description:
        raise ValueError("Description is required")
    
    if not script_type:
        raise ValueError("Script type is required")
    
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            raise ValueError("Timeout must be an integer between 1 and 300 seconds")
    
    # Call external API to simulate script generation
    api_data = call_external_api("powershell-exec-server-generate_custom_script")
    
    # Construct result matching output schema
    result = {
        "script_path": api_data["script_path"]
    }
    
    return result