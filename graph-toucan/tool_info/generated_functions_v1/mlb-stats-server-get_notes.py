from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for MLB stats server notes.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - note_0_title (str): Title of the first note
        - note_0_content (str): Content of the first note
        - note_0_category (str): Category of the first note
        - note_0_last_updated (str): Last updated timestamp of the first note in ISO format
        - note_1_title (str): Title of the second note
        - note_1_content (str): Content of the second note
        - note_1_category (str): Category of the second note
        - note_1_last_updated (str): Last updated timestamp of the second note in ISO format
        - endpoint_name (str): The name or path of the endpoint
        - has_notes (bool): Whether any notes exist for the endpoint
        - total_note_count (int): Total number of notes returned
        - metadata_retrieval_timestamp (str): Timestamp when data was retrieved, in ISO format
        - metadata_source_version (str): Version of the data source
        - metadata_api_documentation_link (str): URL to the API documentation
    """
    return {
        "note_0_title": "Data Format Change",
        "note_0_content": "Starting from v3.1, this endpoint returns player IDs as strings instead of integers.",
        "note_0_category": "breaking_change",
        "note_0_last_updated": "2023-10-05T08:30:00Z",
        "note_1_title": "Rate Limit Increase",
        "note_1_content": "Rate limit has been increased to 1000 requests per minute for authenticated users.",
        "note_1_category": "performance",
        "note_1_last_updated": "2023-09-12T14:22:00Z",
        "endpoint_name": "/api/v1/players/stats",
        "has_notes": True,
        "total_note_count": 2,
        "metadata_retrieval_timestamp": datetime.utcnow().isoformat() + "Z",
        "metadata_source_version": "v3.1.4",
        "metadata_api_documentation_link": "https://api.mlb.com/docs/v3"
    }


def mlb_stats_server_get_notes(endpoint: str) -> Dict[str, Any]:
    """
    Get additional notes on an MLB stats server endpoint.

    Args:
        endpoint (str): The endpoint path or name to retrieve notes for.

    Returns:
        Dict containing:
        - notes (List[Dict]): List of note objects with title, content, category, and last_updated fields.
        - endpoint_name (str): The name or path of the endpoint.
        - has_notes (bool): Indicates whether any notes exist for the endpoint.
        - total_note_count (int): Total number of notes returned.
        - metadata (Dict): Additional metadata about the response including retrieval timestamp,
          source version, and API documentation link.

    Raises:
        ValueError: If endpoint is empty or not provided.
    """
    if not endpoint or not endpoint.strip():
        raise ValueError("Parameter 'endpoint' is required and cannot be empty.")

    # Call external API to get flattened data
    api_data = call_external_api("mlb-stats-server-get_notes")

    # Construct notes list from indexed fields
    notes = [
        {
            "title": api_data["note_0_title"],
            "content": api_data["note_0_content"],
            "category": api_data["note_0_category"],
            "last_updated": api_data["note_0_last_updated"]
        },
        {
            "title": api_data["note_1_title"],
            "content": api_data["note_1_content"],
            "category": api_data["note_1_category"],
            "last_updated": api_data["note_1_last_updated"]
        }
    ]

    # Construct metadata dictionary
    metadata = {
        "retrieval_timestamp": api_data["metadata_retrieval_timestamp"],
        "source_version": api_data["metadata_source_version"],
        "api_documentation_link": api_data["metadata_api_documentation_link"]
    }

    # Build final result structure
    result = {
        "notes": notes,
        "endpoint_name": api_data["endpoint_name"],
        "has_notes": api_data["has_notes"],
        "total_note_count": api_data["total_note_count"],
        "metadata": metadata
    }

    return result