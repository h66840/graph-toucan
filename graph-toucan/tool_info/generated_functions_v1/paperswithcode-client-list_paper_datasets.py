from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode paper datasets.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - dataset_0_id (str): ID of the first dataset
        - dataset_0_name (str): Name of the first dataset
        - dataset_0_description (str): Description of the first dataset
        - dataset_0_url (str): URL of the first dataset
        - dataset_0_paper_id (str): Paper ID associated with the first dataset
        - dataset_1_id (str): ID of the second dataset
        - dataset_1_name (str): Name of the second dataset
        - dataset_1_description (str): Description of the second dataset
        - dataset_1_url (str): URL of the second dataset
        - dataset_1_paper_id (str): Paper ID associated with the second dataset
        - count (int): Total number of datasets available
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - meta_api_version (str): API version
        - meta_response_timestamp (str): Timestamp of the response
        - meta_rate_limit_remaining (int): Remaining rate limit count
    """
    return {
        "dataset_0_id": "imagenet",
        "dataset_0_name": "ImageNet",
        "dataset_0_description": "A large-scale image classification dataset with over 14 million images.",
        "dataset_0_url": "https://paperswithcode.com/dataset/imagenet",
        "dataset_0_paper_id": "resnet",
        "dataset_1_id": "cifar10",
        "dataset_1_name": "CIFAR-10",
        "dataset_1_description": "A dataset of 32x32 color images of 10 classes.",
        "dataset_1_url": "https://paperswithcode.com/dataset/cifar10",
        "dataset_1_paper_id": "resnet",
        "count": 2,
        "page": 1,
        "items_per_page": 2,
        "has_next_page": False,
        "has_previous_page": False,
        "meta_api_version": "v1",
        "meta_response_timestamp": "2023-10-01T12:00:00Z",
        "meta_rate_limit_remaining": 987
    }

def paperswithcode_client_list_paper_datasets(paper_id: str, items_per_page: Optional[int] = None, page: Optional[int] = None) -> Dict[str, Any]:
    """
    List the datasets for a given paper ID in PapersWithCode.

    Args:
        paper_id (str): The ID of the paper to retrieve datasets for (required).
        items_per_page (Optional[int]): Number of datasets to return per page (optional).
        page (Optional[int]): Page number to retrieve (optional).

    Returns:
        Dict containing:
            - datasets (List[Dict]): List of dataset objects with keys 'id', 'name', 'description', 'url', 'paper_id'
            - count (int): Total number of datasets available
            - page (int): Current page number
            - items_per_page (int): Number of datasets per page
            - has_next_page (bool): Whether next page exists
            - has_previous_page (bool): Whether previous page exists
            - meta (Dict): Metadata including API version, timestamp, and rate limit info

    Raises:
        ValueError: If paper_id is empty or invalid.
    """
    if not paper_id or not paper_id.strip():
        raise ValueError("paper_id is required and cannot be empty")

    # Normalize paper_id
    paper_id = paper_id.strip()

    # Call simulated external API
    api_data = call_external_api("paperswithcode-client-list_paper_datasets")

    # Construct datasets list from flattened fields
    datasets = [
        {
            "id": api_data["dataset_0_id"],
            "name": api_data["dataset_0_name"],
            "description": api_data["dataset_0_description"],
            "url": api_data["dataset_0_url"],
            "paper_id": api_data["dataset_0_paper_id"]
        },
        {
            "id": api_data["dataset_1_id"],
            "name": api_data["dataset_1_name"],
            "description": api_data["dataset_1_description"],
            "url": api_data["dataset_1_url"],
            "paper_id": api_data["dataset_1_paper_id"]
        }
    ]

    # Construct meta dictionary
    meta = {
        "api_version": api_data["meta_api_version"],
        "response_timestamp": api_data["meta_response_timestamp"],
        "rate_limit_remaining": api_data["meta_rate_limit_remaining"]
    }

    # Build final result
    result = {
        "datasets": datasets,
        "count": api_data["count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "meta": meta
    }

    return result