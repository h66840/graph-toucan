from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for scheduled tasks.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - error (str): Error message if any, otherwise empty string
        - platform (str): Operating system platform, e.g., 'windows' or 'linux'
        - action_performed (str): Action performed, e.g., 'query' or 'status'
        - task_name (str): Name of the specific task queried, if applicable
        - available_on_platform (bool): Whether scheduled tasks are supported on this platform
    """
    return {
        "error": "",
        "platform": "windows",
        "action_performed": "query",
        "task_name": "SampleTask",
        "available_on_platform": True
    }

def windows_command_line_mcp_server_get_scheduled_tasks(action: Optional[str] = None, taskName: Optional[str] = None) -> Dict[str, Any]:
    """
    Retrieve information about scheduled tasks on the system.
    
    This function simulates querying scheduled tasks on a Windows system.
    It can return a list of all tasks or detailed status of a specific task.

    Args:
        action (Optional[str]): The action to perform. Valid values are 'query' to list all tasks or 'status' to get details of a specific task.
        taskName (Optional[str]): The name of the specific task to query when action is 'status'.

    Returns:
        Dict containing the following keys:
        - error (str): Error message if operation failed, otherwise empty string
        - platform (str): Current operating system platform
        - action_performed (str): The action that was attempted ('query' or 'status')
        - task_name (str): Name of the specific task queried, if applicable
        - available_on_platform (bool): Whether the tool is supported on current platform
    """
    # Validate inputs
    if action and action not in ['query', 'status']:
        return {
            "error": "Invalid action. Supported actions are 'query' and 'status'.",
            "platform": "windows",
            "action_performed": action or "unknown",
            "task_name": taskName or "",
            "available_on_platform": False
        }

    # Simulate platform check
    platform = "windows"
    available_on_platform = platform == "windows"

    if not available_on_platform:
        return {
            "error": "Scheduled tasks are only supported on Windows platforms.",
            "platform": platform,
            "action_performed": action or "query",
            "task_name": taskName or "",
            "available_on_platform": available_on_platform
        }

    # Determine action to perform
    action_performed = action or "query"

    # If status action is requested but no task name provided
    if action_performed == "status" and not taskName:
        return {
            "error": "Task name is required when performing 'status' action.",
            "platform": platform,
            "action_performed": action_performed,
            "task_name": "",
            "available_on_platform": available_on_platform
        }

    # Call external API simulation
    api_data = call_external_api("windows-command-line-mcp-server-get_scheduled_tasks")

    # Construct result using API data
    result = {
        "error": api_data["error"],
        "platform": api_data["platform"],
        "action_performed": action_performed,
        "task_name": taskName or api_data["task_name"],
        "available_on_platform": api_data["available_on_platform"]
    }

    # Special case: if task does not exist (simulated)
    if action_performed == "status" and taskName and "invalid" in taskName.lower():
        result["error"] = f"Task '{taskName}' not found."
        result["task_name"] = taskName

    return result