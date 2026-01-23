from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
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
    api_data = call_external_api("databutton-submit_app_requirements")
    
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