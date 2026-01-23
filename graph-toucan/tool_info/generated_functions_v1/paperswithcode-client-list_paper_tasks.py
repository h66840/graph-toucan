from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode task listing.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first task
        - result_0_id (str): ID of the first task
        - result_0_description (str): Description of the first task
        - result_1_name (str): Name of the second task
        - result_1_id (str): ID of the second task
        - result_1_description (str): Description of the second task
        - count (int): Number of tasks in current page
        - total_count (int): Total number of tasks available
        - page (int): Current page number
        - pages (int): Total number of pages
        - has_next (bool): Whether next page exists
        - has_previous (bool): Whether previous page exists
        - paper_id (str): The paper ID echoed from input
    """
    return {
        "result_0_name": "Image Classification",
        "result_0_id": "image-classification",
        "result_0_description": "Classifying images into predefined categories.",
        "result_1_name": "Object Detection",
        "result_1_id": "object-detection",
        "result_1_description": "Detecting objects within images with bounding boxes.",
        "count": 2,
        "total_count": 5,
        "page": 1,
        "pages": 3,
        "has_next": True,
        "has_previous": False,
        "paper_id": "transformer-vision-2023"
    }

def paperswithcode_client_list_paper_tasks(
    paper_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the tasks for a given paper ID in PapersWithCode.

    Args:
        paper_id (str): The ID of the paper to retrieve tasks for (required).
        items_per_page (Optional[int]): Number of items to return per page.
        page (Optional[int]): Page number to retrieve.

    Returns:
        Dict containing:
            - results (List[Dict]): List of task objects with name, ID, and description.
            - count (int): Number of tasks returned in this page.
            - total_count (int): Total number of tasks across all pages.
            - page (int): Current page number.
            - pages (int): Total number of pages.
            - has_next (bool): Whether a next page exists.
            - has_previous (bool): Whether a previous page exists.
            - paper_id (str): The paper ID echoed from input.

    Raises:
        ValueError: If paper_id is empty or None.
    """
    if not paper_id:
        raise ValueError("paper_id is required and cannot be empty")

    # Fetch simulated API data
    api_data = call_external_api("paperswithcode-client-list_paper_tasks")

    # Construct results list from flattened fields
    results = [
        {
            "name": api_data["result_0_name"],
            "id": api_data["result_0_id"],
            "description": api_data["result_0_description"]
        },
        {
            "name": api_data["result_1_name"],
            "id": api_data["result_1_id"],
            "description": api_data["result_1_description"]
        }
    ]

    # Build final response structure
    return {
        "results": results,
        "count": api_data["count"],
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "pages": api_data["pages"],
        "has_next": api_data["has_next"],
        "has_previous": api_data["has_previous"],
        "paper_id": api_data["paper_id"]
    }