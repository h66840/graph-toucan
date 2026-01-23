from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for retrieving documentation index.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - index_content (str): Markdown-formatted string listing available documentation pages
        - doc_name (str): Name of the documentation set
        - page_count (int): Total number of pages in the index
        - item_0_title (str): Title of the first available page
        - item_0_page_id (str): Page ID of the first available page
        - item_0_description (str): Description of the first available page
        - item_1_title (str): Title of the second available page
        - item_1_page_id (str): Page ID of the second available page
        - item_1_description (str): Description of the second available page
        - retrieval_timestamp (str): ISO 8601 timestamp when index was retrieved
        - next_steps_hint (str): Suggested follow-up action
    """
    return {
        "index_content": "# Atlas Docs Index\n\n- [Getting Started](/getting-started)\n- [API Reference](/api-reference)\n- [Configuration Guide](/configuration)",
        "doc_name": "Atlas Documentation",
        "page_count": 3,
        "item_0_title": "Getting Started",
        "item_0_page_id": "getting-started",
        "item_0_description": "Learn how to set up and run Atlas for the first time.",
        "item_1_title": "API Reference",
        "item_1_page_id": "api-reference",
        "item_1_description": "Complete API endpoints and request/response examples.",
        "retrieval_timestamp": datetime.now().isoformat(),
        "next_steps_hint": "Use get_docs_page with a specific page_id to retrieve full content."
    }

def atlas_docs_get_docs_index(docName: str) -> Dict[str, Any]:
    """
    Retrieves a condensed, LLM-friendly index of the pages in a documentation set.
    
    This function is used for initial exploration to understand what's covered and identify relevant pages.
    It returns a structured index with metadata about available documentation pages.
    
    Args:
        docName (str): Name of the documentation set (required)
    
    Returns:
        Dict containing:
        - index_content (str): Markdown-formatted string with list of available pages
        - doc_name (str): Name of the documentation set
        - page_count (int): Total number of pages listed
        - available_pages (List[Dict]): List of page entries with title, page_id, and optional description
        - retrieval_timestamp (str): ISO 8601 timestamp of retrieval
        - next_steps_hint (str): Guidance on next steps (e.g., using get_docs_page)
    
    Raises:
        ValueError: If docName is empty or not a string
    """
    if not docName or not isinstance(docName, str):
        raise ValueError("docName must be a non-empty string")
    
    # Call simulated external API
    api_data = call_external_api("atlas-docs-get_docs_index")
    
    # Construct available_pages list from indexed fields
    available_pages: List[Dict[str, str]] = [
        {
            "title": api_data["item_0_title"],
            "page_id": api_data["item_0_page_id"],
            "description": api_data["item_0_description"]
        },
        {
            "title": api_data["item_1_title"],
            "page_id": api_data["item_1_page_id"],
            "description": api_data["item_1_description"]
        }
    ]
    
    # Build final result structure matching output schema
    result = {
        "index_content": api_data["index_content"],
        "doc_name": api_data["doc_name"],
        "page_count": api_data["page_count"],
        "available_pages": available_pages,
        "retrieval_timestamp": api_data["retrieval_timestamp"],
        "next_steps_hint": api_data["next_steps_hint"]
    }
    
    return result