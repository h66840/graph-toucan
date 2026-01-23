from typing import Dict, List, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching MITRE ATT&CK tactics data from an external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - tactic_0_id (str): ID of the first tactic
        - tactic_0_name (str): Name of the first tactic
        - tactic_0_description (str): Description of the first tactic
        - tactic_1_id (str): ID of the second tactic
        - tactic_1_name (str): Name of the second tactic
        - tactic_1_description (str): Description of the second tactic
    """
    return {
        "tactic_0_id": "TA0001",
        "tactic_0_name": "Initial Access",
        "tactic_0_description": "The adversary is trying to get into your network.",
        "tactic_1_id": "TA0002",
        "tactic_1_name": "Execution",
        "tactic_1_description": "The adversary is trying to run malicious code."
    }


def attack_mcp_server_list_tactics() -> List[Dict[str, str]]:
    """
    获取并列出MITRE ATT&CK框架中定义的所有战术。为每个战术提供ID、名称和描述。

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing 'id', 'name', and 'description'
                              fields for a MITRE ATT&CK tactic.
    """
    try:
        # Fetch simulated external data
        api_data = call_external_api("attack-mcp-server-list_tactics")

        # Construct the list of tactics from flattened API response
        tactics = [
            {
                "id": api_data["tactic_0_id"],
                "name": api_data["tactic_0_name"],
                "description": api_data["tactic_0_description"]
            },
            {
                "id": api_data["tactic_1_id"],
                "name": api_data["tactic_1_name"],
                "description": api_data["tactic_1_description"]
            }
        ]

        return tactics

    except KeyError as e:
        # Handle missing expected fields in API response
        raise RuntimeError(f"Missing required field in API response: {e}")
    except Exception as e:
        # Handle any other unforeseen errors
        raise RuntimeError(f"An error occurred while processing tactics: {e}")