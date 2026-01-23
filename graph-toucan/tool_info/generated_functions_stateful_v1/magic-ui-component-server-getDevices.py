from typing import Dict, List, Any

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
    Simulates fetching data from external API for UI component devices.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - device_0_name (str): Name of the first device
        - device_0_type (str): Type of the first device
        - device_0_supported_platforms (str): Supported platforms for the first device (comma-separated)
        - device_0_component_details (str): Component details for the first device
        - device_0_metadata (str): Metadata for the first device in JSON string format
        - device_1_name (str): Name of the second device
        - device_1_type (str): Type of the second device
        - device_1_supported_platforms (str): Supported platforms for the second device (comma-separated)
        - device_1_component_details (str): Component details for the second device
        - device_1_metadata (str): Metadata for the second device in JSON string format
        - total_count (int): Total number of devices returned
        - supported_frameworks_0 (str): First supported framework
        - supported_frameworks_1 (str): Second supported framework
        - documentation_url (str): URL to the official documentation
        - last_updated (str): ISO 8601 timestamp of last update
    """
    return {
        "device_0_name": "iPhone 15 Pro",
        "device_0_type": "mobile",
        "device_0_supported_platforms": "iOS,Safari",
        "device_0_component_details": "Advanced UI components with dynamic island support and dark mode integration.",
        "device_0_metadata": '{"screen_size": "6.1 inches", "resolution": "2556x1179", "pixel_density": 460}',
        "device_1_name": "Samsung Galaxy S23",
        "device_1_type": "mobile",
        "device_1_supported_platforms": "Android,Chrome",
        "device_1_component_details": "Material You design support with adaptive theming and gesture navigation.",
        "device_1_metadata": '{"screen_size": "6.1 inches", "resolution": "2340x1080", "pixel_density": 425}',
        "total_count": 2,
        "supported_frameworks_0": "Safari",
        "supported_frameworks_1": "Android",
        "documentation_url": "https://docs.magicuicomponents.com/devices",
        "last_updated": "2024-04-15T10:30:00Z"
    }

def magic_ui_component_server_getDevices() -> Dict[str, Any]:
    """
    Fetches implementation details for UI components across various devices such as Safari, iPhone 15 Pro, and Android.

    Returns:
        Dict containing:
        - devices (List[Dict]): List of device objects with implementation details including name, type,
          supported_platforms, component_details, and metadata.
        - total_count (int): Total number of devices returned.
        - supported_frameworks (List[str]): List of supported UI frameworks or environments.
        - documentation_url (str): URL to the official documentation for these UI components.
        - last_updated (str): ISO 8601 timestamp indicating when the device information was last updated.
    """
    # Fetch data from simulated external API
    api_data = call_external_api("magic-ui-component-server-getDevices", **locals())

    # Construct devices list from indexed fields
    devices = [
        {
            "name": api_data["device_0_name"],
            "type": api_data["device_0_type"],
            "supported_platforms": api_data["device_0_supported_platforms"].split(","),
            "component_details": api_data["device_0_component_details"],
            "metadata": api_data["device_0_metadata"]  # Note: kept as string; could be json.loads() if needed
        },
        {
            "name": api_data["device_1_name"],
            "type": api_data["device_1_type"],
            "supported_platforms": api_data["device_1_supported_platforms"].split(","),
            "component_details": api_data["device_1_component_details"],
            "metadata": api_data["device_1_metadata"]
        }
    ]

    # Construct supported frameworks list
    supported_frameworks = [
        api_data["supported_frameworks_0"],
        api_data["supported_frameworks_1"]
    ]

    # Build final result dictionary matching output schema
    result = {
        "devices": devices,
        "total_count": api_data["total_count"],
        "supported_frameworks": supported_frameworks,
        "documentation_url": api_data["documentation_url"],
        "last_updated": api_data["last_updated"]
    }

    return result

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
