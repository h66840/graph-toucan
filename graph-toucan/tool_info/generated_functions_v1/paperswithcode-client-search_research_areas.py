from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode research areas search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first research area
        - result_0_name (str): Name of the first research area
        - result_0_paper_count (int): Number of papers in the first research area
        - result_0_task_count (int): Number of tasks in the first research area
        - result_0_description (str): Description of the first research area
        - result_1_id (str): ID of the second research area
        - result_1_name (str): Name of the second research area
        - result_1_paper_count (int): Number of papers in the second research area
        - result_1_task_count (int): Number of tasks in the second research area
        - result_1_description (str): Description of the second research area
        - count (int): Total number of research areas returned
        - next (str): URL for the next page, or empty string if none
        - previous (str): URL for the previous page, or empty string if none
        - page_size (int): Number of items per page
    """
    return {
        "result_0_id": "nlp",
        "result_0_name": "Natural Language Processing",
        "result_0_paper_count": 15000,
        "result_0_task_count": 200,
        "result_0_description": "Research area focused on interaction between computers and human language.",
        "result_1_id": "cv",
        "result_1_name": "Computer Vision",
        "result_1_paper_count": 18000,
        "result_1_task_count": 250,
        "result_1_description": "Field concerned with enabling computers to interpret and understand visual information.",
        "count": 2,
        "next": "https://api.paperswithcode.com/research-areas?page=2",
        "previous": "",
        "page_size": 2
    }

def paperswithcode_client_search_research_areas(
    name: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for research areas that exist in PapersWithCode.
    
    Args:
        name (str): Required. Name of the research area to search for.
        items_per_page (Optional[int]): Optional. Number of items to return per page.
        page (Optional[int]): Optional. Page number to retrieve.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of research area entries with 'id', 'name', 'paper_count', 
          'task_count', and 'description' fields.
        - count (int): Total number of research areas returned.
        - next (str): URL to fetch the next page of results, or None if no more pages.
        - previous (str): URL to fetch the previous page of results, or None if on first page.
        - page_size (int): Number of items per page in the current response.
    
    Raises:
        ValueError: If name is empty or not provided.
    """
    if not name or not name.strip():
        raise ValueError("Parameter 'name' is required and cannot be empty.")
    
    # Fetch simulated API data
    api_data = call_external_api("paperswithcode-client-search_research_areas")
    
    # Construct results list from indexed fields
    results = [
        {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "paper_count": api_data["result_0_paper_count"],
            "task_count": api_data["result_0_task_count"],
            "description": api_data["result_0_description"]
        },
        {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "paper_count": api_data["result_1_paper_count"],
            "task_count": api_data["result_1_task_count"],
            "description": api_data["result_1_description"]
        }
    ]
    
    # Build final response structure
    response = {
        "results": results,
        "count": api_data["count"],
        "next": api_data["next"] if api_data["next"] else None,
        "previous": api_data["previous"] if api_data["previous"] else None,
        "page_size": api_data["page_size"]
    }
    
    return response