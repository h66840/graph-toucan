from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode paper results.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_task (str): Task name for the first result
        - result_0_method (str): Method name for the first result
        - result_0_metrics_mae (float): MAE metric value for the first result
        - result_0_metrics_rmse (float): RMSE metric value for the first result
        - result_0_model_name (str): Model name for the first result
        - result_0_model_link (str): Model URL for the first result
        - result_1_task (str): Task name for the second result
        - result_1_method (str): Method name for the second result
        - result_1_metrics_mae (float): MAE metric value for the second result
        - result_1_metrics_rmse (float): RMSE metric value for the second result
        - result_1_model_name (str): Model name for the second result
        - result_1_model_link (str): Model URL for the second result
        - count (int): Total number of results available
        - page (int): Current page number
        - pages (int): Total number of pages
        - next_page (str): URL for next page or null
        - previous_page (str): URL for previous page or null
        - paper_id (str): The paper ID these results are associated with
        - metadata_timestamp (str): Timestamp of data retrieval
        - metadata_api_version (str): API version used
        - metadata_source_domain (str): Source domain of the data
    """
    return {
        "result_0_task": "Machine Translation",
        "result_0_method": "Transformer",
        "result_0_metrics_mae": 0.85,
        "result_0_metrics_rmse": 0.92,
        "result_0_model_name": "Transformer-Big",
        "result_0_model_link": "https://example.com/models/transformer-big",
        "result_1_task": "Text Summarization",
        "result_1_method": "BART",
        "result_1_metrics_mae": 0.78,
        "result_1_metrics_rmse": 0.88,
        "result_1_model_name": "BART-Large",
        "result_1_model_link": "https://example.com/models/bart-large",
        "count": 15,
        "page": 1,
        "pages": 3,
        "next_page": "https://api.paperswithcode.com/papers/example-paper-id/results?page=2",
        "previous_page": None,
        "paper_id": "example-paper-id",
        "metadata_timestamp": "2023-10-01T12:00:00Z",
        "metadata_api_version": "v1",
        "metadata_source_domain": "paperswithcode.com"
    }

def paperswithcode_client_list_paper_results(
    paper_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the results for a given paper ID in PapersWithCode.

    Args:
        paper_id (str): The unique identifier of the paper (required)
        items_per_page (Optional[int]): Number of items to return per page
        page (Optional[int]): Page number to retrieve

    Returns:
        Dict containing:
        - results (List[Dict]): List of result entries with task, method, metrics, and model info
        - count (int): Total number of results available
        - page (int): Current page number
        - pages (int): Total number of pages
        - next_page (str): URL for next page or None
        - previous_page (str): URL for previous page or None
        - paper_id (str): The paper ID these results are associated with
        - metadata (Dict): Additional contextual information

    Raises:
        ValueError: If paper_id is empty or None
    """
    if not paper_id:
        raise ValueError("paper_id is required")

    # Fetch simulated external data
    api_data = call_external_api("paperswithcode-client-list_paper_results")

    # Construct results list from indexed flat fields
    results = [
        {
            "task": api_data["result_0_task"],
            "method": api_data["result_0_method"],
            "metrics": {
                "mae": api_data["result_0_metrics_mae"],
                "rmse": api_data["result_0_metrics_rmse"]
            },
            "model": {
                "name": api_data["result_0_model_name"],
                "link": api_data["result_0_model_link"]
            }
        },
        {
            "task": api_data["result_1_task"],
            "method": api_data["result_1_method"],
            "metrics": {
                "mae": api_data["result_1_metrics_mae"],
                "rmse": api_data["result_1_metrics_rmse"]
            },
            "model": {
                "name": api_data["result_1_model_name"],
                "link": api_data["result_1_model_link"]
            }
        }
    ]

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "api_version": api_data["metadata_api_version"],
        "source_domain": api_data["metadata_source_domain"]
    }

    # Build final response structure
    response = {
        "results": results,
        "count": api_data["count"],
        "page": api_data["page"],
        "pages": api_data["pages"],
        "next_page": api_data["next_page"],
        "previous_page": api_data["previous_page"],
        "paper_id": api_data["paper_id"],
        "metadata": metadata
    }

    return response