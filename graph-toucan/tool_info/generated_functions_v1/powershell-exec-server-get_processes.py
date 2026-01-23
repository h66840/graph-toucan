from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for process information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - process_0_Name (str): Name of the first process
        - process_0_Id (int): ID of the first process
        - process_0_CPU (float): CPU usage of the first process
        - process_0_WorkingSet (int): Working set (memory) of the first process
        - process_0_StartTime (str): Start time of the first process
        - process_1_Name (str): Name of the second process
        - process_1_Id (int): ID of the second process
        - process_1_CPU (float): CPU usage of the second process
        - process_1_WorkingSet (int): Working set (memory) of the second process
        - process_1_StartTime (str): Start time of the second process
        - error (str): Error message if any occurred
    """
    return {
        "process_0_Name": "python.exe",
        "process_0_Id": 1234,
        "process_0_CPU": 12.5,
        "process_0_WorkingSet": 104857600,
        "process_0_StartTime": "2023-10-01T08:30:00",
        "process_1_Name": "chrome.exe",
        "process_1_Id": 5678,
        "process_1_CPU": 25.3,
        "process_1_WorkingSet": 209715200,
        "process_1_StartTime": "2023-10-01T09:15:00",
        "error": ""
    }

def powershell_exec_server_get_processes(
    name: Optional[str] = None,
    sort_by: Optional[str] = None,
    timeout: Optional[int] = None,
    top: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get information about running processes.
    
    Args:
        name (Optional[str]): Filter processes by name (supports wildcards)
        sort_by (Optional[str]): Property to sort by (e.g., CPU, WorkingSet)
        timeout (Optional[int]): Command timeout in seconds (1-300, default 60)
        top (Optional[int]): Limit to top N processes
    
    Returns:
        Dict containing:
        - processes (List[Dict]): List of running processes with details such as 'Name', 'Id', 
          'CPU', 'WorkingSet', 'StartTime', and other process-related properties
        - error (str): Error message if the command failed to execute
    """
    # Input validation
    if timeout is not None and (timeout < 1 or timeout > 300):
        return {
            "processes": [],
            "error": "Timeout must be between 1 and 300 seconds"
        }
    
    # Call external API to get flattened data
    api_data = call_external_api("powershell-exec-server-get_processes")
    
    # Extract error if present
    error = api_data.get("error", "")
    
    # Construct processes list from flattened API data
    processes = []
    
    # Process index 0
    if "process_0_Name" in api_data:
        process_0 = {
            "Name": api_data["process_0_Name"],
            "Id": api_data["process_0_Id"],
            "CPU": api_data["process_0_CPU"],
            "WorkingSet": api_data["process_0_WorkingSet"],
            "StartTime": api_data["process_0_StartTime"]
        }
        processes.append(process_0)
    
    # Process index 1
    if "process_1_Name" in api_data:
        process_1 = {
            "Name": api_data["process_1_Name"],
            "Id": api_data["process_1_Id"],
            "CPU": api_data["process_1_CPU"],
            "WorkingSet": api_data["process_1_WorkingSet"],
            "StartTime": api_data["process_1_StartTime"]
        }
        processes.append(process_1)
    
    # Apply name filter if specified
    if name is not None:
        # Simple wildcard support: * matches any sequence, ? matches any single character
        import fnmatch
        processes = [p for p in processes if fnmatch.fnmatch(p["Name"].lower(), name.lower())]
    
    # Apply sorting if specified
    if sort_by is not None:
        # Supported sort fields
        valid_sort_fields = ["CPU", "WorkingSet", "Id", "Name"]
        sort_field = sort_by.strip()
        if sort_field not in valid_sort_fields:
            return {
                "processes": [],
                "error": f"Invalid sort_by value: {sort_by}. Supported values: {valid_sort_fields}"
            }
        # Sort in descending order by default for numeric fields
        reverse = sort_field in ["CPU", "WorkingSet", "Id"]
        try:
            processes.sort(key=lambda x: x[sort_field], reverse=reverse)
        except KeyError:
            # Handle case where sort field might not exist in all process entries
            pass
    
    # Apply top limit if specified
    if top is not None:
        if top <= 0:
            processes = []
        else:
            processes = processes[:top]
    
    return {
        "processes": processes,
        "error": error
    }