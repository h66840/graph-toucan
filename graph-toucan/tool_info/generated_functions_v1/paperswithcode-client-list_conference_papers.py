from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from PapersWithCode API for conference papers.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first paper
        - paper_0_authors (str): Comma-separated authors of the first paper
        - paper_0_abstract (str): Abstract of the first paper
        - paper_0_pdf_url (str): PDF link of the first paper
        - paper_0_id (str): ID of the first paper
        - paper_0_published_date (str): Publication date of the first paper
        - paper_1_title (str): Title of the second paper
        - paper_1_authors (str): Comma-separated authors of the second paper
        - paper_1_abstract (str): Abstract of the second paper
        - paper_1_pdf_url (str): PDF link of the second paper
        - paper_1_id (str): ID of the second paper
        - paper_1_published_date (str): Publication date of the second paper
        - total_count (int): Total number of papers available
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - conference_id (str): Conference ID
        - proceeding_id (str): Proceeding ID
        - metadata_api_version (str): API version
        - metadata_timestamp (str): Response timestamp
        - metadata_rate_limit_remaining (int): Remaining rate limit
        - metadata_rate_limit_reset (int): Rate limit reset time in seconds
    """
    return {
        "paper_0_title": "Attention Is All You Need",
        "paper_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin",
        "paper_0_abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder...",
        "paper_0_pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
        "paper_0_id": "1706.03762",
        "paper_0_published_date": "2017-06-12",
        "paper_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "paper_1_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "paper_1_abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers...",
        "paper_1_pdf_url": "https://arxiv.org/pdf/1810.04805.pdf",
        "paper_1_id": "1810.04805",
        "paper_1_published_date": "2018-10-11",
        "total_count": 150,
        "page": 1,
        "items_per_page": 2,
        "has_next_page": True,
        "has_previous_page": False,
        "conference_id": "neurips",
        "proceeding_id": "neurips-2023",
        "metadata_api_version": "v1",
        "metadata_timestamp": "2023-11-15T10:30:00Z",
        "metadata_rate_limit_remaining": 98,
        "metadata_rate_limit_reset": 3600
    }

def paperswithcode_client_list_conference_papers(
    conference_id: str,
    proceeding_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the papers for a given conference ID and proceeding ID in PapersWithCode.
    
    Args:
        conference_id (str): ID of the conference (required)
        proceeding_id (str): ID of the proceeding (required)
        items_per_page (Optional[int]): Number of papers to return per page (default: 2)
        page (Optional[int]): Page number for pagination (default: 1)
    
    Returns:
        Dict containing:
        - papers (List[Dict]): List of paper objects with title, authors, abstract, PDF link, and metadata
        - total_count (int): Total number of papers available
        - page (int): Current page number
        - items_per_page (int): Number of papers per page
        - has_next_page (bool): Whether next page exists
        - has_previous_page (bool): Whether previous page exists
        - conference_id (str): Conference ID for context
        - proceeding_id (str): Proceeding ID for context
        - metadata (Dict): Additional information about the response
    
    Raises:
        ValueError: If conference_id or proceeding_id is empty
    """
    if not conference_id:
        raise ValueError("conference_id is required")
    if not proceeding_id:
        raise ValueError("proceeding_id is required")
    
    # Use defaults if not provided
    items_per_page = items_per_page if items_per_page is not None else 2
    page = page if page is not None else 1
    
    # Call external API (simulated)
    api_data = call_external_api("paperswithcode-client-list_conference_papers")
    
    # Construct papers list from indexed fields
    papers = [
        {
            "title": api_data["paper_0_title"],
            "authors": api_data["paper_0_authors"],
            "abstract": api_data["paper_0_abstract"],
            "pdf_url": api_data["paper_0_pdf_url"],
            "id": api_data["paper_0_id"],
            "published_date": api_data["paper_0_published_date"]
        },
        {
            "title": api_data["paper_1_title"],
            "authors": api_data["paper_1_authors"],
            "abstract": api_data["paper_1_abstract"],
            "pdf_url": api_data["paper_1_pdf_url"],
            "id": api_data["paper_1_id"],
            "published_date": api_data["paper_1_published_date"]
        }
    ]
    
    # Construct metadata
    metadata = {
        "api_version": api_data["metadata_api_version"],
        "timestamp": api_data["metadata_timestamp"],
        "rate_limit_remaining": api_data["metadata_rate_limit_remaining"],
        "rate_limit_reset": api_data["metadata_rate_limit_reset"]
    }
    
    # Build final result matching output schema
    result = {
        "papers": papers,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "conference_id": api_data["conference_id"],
        "proceeding_id": api_data["proceeding_id"],
        "metadata": metadata
    }
    
    return result