from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PowerShell service query.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - service_0_Name (str): Name of the first running service
        - service_0_Status (str): Status of the first service (e.g., Running)
        - service_0_DisplayName (str): Display name of the first service
        - service_0_StartType (str): Start type of the first service (e.g., Automatic)
        - service_1_Name (str): Name of the second running service
        - service_1_Status (str): Status of the second service (e.g., Running)
        - service_1_DisplayName (str): Display name of the second service
        - service_1_StartType (str): Start type of the second service (e.g., Manual)
        - error (str): Error message if any occurred, otherwise empty string
    """
    return {
        "service_0_Name": "WinRM",
        "service_0_Status": "Running",
        "service_0_DisplayName": "Windows Remote Management (WS-Management)",
        "service_0_StartType": "Automatic",
        "service_1_Name": "Spooler",
        "service_1_Status": "Running",
        "service_1_DisplayName": "Print Spooler",
        "service_1_StartType": "Automatic",
        "error": ""
    }

def powershell_exec_server_get_running_services(
    name: Optional[str] = None,
    status: Optional[str] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Get information about running services on a Windows server using PowerShell.
    
    Args:
        name (Optional[str]): Filter services by name (supports wildcards like '*')
        status (Optional[str]): Filter by status (e.g., 'Running', 'Stopped')
        timeout (Optional[int]): Command timeout in seconds (valid range: 1-300, default: 60)
    
    Returns:
        Dict containing:
        - services (List[Dict]): List of service objects with 'Name', 'Status', 'DisplayName', and 'StartType'
        - error (Optional[str]): Error message if command failed, otherwise None
    
    Raises:
        ValueError: If timeout is not within valid range (1-300 seconds)
    """
    # Input validation
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            return {
                "services": [],
                "error": "Timeout must be an integer between 1 and 300 seconds."
            }
    
    try:
        # Call external API to simulate PowerShell command execution
        api_data = call_external_api("powershell-exec-server-get_running_services")
        
        # Extract error if present
        error = api_data.get("error", "")
        if error:
            return {
                "services": [],
                "error": error
            }
        
        # Construct services list from flattened API response
        services = []
        
        # Process first service
        if "service_0_Name" in api_data:
            service_0 = {
                "Name": api_data["service_0_Name"],
                "Status": api_data["service_0_Status"],
                "DisplayName": api_data["service_0_DisplayName"],
                "StartType": api_data["service_0_StartType"]
            }
            # Apply filtering by name if specified
            if name:
                if not isinstance(name, str):
                    return {
                        "services": [],
                        "error": "Name filter must be a string."
                    }
                import fnmatch
                if not fnmatch.fnmatch(service_0["Name"], name):
                    pass  # Skip if doesn't match
                else:
                    if status:
                        if service_0["Status"] == status:
                            services.append(service_0)
                    else:
                        services.append(service_0)
            else:
                # No name filter
                if status:
                    if service_0["Status"] == status:
                        services.append(service_0)
                else:
                    services.append(service_0)
        
        # Process second service
        if "service_1_Name" in api_data:
            service_1 = {
                "Name": api_data["service_1_Name"],
                "Status": api_data["service_1_Status"],
                "DisplayName": api_data["service_1_DisplayName"],
                "StartType": api_data["service_1_StartType"]
            }
            # Apply filtering by name if specified
            if name:
                if not isinstance(name, str):
                    return {
                        "services": [],
                        "error": "Name filter must be a string."
                    }
                import fnmatch
                if not fnmatch.fnmatch(service_1["Name"], name):
                    pass  # Skip if doesn't match
                else:
                    if status:
                        if service_1["Status"] == status:
                            services.append(service_1)
                    else:
                        services.append(service_1)
            else:
                # No name filter
                if status:
                    if service_1["Status"] == status:
                        services.append(service_1)
                else:
                    services.append(service_1)
        
        # Return final result
        return {
            "services": services,
            "error": None
        }
        
    except Exception as e:
        return {
            "services": [],
            "error": f"Failed to retrieve services: {str(e)}"
        }