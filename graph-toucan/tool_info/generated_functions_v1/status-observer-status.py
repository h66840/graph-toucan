from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching platform status data from an external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - platform_0_name (str): Name of the first platform
        - platform_0_status (str): Status of the first platform (e.g., 'operational', 'degraded', 'down')
        - platform_0_details_0_component (str): First component name for platform 0
        - platform_0_details_0_status (str): Status of first component for platform 0
        - platform_0_details_1_component (str): Second component name for platform 0
        - platform_0_details_1_status (str): Status of second component for platform 0
        - platform_1_name (str): Name of the second platform
        - platform_1_status (str): Status of the second platform
        - platform_1_details_0_component (str): First component name for platform 1
        - platform_1_details_0_status (str): Status of first component for platform 1
        - platform_1_details_1_component (str): Second component name for platform 1
        - platform_1_details_1_status (str): Status of second component for platform 1
        - last_updated (str): Timestamp of last update in human-readable format
        - error (str): Error message if any; empty string if no error
    """
    return {
        "platform_0_name": "GitHub",
        "platform_0_status": "operational",
        "platform_0_details_0_component": "Repositories",
        "platform_0_details_0_status": "operational",
        "platform_0_details_1_component": "Actions",
        "platform_0_details_1_status": "degraded_performance",
        "platform_1_name": "GitLab",
        "platform_1_status": "degraded_performance",
        "platform_1_details_0_component": "Merge Requests",
        "platform_1_details_0_status": "partial_outage",
        "platform_1_details_1_component": "CI/CD Pipelines",
        "platform_1_details_1_status": "operational",
        "last_updated": "2023-10-05 14:30:00 UTC",
        "error": ""
    }

def status_observer_status(command: str) -> Dict[str, Any]:
    """
    Check operational status of major digital platforms.

    Args:
        command (str): Command to execute. Valid values are 'list', '--all', or '--{platform}' (e.g., '--github').

    Returns:
        Dict containing:
        - platforms (List[Dict]): List of platform status entries with 'name', 'status', and optional 'details'.
        - last_updated (str): Timestamp of the last status update in human-readable format.
        - error (str): Error message if the requested platform is not found or another issue occurs.

    Example:
        >>> status_observer_status("--all")
        {
            "platforms": [
                {
                    "name": "GitHub",
                    "status": "operational",
                    "details": [
                        {"component": "Repositories", "status": "operational"},
                        {"component": "Actions", "status": "degraded_performance"}
                    ]
                },
                {
                    "name": "GitLab",
                    "status": "degraded_performance",
                    "details": [
                        {"component": "Merge Requests", "status": "partial_outage"},
                        {"component": "CI/CD Pipelines", "status": "operational"}
                    ]
                }
            ],
            "last_updated": "2023-10-05 14:30:00 UTC",
            "error": ""
        }
    """
    # Validate input
    if not command:
        return {
            "platforms": [],
            "last_updated": "",
            "error": "Command is required"
        }

    # Normalize command
    command_lower = command.strip().lower()

    # Fetch simulated external data
    api_data = call_external_api("status-observer-status")

    # Extract error if present
    if api_data.get("error"):
        return {
            "platforms": [],
            "last_updated": api_data.get("last_updated", ""),
            "error": api_data["error"]
        }

    # Build platforms list from flattened API data
    platforms = []

    for i in range(2):  # We have two platforms in simulation
        name_key = f"platform_{i}_name"
        status_key = f"platform_{i}_status"
        if name_key not in api_data or not api_data[name_key]:
            continue

        platform_name = api_data[name_key]
        platform_status = api_data[status_key]

        # Filter by platform if command specifies one
        if command_lower.startswith("--") and command_lower[2:] != platform_name.lower():
            continue

        # Build details list
        details = []
        for j in range(2):  # Two components per platform
            comp_key = f"platform_{i}_details_{j}_component"
            stat_key = f"platform_{i}_details_{j}_status"
            if comp_key in api_data and api_data[comp_key]:
                details.append({
                    "component": api_data[comp_key],
                    "status": api_data[stat_key]
                })

        platforms.append({
            "name": platform_name,
            "status": platform_status,
            "details": details
        })

    # If no platforms matched (e.g., invalid platform name)
    if command_lower.startswith("--") and command_lower[2:] not in [p["name"].lower() for p in platforms]:
        return {
            "platforms": [],
            "last_updated": api_data.get("last_updated", ""),
            "error": f"Platform '{command_lower[2:]}' not found"
        }

    return {
        "platforms": platforms,
        "last_updated": api_data["last_updated"],
        "error": ""
    }