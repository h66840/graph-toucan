from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode author search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_name (str): Name of the first matching author
        - result_0_id (str): ID of the first author
        - result_0_affiliation (str): Affiliation of the first author
        - result_0_paper_count (int): Number of papers by the first author
        - result_1_name (str): Name of the second matching author
        - result_1_id (str): ID of the second author
        - result_1_affiliation (str): Affiliation of the second author
        - result_1_paper_count (int): Number of papers by the second author
        - total_count (int): Total number of authors found
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether next page exists
        - has_previous_page (bool): Whether previous page exists
        - query (str): Search query used
    """
    return {
        "result_0_name": "Andrew Ng",
        "result_0_id": "andrew-ng-1",
        "result_0_affiliation": "Stanford University",
        "result_0_paper_count": 150,
        "result_1_name": "Yoshua Bengio",
        "result_1_id": "yoshua-bengio-1",
        "result_1_affiliation": "Université de Montréal",
        "result_1_paper_count": 142,
        "total_count": 2,
        "page": 1,
        "items_per_page": 20,
        "has_next_page": False,
        "has_previous_page": False,
        "query": "Ng"
    }

def paperswithcode_client_search_authors(
    full_name: str, 
    items_per_page: Optional[int] = None, 
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    Search for authors by name in PapersWithCode.
    
    Args:
        full_name (str): Full name of the author to search for.
        items_per_page (Optional[int]): Number of authors to return per page. Defaults to 20 if not specified.
        page (Optional[int]): Page number to retrieve. Defaults to 1 if not specified.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of author objects with keys: name, id, affiliation, paper_count
        - total_count (int): Total number of matching authors
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - query (str): The search query used
    
    Raises:
        ValueError: If full_name is empty or invalid.
    """
    if not full_name or not full_name.strip():
        raise ValueError("full_name is required and cannot be empty")
    
    if items_per_page is None:
        items_per_page = 20
    if page is None:
        page = 1
    
    if items_per_page <= 0:
        raise ValueError("items_per_page must be a positive integer")
    if page <= 0:
        raise ValueError("page must be a positive integer")
    
    # Call the external API simulation
    api_data = call_external_api("paperswithcode-client-search_authors")
    
    # Construct the results list from flattened API response
    results = [
        {
            "name": api_data["result_0_name"],
            "id": api_data["result_0_id"],
            "affiliation": api_data["result_0_affiliation"],
            "paper_count": api_data["result_0_paper_count"]
        },
        {
            "name": api_data["result_1_name"],
            "id": api_data["result_1_id"],
            "affiliation": api_data["result_1_affiliation"],
            "paper_count": api_data["result_1_paper_count"]
        }
    ]
    
    # Construct final response matching output schema
    return {
        "results": results,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "query": api_data["query"]
    }