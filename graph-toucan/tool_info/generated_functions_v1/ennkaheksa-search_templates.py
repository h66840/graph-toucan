from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for template search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - message (str): Human-readable result message
        - tip (str): Suggestion for improving search
        - template_0_name (str): Name of first matching template
        - template_0_description (str): Description of first template
        - template_0_view_count (int): View count of first template
        - template_0_id (int): ID of first template
        - template_1_name (str): Name of second matching template
        - template_1_description (str): Description of second template
        - template_1_view_count (int): View count of second template
        - template_1_id (int): ID of second template
    """
    return {
        "message": "Found 2 templates matching 'chatbot'",
        "tip": "Try broader keywords like 'automation' or 'AI' for more results.",
        "template_0_name": "AI Chatbot for Customer Support",
        "template_0_description": "A fully automated chatbot using AI to handle customer inquiries.",
        "template_0_view_count": 1543,
        "template_0_id": 101,
        "template_1_name": "Slack Chatbot with Webhook Integration",
        "template_1_description": "Trigger a chatbot in Slack using incoming webhooks and n8n logic.",
        "template_1_view_count": 982,
        "template_1_id": 205,
    }

def ennkaheksa_search_templates(limit: Optional[int] = 20, query: str = "") -> Dict[str, Any]:
    """
    Search workflow templates by keywords in template names and descriptions only.
    
    This function does NOT search by node types. For node-based searches, use list_node_templates.
    Results are limited to templates from the last year and include view counts for popularity.

    Args:
        limit (Optional[int]): Maximum number of results to return. Default is 20.
        query (str): Required search term to match against template names and descriptions.
                    Example values: "chatbot", "automation", "social media", "webhook".

    Returns:
        Dict containing:
            - message (str): Result status message
            - tip (str): Optional suggestion for improving the search
            - templates (List[Dict]): List of matching templates with keys:
                - name (str)
                - description (str)
                - view_count (int)
                - id (int)
              Empty list if no matches found.

    Raises:
        ValueError: If query is empty or not provided.
    """
    if not query:
        return {
            "message": "Search query is required.",
            "tip": "Please provide a keyword like 'chatbot' or 'automation'.",
            "templates": []
        }

    if limit is None:
        limit = 20

    # Fetch simulated external data
    api_data = call_external_api("ennkaheksa-search_templates")

    # Construct templates list from flattened API response
    templates = []
    for i in range(2):  # We expect up to 2 templates from the mock API
        name_key = f"template_{i}_name"
        desc_key = f"template_{i}_description"
        count_key = f"template_{i}_view_count"
        id_key = f"template_{i}_id"

        if name_key in api_data and api_data[name_key] is not None:
            templates.append({
                "name": api_data[name_key],
                "description": api_data[desc_key],
                "view_count": api_data[count_key],
                "id": api_data[id_key]
            })

    # Apply limit
    templates = templates[:limit]

    # Generate message based on results
    if not templates:
        message = f"No templates found for query '{query}'."
        tip = "Try using broader terms like 'automation', 'notification', or 'integration'."
    else:
        message = api_data["message"]
        tip = api_data["tip"]

    return {
        "message": message,
        "tip": tip,
        "templates": templates
    }