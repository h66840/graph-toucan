from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode research area tasks.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - task_0_id (str): ID of the first task
        - task_0_name (str): Name of the first task
        - task_0_description (str): Description of the first task
        - task_0_paper_count (int): Number of papers associated with the first task
        - task_0_dataset_count (int): Number of datasets associated with the first task
        - task_0_average_3_year_acr (float): Average 3-year ACR for the first task
        - task_1_id (str): ID of the second task
        - task_1_name (str): Name of the second task
        - task_1_description (str): Description of the second task
        - task_1_paper_count (int): Number of papers associated with the second task
        - task_1_dataset_count (int): Number of datasets associated with the second task
        - task_1_average_3_year_acr (float): Average 3-year ACR for the second task
        - total_count (int): Total number of tasks in the research area
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - research_area_name (str): Name of the research area
        - metadata_api_version (str): Version of the API
        - metadata_request_timestamp (str): Timestamp of the request
        - metadata_rate_limit_remaining (int): Remaining rate limit count
    """
    return {
        "task_0_id": "image-classification",
        "task_0_name": "Image Classification",
        "task_0_description": "Classifying images into predefined categories.",
        "task_0_paper_count": 1500,
        "task_0_dataset_count": 45,
        "task_0_average_3_year_acr": 12.5,
        "task_1_id": "object-detection",
        "task_1_name": "Object Detection",
        "task_1_description": "Detecting objects within images with bounding boxes.",
        "task_1_paper_count": 1200,
        "task_1_dataset_count": 38,
        "task_1_average_3_year_acr": 11.8,
        "total_count": 2700,
        "page": 1,
        "items_per_page": 2,
        "has_next_page": True,
        "has_previous_page": False,
        "research_area_name": "Computer Vision",
        "metadata_api_version": "v1",
        "metadata_request_timestamp": "2023-10-01T12:00:00Z",
        "metadata_rate_limit_remaining": 987
    }

def paperswithcode_client_list_research_area_tasks(
    area_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the tasks for a given research area ID in PapersWithCode.

    Args:
        area_id (str): The ID of the research area (e.g., "computer-vision").
        items_per_page (Optional[int]): Number of items to return per page. Defaults to 2 if not provided.
        page (Optional[int]): Page number to retrieve. Defaults to 1 if not provided.

    Returns:
        Dict containing:
        - tasks (List[Dict]): List of task objects with details like id, name, description, etc.
        - total_count (int): Total number of tasks available in the research area.
        - page (int): The current page number.
        - items_per_page (int): Number of tasks returned per page.
        - has_next_page (bool): Whether there is a next page of results.
        - has_previous_page (bool): Whether there is a previous page of results.
        - research_area_name (str): Name of the research area.
        - metadata (Dict): Additional information about the response including API version, timestamp, and rate limit.

    Raises:
        ValueError: If area_id is empty or invalid.
    """
    if not area_id or not area_id.strip():
        raise ValueError("area_id is required and cannot be empty")

    # Use defaults if parameters not provided
    effective_items_per_page = items_per_page if items_per_page is not None else 2
    effective_page = page if page is not None else 1

    # Fetch simulated external data
    api_data = call_external_api("paperswithcode-client-list_research_area_tasks")

    # Construct tasks list from flattened fields
    tasks = [
        {
            "id": api_data["task_0_id"],
            "name": api_data["task_0_name"],
            "description": api_data["task_0_description"],
            "paper_count": api_data["task_0_paper_count"],
            "dataset_count": api_data["task_0_dataset_count"],
            "average_3_year_acr": api_data["task_0_average_3_year_acr"]
        },
        {
            "id": api_data["task_1_id"],
            "name": api_data["task_1_name"],
            "description": api_data["task_1_description"],
            "paper_count": api_data["task_1_paper_count"],
            "dataset_count": api_data["task_1_dataset_count"],
            "average_3_year_acr": api_data["task_1_average_3_year_acr"]
        }
    ]

    # Construct metadata
    metadata = {
        "api_version": api_data["metadata_api_version"],
        "request_timestamp": api_data["metadata_request_timestamp"],
        "rate_limit_remaining": api_data["metadata_rate_limit_remaining"]
    }

    # Build final result structure
    result = {
        "tasks": tasks,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "research_area_name": api_data["research_area_name"],
        "metadata": metadata
    }

    return result