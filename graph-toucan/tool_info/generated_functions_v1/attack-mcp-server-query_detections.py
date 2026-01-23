from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching detection data from external ATT&CK MCP server API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - detection_0_source (str): Source data component for first detection
        - detection_0_description (str): Description of first detection method
        - detection_1_source (str): Source data component for second detection
        - detection_1_description (str): Description of second detection method
    """
    return {
        "detection_0_source": "Process Creation Events",
        "detection_0_description": "Monitor for unusual parent-child process relationships indicative of T1059.001",
        "detection_1_source": "Command Line Arguments",
        "detection_1_description": "Analyze command lines for suspicious scripting patterns using T1059.001"
    }

def attack_mcp_server_query_detections(technique_id: str) -> Dict[str, Any]:
    """
    Query detection methods based on MITRE ATT&CK technique ID.
    
    Args:
        technique_id (str): The ATT&CK technique ID (e.g., T1059.001)
    
    Returns:
        Dict containing a list of detection methods, each with source and description:
        - detections (List[Dict]): List of detection objects with 'source' and 'description' keys
    
    Raises:
        ValueError: If technique_id is empty or invalid
    """
    if not technique_id or not isinstance(technique_id, str) or not technique_id.strip():
        raise ValueError("technique_id must be a non-empty string")
    
    technique_id = technique_id.strip()
    
    # Fetch simulated external data
    api_data = call_external_api("attack-mcp-server-query_detections")
    
    # Construct detections list from flattened API response
    detections: List[Dict[str, str]] = [
        {
            "source": api_data["detection_0_source"],
            "description": api_data["detection_0_description"]
        },
        {
            "source": api_data["detection_1_source"],
            "description": api_data["detection_1_description"]
        }
    ]
    
    return {
        "detections": detections
    }