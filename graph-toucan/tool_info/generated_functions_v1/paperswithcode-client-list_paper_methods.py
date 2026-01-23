from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode client to list paper methods.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_method_name (str): Name of the first method
        - result_0_description (str): Description of the first method
        - result_1_method_name (str): Name of the second method
        - result_1_description (str): Description of the second method
        - count (int): Total number of methods available
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - paper_id (str): The paper ID these methods belong to
        - metadata_api_version (str): Version of the API
        - metadata_timestamp (str): Timestamp of the response
        - metadata_source_url (str): Source URL of the data
    """
    return {
        "result_0_method_name": "Transformer",
        "result_0_description": "A deep learning model based on self-attention mechanisms.",
        "result_1_method_name": "BERT",
        "result_1_description": "Bidirectional Encoder Representations from Transformers.",
        "count": 2,
        "page": 1,
        "items_per_page": 2,
        "has_next_page": False,
        "has_previous_page": False,
        "paper_id": "attention-is-all-you-need",
        "metadata_api_version": "v1",
        "metadata_timestamp": "2023-10-01T12:00:00Z",
        "metadata_source_url": "https://api.paperswithcode.com/v1/papers/attention-is-all-you-need/methods"
    }

def paperswithcode_client_list_paper_methods(
    paper_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the methods for a given paper ID in PapersWithCode.
    
    Args:
        paper_id (str): The ID of the paper to retrieve methods for (required).
        items_per_page (Optional[int]): Number of results to return per page.
        page (Optional[int]): Page number to retrieve (for pagination).
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of method entries with name and description.
        - count (int): Total number of methods available.
        - page (int): Current page number.
        - items_per_page (int): Number of items per page.
        - has_next_page (bool): Whether more pages exist.
        - has_previous_page (bool): Whether a previous page exists.
        - paper_id (str): The paper ID these methods belong to.
        - metadata (Dict): Additional info like API version, timestamp, source URL.
    
    Raises:
        ValueError: If paper_id is empty or None.
    """
    if not paper_id:
        raise ValueError("paper_id is required and cannot be empty")

    # Use defaults if parameters not provided
    effective_page = page if page is not None else 1
    effective_items_per_page = items_per_page if items_per_page is not None else 10

    # Fetch simulated external data
    api_data = call_external_api("paperswithcode-client-list_paper_methods")

    # Construct results list from indexed fields
    results = [
        {
            "method_name": api_data["result_0_method_name"],
            "description": api_data["result_0_description"]
        },
        {
            "method_name": api_data["result_1_method_name"],
            "description": api_data["result_1_description"]
        }
    ]

    # Construct metadata
    metadata = {
        "api_version": api_data["metadata_api_version"],
        "timestamp": api_data["metadata_timestamp"],
        "source_url": api_data["metadata_source_url"]
    }

    # Build final response structure
    response = {
        "results": results,
        "count": api_data["count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "paper_id": api_data["paper_id"],
        "metadata": metadata
    }

    return response