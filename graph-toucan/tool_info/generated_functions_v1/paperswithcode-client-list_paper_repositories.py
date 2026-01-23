from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode paper repositories.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - repositories_0_url (str): URL of the first repository
        - repositories_0_name (str): Name of the first repository
        - repositories_0_stars (int): Star count of the first repository
        - repositories_0_language (str): Primary language of the first repository
        - repositories_1_url (str): URL of the second repository
        - repositories_1_name (str): Name of the second repository
        - repositories_1_stars (int): Star count of the second repository
        - repositories_1_language (str): Primary language of the second repository
        - count (int): Total number of repositories linked to the paper
        - page (int): Current page number in the paginated result set
        - pages (int): Total number of pages available for pagination
        - has_next_page (bool): Whether a next page of results exists
        - has_previous_page (bool): Whether a previous page of results exists
    """
    return {
        "repositories_0_url": "https://github.com/author/repo1",
        "repositories_0_name": "Implementation of Paper X",
        "repositories_0_stars": 150,
        "repositories_0_language": "Python",
        "repositories_1_url": "https://github.com/anotheruser/paper-x-implementation",
        "repositories_1_name": "PyTorch Reproduction of Paper X",
        "repositories_1_stars": 89,
        "repositories_1_language": "Python",
        "count": 2,
        "page": 1,
        "pages": 1,
        "has_next_page": False,
        "has_previous_page": False,
    }

def paperswithcode_client_list_paper_repositories(
    paper_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the repositories for a given paper ID in PapersWithCode.

    Args:
        paper_id (str): The unique identifier of the paper on PapersWithCode.
        items_per_page (Optional[int]): Number of repositories to return per page.
        page (Optional[int]): Page number for pagination.

    Returns:
        Dict containing:
        - repositories (List[Dict]): List of repository objects with keys 'url', 'name', 'stars', 'language'
        - count (int): Total number of repositories linked to the paper
        - page (int): Current page number in the paginated result set
        - pages (int): Total number of pages available for pagination
        - has_next_page (bool): Whether a next page of results exists
        - has_previous_page (bool): Whether a previous page of results exists

    Raises:
        ValueError: If paper_id is empty or None.
    """
    if not paper_id:
        raise ValueError("paper_id is required and cannot be empty")

    # Fetch simulated API data
    api_data = call_external_api("paperswithcode-client-list_paper_repositories")

    # Construct repositories list from flattened fields
    repositories = [
        {
            "url": api_data["repositories_0_url"],
            "name": api_data["repositories_0_name"],
            "stars": api_data["repositories_0_stars"],
            "language": api_data["repositories_0_language"]
        },
        {
            "url": api_data["repositories_1_url"],
            "name": api_data["repositories_1_name"],
            "stars": api_data["repositories_1_stars"],
            "language": api_data["repositories_1_language"]
        }
    ]

    # Construct final result matching output schema
    result = {
        "repositories": repositories,
        "count": api_data["count"],
        "page": api_data["page"],
        "pages": api_data["pages"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"]
    }

    return result