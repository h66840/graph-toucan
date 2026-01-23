from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode conference proceedings.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - proceedings_0_title (str): Title of the first proceeding
        - proceedings_0_paper_count (int): Number of papers in the first proceeding
        - proceedings_0_date (str): Date of the first proceeding
        - proceedings_0_url (str): URL of the first proceeding
        - proceedings_1_title (str): Title of the second proceeding
        - proceedings_1_paper_count (int): Number of papers in the second proceeding
        - proceedings_1_date (str): Date of the second proceeding
        - proceedings_1_url (str): URL of the second proceeding
        - total_count (int): Total number of proceedings available
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - conference_id (str): Conference ID used in the request
    """
    return {
        "proceedings_0_title": "NeurIPS 2023 Conference Proceedings",
        "proceedings_0_paper_count": 1200,
        "proceedings_0_date": "2023-12-01",
        "proceedings_0_url": "https://paperswithcode.com/conference/neurips-2023",
        "proceedings_1_title": "NeurIPS 2022 Conference Proceedings",
        "proceedings_1_paper_count": 1100,
        "proceedings_1_date": "2022-12-05",
        "proceedings_1_url": "https://paperswithcode.com/conference/neurips-2022",
        "total_count": 10,
        "page": 1,
        "items_per_page": 2,
        "has_next_page": True,
        "has_previous_page": False,
        "conference_id": "neurips"
    }

def paperswithcode_client_list_conference_proceedings(
    conference_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the proceedings for a given conference ID in PapersWithCode.

    Args:
        conference_id (str): The ID of the conference to retrieve proceedings for.
        items_per_page (Optional[int]): Number of proceedings to return per page.
        page (Optional[int]): Page number to retrieve.

    Returns:
        Dict containing:
        - proceedings (List[Dict]): List of conference proceedings with title, paper_count, date, url.
        - total_count (int): Total number of proceedings available.
        - page (int): Current page number.
        - items_per_page (int): Number of items per page.
        - has_next_page (bool): Whether more pages exist.
        - has_previous_page (bool): Whether previous pages exist.
        - conference_id (str): The requested conference ID.

    Raises:
        ValueError: If conference_id is empty or invalid.
    """
    if not conference_id or not conference_id.strip():
        raise ValueError("conference_id is required and cannot be empty")

    # Normalize conference_id
    conference_id = conference_id.strip()

    # Use defaults if parameters not provided
    effective_items_per_page = items_per_page if items_per_page is not None else 20
    effective_page = page if page is not None else 1

    # Call simulated external API
    api_data = call_external_api("paperswithcode-client-list_conference_proceedings")

    # Construct proceedings list from flattened API response
    proceedings = [
        {
            "title": api_data["proceedings_0_title"],
            "paper_count": api_data["proceedings_0_paper_count"],
            "date": api_data["proceedings_0_date"],
            "url": api_data["proceedings_0_url"]
        },
        {
            "title": api_data["proceedings_1_title"],
            "paper_count": api_data["proceedings_1_paper_count"],
            "date": api_data["proceedings_1_date"],
            "url": api_data["proceedings_1_url"]
        }
    ]

    # Construct final result matching output schema
    result = {
        "proceedings": proceedings,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "conference_id": api_data["conference_id"]
    }

    return result