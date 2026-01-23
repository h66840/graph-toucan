from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode conference.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - name (str): Full name of the conference
        - acronym (str): Acronym or short form of the conference
        - year (int): Year of the conference edition
        - start_date (str): Start date in ISO format (YYYY-MM-DD)
        - end_date (str): End date in ISO format (YYYY-MM-DD)
        - location (str): Geographic location of the conference
        - website (str): Official website URL
        - paper_count (int): Total number of papers
        - tracks_0 (str): First track name
        - tracks_1 (str): Second track name
        - meta_conference_id (str): ID of the overarching conference series
        - meta_conference_name (str): Name of the overarching conference series
        - meta_conference_acronym (str): Acronym of the overarching conference series
        - is_active (bool): Whether the conference is active or upcoming
        - papers_0_id (str): First paper ID
        - papers_0_title (str): First paper title
        - papers_0_authors_0 (str): First author of first paper
        - papers_0_authors_1 (str): Second author of first paper
        - papers_0_abstract (str): Abstract of first paper
        - papers_0_url_pdf (str): PDF URL of first paper
        - papers_0_url_abs (str): Abstract page URL of first paper
        - papers_0_published (str): Publication date of first paper
        - papers_1_id (str): Second paper ID
        - papers_1_title (str): Second paper title
        - papers_1_authors_0 (str): First author of second paper
        - papers_1_authors_1 (str): Second author of second paper
        - papers_1_abstract (str): Abstract of second paper
        - papers_1_url_pdf (str): PDF URL of second paper
        - papers_1_url_abs (str): Abstract page URL of second paper
        - papers_1_published (str): Publication date of second paper
    """
    return {
        "name": "International Conference on Learning Representations",
        "acronym": "ICLR",
        "year": 2023,
        "start_date": "2023-05-01",
        "end_date": "2023-05-05",
        "location": "Kigali, Rwanda",
        "website": "https://iclr.cc/Conferences/2023",
        "paper_count": 987,
        "tracks_0": "Main Conference",
        "tracks_1": "Workshops",
        "meta_conference_id": "iclr",
        "meta_conference_name": "International Conference on Learning Representations",
        "meta_conference_acronym": "ICLR",
        "is_active": False,
        "papers_0_id": "paper_12345",
        "papers_0_title": "On the Expressivity of Neural Networks",
        "papers_0_authors_0": "Alice Johnson",
        "papers_0_authors_1": "Bob Smith",
        "papers_0_abstract": "This paper explores the theoretical expressivity of deep neural networks.",
        "papers_0_url_pdf": "https://arxiv.org/pdf/2301.12345.pdf",
        "papers_0_url_abs": "https://arxiv.org/abs/2301.12345",
        "papers_0_published": "2023-01-15",
        "papers_1_id": "paper_67890",
        "papers_1_title": "Efficient Transformers for Long Sequences",
        "papers_1_authors_0": "Carol Davis",
        "papers_1_authors_1": "David Wilson",
        "papers_1_abstract": "We propose a new attention mechanism for efficient sequence modeling.",
        "papers_1_url_pdf": "https://arxiv.org/pdf/2302.67890.pdf",
        "papers_1_url_abs": "https://arxiv.org/abs/2302.67890",
        "papers_1_published": "2023-02-20",
    }

def paperswithcode_client_get_conference(conference_id: str) -> Dict[str, Any]:
    """
    Get a conference by ID from PapersWithCode.

    Args:
        conference_id (str): The ID of the conference to retrieve.

    Returns:
        Dict containing conference details with the following structure:
        - name (str): Full name of the conference
        - acronym (str): Acronym or short form
        - year (int): Year of the conference edition
        - start_date (str): Start date in ISO format
        - end_date (str): End date in ISO format
        - location (str): Geographic location
        - website (str): Official website URL
        - papers (List[Dict]): List of papers with keys: id, title, authors, abstract, url_pdf, url_abs, published
        - paper_count (int): Total number of papers
        - tracks (List[str]): List of tracks or categories
        - meta_conference (Dict): Info about the overarching series with keys: id, name, acronym
        - is_active (bool): Whether the conference is active or upcoming
    """
    if not conference_id or not isinstance(conference_id, str):
        raise ValueError("conference_id must be a non-empty string")

    api_data = call_external_api("paperswithcode-client-get_conference")

    # Construct papers list
    papers = [
        {
            "id": api_data["papers_0_id"],
            "title": api_data["papers_0_title"],
            "authors": [api_data["papers_0_authors_0"], api_data["papers_0_authors_1"]],
            "abstract": api_data["papers_0_abstract"],
            "url_pdf": api_data["papers_0_url_pdf"],
            "url_abs": api_data["papers_0_url_abs"],
            "published": api_data["papers_0_published"],
        },
        {
            "id": api_data["papers_1_id"],
            "title": api_data["papers_1_title"],
            "authors": [api_data["papers_1_authors_0"], api_data["papers_1_authors_1"]],
            "abstract": api_data["papers_1_abstract"],
            "url_pdf": api_data["papers_1_url_pdf"],
            "url_abs": api_data["papers_1_url_abs"],
            "published": api_data["papers_1_published"],
        }
    ]

    # Construct tracks list
    tracks = [api_data["tracks_0"], api_data["tracks_1"]]

    # Construct meta_conference dict
    meta_conference = {
        "id": api_data["meta_conference_id"],
        "name": api_data["meta_conference_name"],
        "acronym": api_data["meta_conference_acronym"]
    }

    # Build final result matching output schema
    result = {
        "name": api_data["name"],
        "acronym": api_data["acronym"],
        "year": api_data["year"],
        "start_date": api_data["start_date"],
        "end_date": api_data["end_date"],
        "location": api_data["location"],
        "website": api_data["website"],
        "papers": papers,
        "paper_count": api_data["paper_count"],
        "tracks": tracks,
        "meta_conference": meta_conference,
        "is_active": api_data["is_active"]
    }

    return result