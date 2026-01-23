from typing import Dict, Any

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
    Simulates fetching data from external API for submitting app requirements.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the submission ("success" or "error")
        - message (str): Human-readable message about the outcome
        - redirect_url (str): URL to continue the process in the browser (present only on success)
        - error_code (str): Error identifier if the call failed (e.g., "Invalid character")
        - error_traceback (str): Full traceback string for debugging (present only on error)
    """
    # Simulate successful response
    return {
        "status": "success",
        "message": "App requirements submitted successfully",
        "redirect_url": "https://databutton.ai/apps/submit/12345",
        "error_code": "",
        "error_traceback": ""
    }

def databutton_submit_app_requirements(name: str, pitch: str, spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Submit app requirements to DataButton.
    
    Args:
        name (str): The name of the app
        pitch (str): The pitch for the app
        spec (Dict[str, Any]): Specification object containing app details
    
    Returns:
        Dict containing:
        - status (str): Status of the submission ("success" or "error")
        - message (str): Human-readable message about the outcome
        - redirect_url (str): URL to continue the process in the browser (present only on success)
        - error_code (str): Error identifier if the call failed
        - error_traceback (str): Full traceback string for debugging (present only on error)
    
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not name or not isinstance(name, str):
        return {
            "status": "error",
            "message": "App name is required and must be a non-empty string",
            "error_code": "Invalid name",
            "error_traceback": "Name parameter is missing or invalid"
        }
    
    if not pitch or not isinstance(pitch, str):
        return {
            "status": "error",
            "message": "App pitch is required and must be a non-empty string",
            "error_code": "Invalid pitch",
            "error_traceback": "Pitch parameter is missing or invalid"
        }
    
    if spec is None or not isinstance(spec, dict):
        return {
            "status": "error",
            "message": "App specification is required and must be an object",
            "error_code": "Invalid spec",
            "error_traceback": "Spec parameter is missing or not an object"
        }
    
    # Call external API (simulated)
    api_data = call_external_api("databutton-submit_app_requirements", **locals())
    
    # Construct response based on API data
    result = {
        "status": api_data["status"],
        "message": api_data["message"]
    }
    
    # Add conditional fields based on status
    if api_data["status"] == "success":
        if api_data.get("redirect_url"):
            result["redirect_url"] = api_data["redirect_url"]
    else:
        if api_data.get("error_code"):
            result["error_code"] = api_data["error_code"]
        if api_data.get("error_traceback"):
            result["error_traceback"] = api_data["error_traceback"]
    
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
