from typing import Dict, List, Any, Optional
from datetime import datetime

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching system information from an external PowerShell API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - os_name (str): Name of the operating system
        - os_version (str): Version of the operating system
        - uptime (str): System uptime as duration string
        - total_memory_mb (int): Total physical memory in MB
        - free_memory_mb (int): Free physical memory in MB
        - cpu (str): CPU model/name
        - computer_name (str): Hostname of the system
        - retrieved_property_0 (str): First successfully retrieved property name
        - retrieved_property_1 (str): Second successfully retrieved property name
        - timestamp (str): ISO 8601 timestamp of data collection
        - status (str): Execution status ('success' or 'error')
        - error_message (str): Error description if any, else empty string
        - source_host (str): Hostname or IP address of the source server
    """
    return {
        "os_name": "Microsoft Windows Server 2022 Datacenter",
        "os_version": "10.0.20348",
        "uptime": "12 days, 5 hours, 34 minutes",
        "total_memory_mb": 16384,
        "free_memory_mb": 4271,
        "cpu": "Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz",
        "computer_name": "SRV-WIN2022-01",
        "retrieved_property_0": "os_name",
        "retrieved_property_1": "os_version",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "status": "success",
        "error_message": "",
        "source_host": "192.168.1.100"
    }

def powershell_exec_server_get_system_info(
    properties: Optional[List[str]] = None,
    timeout: Optional[int] = 60
) -> Dict[str, Any]:
    """
    Get system information from a remote server using PowerShell.
    
    Args:
        properties (Optional[List[str]]): List of ComputerInfo properties to retrieve.
            If None, retrieves default set of system properties.
        timeout (Optional[int]): Command timeout in seconds (1-300). Default is 60.
    
    Returns:
        Dict containing the following keys:
        - system_info (Dict): Key system properties including os_name, os_version, uptime,
          total_memory_mb, free_memory_mb, cpu, computer_name, and others.
        - retrieved_properties (List[str]): List of property names successfully retrieved.
        - timestamp (str): ISO 8601 timestamp when information was collected.
        - status (str): 'success' or 'error' indicating execution outcome.
        - error_message (Optional[str]): Description of error if status is 'error', else None.
        - source_host (str): Hostname or IP address of the server from which data was gathered.
    
    Raises:
        ValueError: If timeout is not within valid range (1-300 seconds).
    """
    # Input validation
    if timeout is not None:
        if not isinstance(timeout, int) or timeout < 1 or timeout > 300:
            return {
                "system_info": {},
                "retrieved_properties": [],
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "status": "error",
                "error_message": "Timeout must be an integer between 1 and 300 seconds.",
                "source_host": ""
            }
    
    try:
        # Call external API to simulate PowerShell execution
        api_data = call_external_api("powershell-exec-server-get_system_info", **locals())
        
        # Construct system_info dictionary from flat API response
        system_info = {
            "os_name": api_data["os_name"],
            "os_version": api_data["os_version"],
            "uptime": api_data["uptime"],
            "total_memory_mb": api_data["total_memory_mb"],
            "free_memory_mb": api_data["free_memory_mb"],
            "cpu": api_data["cpu"],
            "computer_name": api_data["computer_name"]
        }
        
        # Filter system_info based on requested properties if specified
        if properties and isinstance(properties, list):
            filtered_system_info = {}
            for prop in properties:
                if prop in system_info:
                    filtered_system_info[prop] = system_info[prop]
            system_info = filtered_system_info
        
        # Build retrieved_properties list from available data
        retrieved_properties = []
        for i in range(2):  # We have two indexed properties from API
            prop_key = f"retrieved_property_{i}"
            if prop_key in api_data and api_data[prop_key]:
                retrieved_properties.append(api_data[prop_key])
        
        # Final result construction
        result = {
            "system_info": system_info,
            "retrieved_properties": retrieved_properties,
            "timestamp": api_data["timestamp"],
            "status": api_data["status"],
            "error_message": api_data["error_message"] if api_data["error_message"] else None,
            "source_host": api_data["source_host"]
        }
        
        return result
        
    except Exception as e:
        return {
            "system_info": {},
            "retrieved_properties": [],
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "error",
            "error_message": f"Unexpected error occurred: {str(e)}",
            "source_host": ""
        }

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        # WRITE / CREATE
        if "write" in cmd or "create" in cmd or "save" in cmd or "update" in cmd:
            path = kwargs.get("path")
            content = kwargs.get("content") or kwargs.get("file_text") or kwargs.get("text")
            if path and content:
                sys_state.write_file(path, content)
                
        # READ / VIEW (Inject State)
        if "read" in cmd or "view" in cmd or "cat" in cmd or "search" in cmd or "list" in cmd:
            path = kwargs.get("path")
            if path:
                real_content = sys_state.read_file(path)
                if real_content is not None:
                    result["content"] = real_content
    except Exception:
        pass 
    return result
