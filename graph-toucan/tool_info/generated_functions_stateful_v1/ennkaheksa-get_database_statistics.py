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
    Simulates fetching data from external API for n8n node ecosystem statistics.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_nodes (int): Total number of n8n nodes available in the ecosystem
        - ai_tools_count (int): Number of AI-related tools/nodes available
        - trigger_nodes_count (int): Number of nodes that function as triggers
        - versioned_nodes_count (int): Number of nodes that support versioning
        - documentation_coverage (float): Percentage (0-100) of nodes with documentation coverage
        - package_breakdown_webhook (int): Node count for webhook package
        - package_breakdown_trigger (int): Node count for trigger package
        - package_breakdown_ai (int): Node count for AI package
        - package_breakdown_utility (int): Node count for utility package
        - summary (str): A concise textual summary of the database statistics for quick reading
    """
    return {
        "total_nodes": 525,
        "ai_tools_count": 263,
        "trigger_nodes_count": 104,
        "versioned_nodes_count": 412,
        "documentation_coverage": 87.0,
        "package_breakdown_webhook": 45,
        "package_breakdown_trigger": 104,
        "package_breakdown_ai": 263,
        "package_breakdown_utility": 113,
        "summary": "The n8n ecosystem includes 525 total nodes with strong AI support (263 tools) and 104 trigger nodes. Documentation covers 87% of nodes, and 412 nodes support versioning. Major packages include AI, Trigger, Webhook, and Utility nodes."
    }

def ennkaheksa_get_database_statistics() -> Dict[str, Any]:
    """
    Quick summary of the n8n node ecosystem. Shows: total nodes (525), AI tools (263), triggers (104),
    versioned nodes, documentation coverage (87%), package breakdown. No parameters needed.
    Useful for verifying MCP is working and understanding available scope.

    Returns:
        Dict containing:
            - total_nodes (int): Total number of n8n nodes available in the ecosystem
            - ai_tools_count (int): Number of AI-related tools/nodes available
            - trigger_nodes_count (int): Number of nodes that function as triggers
            - versioned_nodes_count (int): Number of nodes that support versioning
            - documentation_coverage (float): Percentage (0-100) of nodes with documentation coverage
            - package_breakdown (Dict): Breakdown of node counts by package type
            - summary (str): A concise textual summary of the database statistics for quick reading
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("ennkaheksa-get_database_statistics", **locals())

        # Construct package breakdown dictionary from flattened fields
        package_breakdown = {
            "webhook": api_data["package_breakdown_webhook"],
            "trigger": api_data["package_breakdown_trigger"],
            "ai": api_data["package_breakdown_ai"],
            "utility": api_data["package_breakdown_utility"]
        }

        # Build final result structure matching output schema
        result = {
            "total_nodes": api_data["total_nodes"],
            "ai_tools_count": api_data["ai_tools_count"],
            "trigger_nodes_count": api_data["trigger_nodes_count"],
            "versioned_nodes_count": api_data["versioned_nodes_count"],
            "documentation_coverage": api_data["documentation_coverage"],
            "package_breakdown": package_breakdown,
            "summary": api_data["summary"]
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while retrieving database statistics: {str(e)}")

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
