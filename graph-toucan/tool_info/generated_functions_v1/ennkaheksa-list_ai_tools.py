from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for AI-optimized nodes in n8n.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - tool_0_name (str): Name of the first AI-optimized node
        - tool_0_description (str): Description of the first node
        - tool_0_category (str): Category of the first node
        - tool_0_usableAsTool (bool): Whether the first node is usable as a tool
        - tool_0_isCommunityNode (bool): Whether the first node is a community node
        - tool_1_name (str): Name of the second AI-optimized node
        - tool_1_description (str): Description of the second node
        - tool_1_category (str): Category of the second node
        - tool_1_usableAsTool (bool): Whether the second node is usable as a tool
        - tool_1_isCommunityNode (bool): Whether the second node is a community node
        - total_count (int): Total number of AI-optimized nodes (should be 263)
        - metadata_source_system (str): Source system identifier
        - metadata_timestamp (str): ISO format timestamp of response generation
        - metadata_note (str): Note about expandability to non-listed nodes
    """
    return {
        "tool_0_name": "HTTP Request",
        "tool_0_description": "Sends an HTTP request to any API with customizable headers, body, and authentication.",
        "tool_0_category": "Core",
        "tool_0_usableAsTool": True,
        "tool_0_isCommunityNode": False,
        "tool_1_name": "OpenAI",
        "tool_1_description": "Interact with OpenAI models for text generation, embeddings, and more.",
        "tool_1_category": "AI",
        "tool_1_usableAsTool": True,
        "tool_1_isCommunityNode": False,
        "total_count": 263,
        "metadata_source_system": "n8n-ai-tool-registry",
        "metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_note": "Any node in n8n can be used as a tool. These 263 are optimized for AI usage."
    }


def ennkaheksa_list_ai_tools() -> Dict[str, Any]:
    """
    List all 263 nodes marked with usableAsTool=true property.

    This function retrieves metadata about AI-optimized nodes in n8n that are suitable for use
    with AI agents. While only 263 nodes are listed here as optimized, any node in n8n
    (e.g., Slack, Google Sheets, HTTP Request) can be connected to an AI Agent's tool port.

    Returns:
        Dict containing:
        - tools (List[Dict]): List of AI-optimized nodes with name, description, category,
          usableAsTool flag, and isCommunityNode flag.
        - total_count (int): Total number of tools returned (263).
        - metadata (Dict): Additional context including source system, timestamp,
          and a note about expandability to non-listed nodes.
    """
    try:
        # Fetch simulated external data
        api_data = call_external_api("ennkaheksa-list_ai_tools")

        # Construct tools list from indexed fields
        tools = [
            {
                "name": api_data["tool_0_name"],
                "description": api_data["tool_0_description"],
                "category": api_data["tool_0_category"],
                "usableAsTool": api_data["tool_0_usableAsTool"],
                "isCommunityNode": api_data["tool_0_isCommunityNode"]
            },
            {
                "name": api_data["tool_1_name"],
                "description": api_data["tool_1_description"],
                "category": api_data["tool_1_category"],
                "usableAsTool": api_data["tool_1_usableAsTool"],
                "isCommunityNode": api_data["tool_1_isCommunityNode"]
            }
        ]

        # Construct final result matching output schema
        result = {
            "tools": tools,
            "total_count": api_data["total_count"],
            "metadata": {
                "source_system": api_data["metadata_source_system"],
                "timestamp": api_data["metadata_timestamp"],
                "note": api_data["metadata_note"]
            }
        }

        return result

    except KeyError as e:
        raise RuntimeError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to list AI tools: {str(e)}") from e