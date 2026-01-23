from typing import Dict, List, Any, Optional
import random
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external PapersWithCode API for author papers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first paper
        - paper_0_abstract (str): Abstract of the first paper
        - paper_0_authors_0_name (str): First author name of first paper
        - paper_0_authors_1_name (str): Second author name of first paper
        - paper_0_published_date (str): Publication date of first paper
        - paper_0_pdf_url (str): PDF URL of first paper
        - paper_0_pwc_url (str): PapersWithCode page URL of first paper
        - paper_1_title (str): Title of the second paper
        - paper_1_abstract (str): Abstract of the second paper
        - paper_1_authors_0_name (str): First author name of second paper
        - paper_1_authors_1_name (str): Second author name of second paper
        - paper_1_published_date (str): Publication date of second paper
        - paper_1_pdf_url (str): PDF URL of second paper
        - paper_1_pwc_url (str): PapersWithCode page URL of second paper
        - total_count (int): Total number of papers found
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether next page exists
        - has_previous_page (bool): Whether previous page exists
        - author_match_count (int): Estimated number of distinct authors with this name
        - query_metadata_matched_name (str): The exact author name matched
        - query_metadata_disambiguation_warning (bool): Whether name is ambiguous
        - query_metadata_fetch_timestamp (str): ISO timestamp of data fetch
    """
    return {
        "paper_0_title": "Attention Is All You Need",
        "paper_0_abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder...",
        "paper_0_authors_0_name": "Ashish Vaswani",
        "paper_0_authors_1_name": "Noam Shazeer",
        "paper_0_published_date": "2017-06-12",
        "paper_0_pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
        "paper_0_pwc_url": "https://paperswithcode.com/paper/attention-is-all-you-need",
        "paper_1_title": "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context",
        "paper_1_abstract": "Transformers have been shown to be superior to RNNs for language modeling tasks, but suffer from context fragmentation due to fixed-length context...",
        "paper_1_authors_0_name": "Ashish Vaswani",
        "paper_1_authors_1_name": "Zihang Dai",
        "paper_1_published_date": "2019-01-15",
        "paper_1_pdf_url": "https://arxiv.org/pdf/1901.02860.pdf",
        "paper_1_pwc_url": "https://paperswithcode.com/paper/transformer-xl-attentive-language-models",
        "total_count": 15,
        "page": 1,
        "items_per_page": 10,
        "has_next_page": True,
        "has_previous_page": False,
        "author_match_count": 1,
        "query_metadata_matched_name": "Ashish Vaswani",
        "query_metadata_disambiguation_warning": False,
        "query_metadata_fetch_timestamp": datetime.utcnow().isoformat() + "Z"
    }


def paperswithcode_client_list_papers_by_author_name(
    author_name: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the papers written by a given author name in PapersWithCode.

    Args:
        author_name (str): The name of the author to search for.
        items_per_page (Optional[int]): Number of papers to return per page. Defaults to 10 if not provided.
        page (Optional[int]): Page number for pagination. Defaults to 1 if not provided.

    Returns:
        Dict containing:
        - papers (List[Dict]): List of paper objects with title, authors, abstract, publication info, and links.
        - total_count (int): Total number of papers found for the author.
        - page (int): Current page number.
        - items_per_page (int): Number of papers per page.
        - has_next_page (bool): Whether a next page exists.
        - has_previous_page (bool): Whether a previous page exists.
        - author_match_count (int): Estimated number of distinct authors matching the name.
        - query_metadata (Dict): Additional metadata about the search including matched name, disambiguation warning, and fetch timestamp.

    Raises:
        ValueError: If author_name is empty or invalid.
    """
    if not author_name or not author_name.strip():
        raise ValueError("author_name is required and cannot be empty")

    # Validate and set defaults
    if items_per_page is None:
        items_per_page = 10
    elif items_per_page < 1 or items_per_page > 100:
        raise ValueError("items_per_page must be between 1 and 100")

    if page is None:
        page = 1
    elif page < 1:
        raise ValueError("page must be a positive integer")

    # Call external API (simulated)
    api_data = call_external_api("paperswithcode-client-list_papers_by_author_name")

    # Construct papers list from flattened API response
    papers = [
        {
            "title": api_data["paper_0_title"],
            "authors": [
                {"name": api_data["paper_0_authors_0_name"]},
                {"name": api_data["paper_0_authors_1_name"]}
            ],
            "abstract": api_data["paper_0_abstract"],
            "published_date": api_data["paper_0_published_date"],
            "links": {
                "pdf": api_data["paper_0_pdf_url"],
                "pwc": api_data["paper_0_pwc_url"]
            }
        },
        {
            "title": api_data["paper_1_title"],
            "authors": [
                {"name": api_data["paper_1_authors_0_name"]},
                {"name": api_data["paper_1_authors_1_name"]}
            ],
            "abstract": api_data["paper_1_abstract"],
            "published_date": api_data["paper_1_published_date"],
            "links": {
                "pdf": api_data["paper_1_pdf_url"],
                "pwc": api_data["paper_1_pwc_url"]
            }
        }
    ]

    # Construct query metadata
    query_metadata = {
        "matched_name": api_data["query_metadata_matched_name"],
        "disambiguation_warning": api_data["query_metadata_disambiguation_warning"],
        "fetch_timestamp": api_data["query_metadata_fetch_timestamp"]
    }

    # Build final result structure
    result = {
        "papers": papers,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "author_match_count": api_data["author_match_count"],
        "query_metadata": query_metadata
    }

    return result