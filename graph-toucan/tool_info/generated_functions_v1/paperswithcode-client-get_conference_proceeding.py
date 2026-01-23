from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode conference proceeding.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): The title of the conference proceeding
        - event (str): Name of the associated conference or event (e.g., NeurIPS, ICML)
        - year (int): Year in which the proceeding was published
        - paper_count (int): Number of papers included in this proceeding
        - start_date (str): Start date of the conference (ISO format string, e.g., '2023-12-05')
        - end_date (str): End date of the conference (ISO format string)
        - location (str): Geographic location of the conference
        - url (str): URL to the official proceeding page on PapersWithCode
        - papers_0_title (str): Title of the first paper in the proceeding
        - papers_0_authors (str): Authors of the first paper (comma-separated)
        - papers_0_url (str): URL to the first paper on PapersWithCode
        - papers_0_code_count (int): Number of code repositories linked to the first paper
        - papers_0_task (str): Research task/category of the first paper
        - papers_1_title (str): Title of the second paper in the proceeding
        - papers_1_authors (str): Authors of the second paper (comma-separated)
        - papers_1_url (str): URL to the second paper on PapersWithCode
        - papers_1_code_count (int): Number of code repositories linked to the second paper
        - papers_1_task (str): Research task/category of the second paper
        - has_next (bool): Indicates if there is a next proceeding (e.g., future edition)
        - has_previous (bool): Indicates if there is a previous proceeding (e.g., past edition)
        - next_proceeding_id (str): ID of the next proceeding in the sequence, if available
        - previous_proceeding_id (str): ID of the previous proceeding in the sequence, if available
    """
    return {
        "title": "Proceedings of the 37th International Conference on Machine Learning",
        "event": "ICML",
        "year": 2023,
        "paper_count": 1200,
        "start_date": "2023-07-23",
        "end_date": "2023-07-29",
        "location": "Honolulu, Hawaii",
        "url": "https://paperswithcode.com/conference/icml-2023",
        "papers_0_title": "Attention Is All You Need",
        "papers_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin",
        "papers_0_url": "https://paperswithcode.com/paper/attention-is-all-you-need",
        "papers_0_code_count": 5,
        "papers_0_task": "Machine Translation",
        "papers_1_title": "Deep Residual Learning for Image Recognition",
        "papers_1_authors": "Kaiming He, Xiangyu Zhang, Shaoqing Ren, Jian Sun",
        "papers_1_url": "https://paperswithcode.com/paper/deep-residual-learning-for-image-recognition",
        "papers_1_code_count": 8,
        "papers_1_task": "Image Classification",
        "has_next": True,
        "has_previous": True,
        "next_proceeding_id": "icml-2024",
        "previous_proceeding_id": "icml-2022"
    }

def paperswithcode_client_get_conference_proceeding(conference_id: str, proceeding_id: str) -> Dict[str, Any]:
    """
    Get a proceeding by ID in PapersWithCode.

    Args:
        conference_id (str): The ID of the conference (e.g., 'icml', 'neurips')
        proceeding_id (str): The ID of the proceeding (e.g., 'icml-2023')

    Returns:
        Dict containing the following keys:
        - title (str): The title of the conference proceeding
        - event (str): Name of the associated conference or event (e.g., NeurIPS, ICML)
        - year (int): Year in which the proceeding was published
        - paper_count (int): Number of papers included in this proceeding
        - start_date (str): Start date of the conference (ISO format string)
        - end_date (str): End date of the conference (ISO format string)
        - location (str): Geographic location of the conference
        - url (str): URL to the official proceeding page on PapersWithCode
        - papers (List[Dict]): List of papers in this proceeding, each containing:
            - title (str)
            - authors (str)
            - url (str)
            - code_count (int)
            - task (str)
        - has_next (bool): Indicates if there is a next proceeding
        - has_previous (bool): Indicates if there is a previous proceeding
        - next_proceeding_id (str): ID of the next proceeding in the sequence
        - previous_proceeding_id (str): ID of the previous proceeding in the sequence

    Raises:
        ValueError: If conference_id or proceeding_id is empty
    """
    if not conference_id:
        raise ValueError("conference_id is required")
    if not proceeding_id:
        raise ValueError("proceeding_id is required")

    # Fetch data from external API (simulated)
    api_data = call_external_api("paperswithcode-client-get_conference_proceeding")

    # Construct papers list from indexed fields
    papers = [
        {
            "title": api_data["papers_0_title"],
            "authors": api_data["papers_0_authors"],
            "url": api_data["papers_0_url"],
            "code_count": api_data["papers_0_code_count"],
            "task": api_data["papers_0_task"]
        },
        {
            "title": api_data["papers_1_title"],
            "authors": api_data["papers_1_authors"],
            "url": api_data["papers_1_url"],
            "code_count": api_data["papers_1_code_count"],
            "task": api_data["papers_1_task"]
        }
    ]

    # Construct final result matching output schema
    result = {
        "title": api_data["title"],
        "event": api_data["event"],
        "year": api_data["year"],
        "paper_count": api_data["paper_count"],
        "start_date": api_data["start_date"],
        "end_date": api_data["end_date"],
        "location": api_data["location"],
        "url": api_data["url"],
        "papers": papers,
        "has_next": api_data["has_next"],
        "has_previous": api_data["has_previous"],
        "next_proceeding_id": api_data["next_proceeding_id"],
        "previous_proceeding_id": api_data["previous_proceeding_id"]
    }

    return result