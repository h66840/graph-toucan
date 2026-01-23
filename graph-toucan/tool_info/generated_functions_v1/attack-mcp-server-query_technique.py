from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for ATT&CK technique query.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first matched technique
        - result_0_name (str): Name of the first matched technique
        - result_0_description (str): Description of the first matched technique
        - result_1_id (str): ID of the second matched technique
        - result_1_name (str): Name of the second matched technique
        - result_1_description (str): Description of the second matched technique
        - count (int): Total number of techniques returned (0, 1, or 2)
    """
    return {
        "result_0_id": "T1059.001",
        "result_0_name": "Command and Scripting Interpreter: PowerShell",
        "result_0_description": "Adversaries may abuse PowerShell commands and scripts for execution. PowerShell is a powerful interactive command-line interface and scripting environment included in the Windows operating system.",
        "result_1_id": "T1059.003",
        "result_1_name": "Command and Scripting Interpreter: Windows Command Shell",
        "result_1_description": "Adversaries may abuse the Windows command shell for execution. The Windows command shell (cmd) is the primary command prompt on Windows systems.",
        "count": 2,
    }


def attack_mcp_server_query_technique(tech_name: Optional[str] = None, technique_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Queries ATT&CK framework for techniques by exact technique ID or fuzzy name match.

    If technique_id is provided, returns detailed information for that single technique.
    If tech_name is provided, returns a list of techniques matching the name (fuzzy search).
    If neither is provided, returns empty results.

    Args:
        tech_name (Optional[str]): The name or partial name of the technique to search for.
        technique_id (Optional[str]): The exact technique ID (e.g., T1059.001) to retrieve.

    Returns:
        Dict containing:
        - results (List[Dict]): List of technique objects with 'id', 'name', and 'description' fields.
        - count (int): Number of techniques returned in the results list.
    """
    # Input validation
    if not tech_name and not technique_id:
        return {"results": [], "count": 0}

    # Simulate external API call
    api_data = call_external_api("attack-mcp-server-query_technique")

    # Construct results list from flattened API response
    results: List[Dict[str, str]] = []
    count = api_data["count"]

    for i in range(count):
        result_id = api_data.get(f"result_{i}_id")
        result_name = api_data.get(f"result_{i}_name")
        result_description = api_data.get(f"result_{i}_description")

        if result_id and result_name and result_description:
            technique = {
                "id": result_id,
                "name": result_name,
                "description": result_description,
            }
            results.append(technique)

    # If technique_id is specified, filter for exact match
    if technique_id:
        filtered_results = [t for t in results if t["id"] == technique_id]
        return {
            "results": filtered_results,
            "count": len(filtered_results),
        }

    # If tech_name is specified, perform case-insensitive substring match
    if tech_name:
        search_term = tech_name.strip().lower()
        if not search_term:
            return {"results": [], "count": 0}
        filtered_results = [t for t in results if search_term in t["name"].lower()]
        return {
            "results": filtered_results,
            "count": len(filtered_results),
        }

    return {"results": results, "count": len(results)}