from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching mitigation data from external ATT&CK API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - mitigation_0_id (str): ID of the first mitigation
        - mitigation_0_name (str): Name of the first mitigation
        - mitigation_0_description (str): Description of the first mitigation
        - mitigation_1_id (str): ID of the second mitigation
        - mitigation_1_name (str): Name of the second mitigation
        - mitigation_1_description (str): Description of the second mitigation
    """
    return {
        "mitigation_0_id": "M1037",
        "mitigation_0_name": "Phishing Training",
        "mitigation_0_description": "Train users to recognize and report phishing attempts to reduce success of social engineering attacks.",
        "mitigation_1_id": "M1018",
        "mitigation_1_name": "User Training",
        "mitigation_1_description": "Educate users on security best practices to reduce the risk of compromise through human error."
    }

def attack_mcp_server_query_mitigations(technique_id: str) -> Dict[str, Any]:
    """
    根据ATT&CK技术ID查询相关的缓解措施列表。为每个缓解措施提供ID、名称和描述。
    
    Args:
        technique_id (str): ATT&CK 技术ID (例如: T1566)
    
    Returns:
        Dict containing:
            - mitigations (List[Dict]): List of mitigation objects with 'id', 'name', and 'description' fields
    
    Raises:
        ValueError: If technique_id is empty or not a string
    """
    if not technique_id or not isinstance(technique_id, str):
        raise ValueError("technique_id must be a non-empty string")
    
    # Fetch data from simulated external API
    api_data = call_external_api("attack-mcp-server-query_mitigations")
    
    # Construct the nested output structure as per schema
    mitigations = [
        {
            "id": api_data["mitigation_0_id"],
            "name": api_data["mitigation_0_name"],
            "description": api_data["mitigation_0_description"]
        },
        {
            "id": api_data["mitigation_1_id"],
            "name": api_data["mitigation_1_name"],
            "description": api_data["mitigation_1_description"]
        }
    ]
    
    return {
        "mitigations": mitigations
    }