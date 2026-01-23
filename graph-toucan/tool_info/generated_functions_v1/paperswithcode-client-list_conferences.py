from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode conference list.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - conference_0_name (str): Name of the first conference
        - conference_0_acronym (str): Acronym of the first conference
        - conference_0_website (str): Official website of the first conference
        - conference_0_papers_count (int): Number of papers associated with the first conference
        - conference_0_year (int): Year of the first conference
        - conference_1_name (str): Name of the second conference
        - conference_1_acronym (str): Acronym of the second conference
        - conference_1_website (str): Official website of the second conference
        - conference_1_papers_count (int): Number of papers associated with the second conference
        - conference_1_year (int): Year of the second conference
        - count (int): Total number of conferences matching the query
        - page (int): Current page number
        - pages (int): Total number of pages available
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - results_per_page (int): Number of results per page
    """
    return {
        "conference_0_name": "Conference on Neural Information Processing Systems",
        "conference_0_acronym": "NeurIPS",
        "conference_0_website": "https://neurips.cc",
        "conference_0_papers_count": 1200,
        "conference_0_year": 2023,
        "conference_1_name": "International Conference on Learning Representations",
        "conference_1_acronym": "ICLR",
        "conference_1_website": "https://iclr.cc",
        "conference_1_papers_count": 980,
        "conference_1_year": 2023,
        "count": 25,
        "page": 1,
        "pages": 3,
        "has_next_page": True,
        "has_previous_page": False,
        "results_per_page": 10
    }

def paperswithcode_client_list_conferences(
    conference_name: Optional[str] = None,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the conferences in PapersWithCode.

    Args:
        conference_name (Optional[str]): Filter conferences by name. Defaults to None.
        items_per_page (Optional[int]): Number of items to return per page. Defaults to None.
        page (Optional[int]): Page number to retrieve. Defaults to None.

    Returns:
        Dict containing:
        - conferences (List[Dict]): List of conference objects with name, acronym, website,
          papers_count, and year.
        - count (int): Total number of conferences.
        - page (int): Current page number.
        - pages (int): Total number of pages.
        - has_next_page (bool): Whether next page exists.
        - has_previous_page (bool): Whether previous page exists.
        - results_per_page (int): Number of results per page.

    Raises:
        ValueError: If items_per_page or page is less than 1.
    """
    # Input validation
    if items_per_page is not None and items_per_page < 1:
        raise ValueError("items_per_page must be at least 1")
    if page is not None and page < 1:
        raise ValueError("page must be at least 1")

    # Fetch simulated API data
    api_data = call_external_api("paperswithcode-client-list_conferences")

    # Construct conferences list from flattened API response
    conferences = [
        {
            "name": api_data["conference_0_name"],
            "acronym": api_data["conference_0_acronym"],
            "website": api_data["conference_0_website"],
            "papers_count": api_data["conference_0_papers_count"],
            "year": api_data["conference_0_year"]
        },
        {
            "name": api_data["conference_1_name"],
            "acronym": api_data["conference_1_acronym"],
            "website": api_data["conference_1_website"],
            "papers_count": api_data["conference_1_papers_count"],
            "year": api_data["conference_1_year"]
        }
    ]

    # Apply conference name filter if provided
    if conference_name is not None:
        conference_name_lower = conference_name.lower()
        conferences = [
            conf for conf in conferences
            if conference_name_lower in conf["name"].lower()
            or (conf["acronym"] and conference_name_lower in conf["acronym"].lower())
        ]

    # Return final structured response
    return {
        "conferences": conferences,
        "count": api_data["count"],
        "page": api_data["page"],
        "pages": api_data["pages"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "results_per_page": api_data["results_per_page"]
    }