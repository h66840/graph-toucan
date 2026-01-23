from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for n8n.io community workflow templates.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - template_0_id (int): ID of the first matching template
        - template_0_name (str): Name of the first template
        - template_0_description (str): Description of the first template
        - template_0_nodeTypesUsed_0 (str): First node type used in first template
        - template_0_nodeTypesUsed_1 (str): Second node type used in first template
        - template_0_createdAt (str): Creation timestamp of first template (ISO format)
        - template_0_url (str): URL to the first template
        - template_0_usageCount (int): Number of times first template has been used
        - template_1_id (int): ID of the second matching template
        - template_1_name (str): Name of the second template
        - template_1_description (str): Description of the second template
        - template_1_nodeTypesUsed_0 (str): First node type used in second template
        - template_1_nodeTypesUsed_1 (str): Second node type used in second template
        - template_1_createdAt (str): Creation timestamp of second template (ISO format)
        - template_1_url (str): URL to the second template
        - template_1_usageCount (int): Number of times second template has been used
        - totalMatches (int): Total number of templates matching the criteria
        - filtersApplied_nodeTypes_0 (str): First node type queried
        - filtersApplied_limit (int): Maximum number of results returned
        - metadata_timeFetched (str): ISO timestamp when data was fetched
        - metadata_source (str): Source of the data (always 'n8n.io community')
        - metadata_timeRange (str): Time range covered by the results
    """
    return {
        "template_0_id": 1001,
        "template_0_name": "HTTP Request to OpenAI Text Generation",
        "template_0_description": "Fetch data via HTTP and generate text using OpenAI.",
        "template_0_nodeTypesUsed_0": "n8n-nodes-base.httpRequest",
        "template_0_nodeTypesUsed_1": "n8n-nodes-base.openAi",
        "template_0_createdAt": "2023-08-15T10:30:00Z",
        "template_0_url": "https://n8n.io/templates/1001",
        "template_0_usageCount": 154,
        "template_1_id": 1002,
        "template_1_name": "LangChain with OpenAI API Call",
        "template_1_description": "Use LangChain to orchestrate an OpenAI API call.",
        "template_1_nodeTypesUsed_0": "n8n-nodes-base.httpRequest",
        "template_1_nodeTypesUsed_1": "@n8n/n8n-nodes-langchain.openAi",
        "template_1_createdAt": "2023-09-20T14:20:00Z",
        "template_1_url": "https://n8n.io/templates/1002",
        "template_1_usageCount": 98,
        "totalMatches": 27,
        "filtersApplied_nodeTypes_0": "n8n-nodes-base.httpRequest",
        "filtersApplied_limit": 10,
        "metadata_timeFetched": datetime.utcnow().isoformat() + "Z",
        "metadata_source": "n8n.io community",
        "metadata_timeRange": "last_year"
    }


def ennkaheksa_list_node_templates(limit: Optional[int] = 10, nodeTypes: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    List workflow templates that use specific node type(s). Returns ready-to-use workflows from n8n.io community.
    Templates are from the last year (399 total). Use FULL node types like "n8n-nodes-base.httpRequest" or
    "@n8n/n8n-nodes-langchain.openAi". Great for finding proven workflow patterns.

    Args:
        limit (Optional[int]): Maximum number of templates to return. Default is 10.
        nodeTypes (List[str]): Array of node types to search for (e.g., ["n8n-nodes-base.httpRequest", "n8n-nodes-base.openAi"]).

    Returns:
        Dict containing:
        - templates (List[Dict]): List of workflow templates with keys 'id', 'name', 'description', 'nodeTypesUsed',
          'createdAt', 'url', and 'usageCount'.
        - totalMatches (int): Total number of templates found matching the criteria.
        - filtersApplied (Dict): Contains applied filters: 'nodeTypes' and 'limit'.
        - metadata (Dict): Additional metadata including 'timeFetched', 'source', and 'timeRange'.

    Raises:
        ValueError: If nodeTypes is not provided or empty.
    """
    if not nodeTypes:
        raise ValueError("nodeTypes is required and must be a non-empty list.")

    if limit is None:
        limit = 10

    # Fetch simulated external data
    api_data = call_external_api("ennkaheksa-list_node_templates")

    # Construct templates list from indexed flat fields
    templates = []
    for i in range(2):  # We simulate 2 templates from API
        node_types_used = []
        node_type_0_key = f"template_{i}_nodeTypesUsed_0"
        node_type_1_key = f"template_{i}_nodeTypesUsed_1"
        if node_type_0_key in api_data and api_data[node_type_0_key]:
            node_types_used.append(api_data[node_type_0_key])
        if node_type_1_key in api_data and api_data[node_type_1_key]:
            node_types_used.append(api_data[node_type_1_key])

        template = {
            "id": api_data[f"template_{i}_id"],
            "name": api_data[f"template_{i}_name"],
            "description": api_data[f"template_{i}_description"],
            "nodeTypesUsed": node_types_used,
            "createdAt": api_data[f"template_{i}_createdAt"],
            "url": api_data[f"template_{i}_url"],
            "usageCount": api_data[f"template_{i}_usageCount"]
        }
        templates.append(template)

    # Apply limit
    templates = templates[:limit]

    # Build result structure matching output schema
    result = {
        "templates": templates,
        "totalMatches": api_data["totalMatches"],
        "filtersApplied": {
            "nodeTypes": [api_data["filtersApplied_nodeTypes_0"]],
            "limit": api_data["filtersApplied_limit"]
        },
        "metadata": {
            "timeFetched": api_data["metadata_timeFetched"],
            "source": api_data["metadata_source"],
            "timeRange": api_data["metadata_timeRange"]
        }
    }

    return result