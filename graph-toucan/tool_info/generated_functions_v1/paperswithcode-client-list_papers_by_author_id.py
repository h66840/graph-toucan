from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external PapersWithCode API for author papers.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_id (str): ID of the first paper
        - paper_0_title (str): Title of the first paper
        - paper_0_abstract (str): Abstract of the first paper
        - paper_0_published_date (str): Publication date of the first paper (ISO format)
        - paper_0_pdf_url (str): URL to the PDF of the first paper
        - paper_0_repository_url (str): URL to the code repository of the first paper
        - paper_0_citation_count (int): Citation count of the first paper
        - paper_0_authors (str): Comma-separated list of authors for the first paper
        - paper_1_id (str): ID of the second paper
        - paper_1_title (str): Title of the second paper
        - paper_1_abstract (str): Abstract of the second paper
        - paper_1_published_date (str): Publication date of the second paper (ISO format)
        - paper_1_pdf_url (str): URL to the PDF of the second paper
        - paper_1_repository_url (str): URL to the code repository of the second paper
        - paper_1_citation_count (int): Citation count of the second paper
        - paper_1_authors (str): Comma-separated list of authors for the second paper
        - total_count (int): Total number of papers for the author
        - page (int): Current page number
        - items_per_page (int): Number of items per page
        - has_next_page (bool): Whether a next page exists
        - has_previous_page (bool): Whether a previous page exists
        - author_info_name (str): Author's full name
        - author_info_affiliation (str): Author's current affiliation
        - author_info_orcid (str): Author's ORCID identifier
        - author_info_homepage (str): Author's personal homepage URL
    """
    return {
        "paper_0_id": "p12345",
        "paper_0_title": "Attention Is All You Need",
        "paper_0_abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder...",
        "paper_0_published_date": "2017-06-12T00:00:00Z",
        "paper_0_pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
        "paper_0_repository_url": "https://github.com/tensorflow/tensor2tensor",
        "paper_0_citation_count": 45000,
        "paper_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin",
        
        "paper_1_id": "p67890",
        "paper_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "paper_1_abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers...",
        "paper_1_published_date": "2018-10-11T00:00:00Z",
        "paper_1_pdf_url": "https://arxiv.org/pdf/1810.04805.pdf",
        "paper_1_repository_url": "https://github.com/google-research/bert",
        "paper_1_citation_count": 38000,
        "paper_1_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        
        "total_count": 15,
        "page": 1,
        "items_per_page": 2,
        "has_next_page": True,
        "has_previous_page": False,
        "author_info_name": "Ashish Vaswani",
        "author_info_affiliation": "Research Scientist, Google Brain",
        "author_info_orcid": "0000-0002-1825-0097",
        "author_info_homepage": "https://ashishvaswani.com"
    }

def paperswithcode_client_list_papers_by_author_id(
    author_id: str,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None
) -> Dict[str, Any]:
    """
    List the papers for a given author ID in PapersWithCode.

    Args:
        author_id (str): The unique identifier for the author in PapersWithCode.
        items_per_page (Optional[int]): Number of papers to return per page. Defaults to 2.
        page (Optional[int]): Page number to retrieve. Defaults to 1.

    Returns:
        Dict containing:
        - papers (List[Dict]): List of paper objects with details such as title, authors, publication information, abstract, and associated links.
        - total_count (int): Total number of papers available for the author.
        - page (int): Current page number.
        - items_per_page (int): Number of papers returned per page.
        - has_next_page (bool): Whether there is a next page of results.
        - has_previous_page (bool): Whether there is a previous page of results.
        - author_info (Dict): Summary information about the author including name, affiliation, and profile identifiers.

    Raises:
        ValueError: If author_id is empty or None.
    """
    if not author_id or not author_id.strip():
        raise ValueError("author_id is required and cannot be empty")

    # Use defaults if parameters not provided
    effective_items_per_page = items_per_page if items_per_page is not None else 2
    effective_page = page if page is not None else 1

    if effective_items_per_page < 1:
        raise ValueError("items_per_page must be at least 1")
    if effective_page < 1:
        raise ValueError("page must be at least 1")

    # Call external API to get flattened data
    api_data = call_external_api("paperswithcode-client-list_papers_by_author_id")

    # Construct papers list from indexed fields
    papers = [
        {
            "id": api_data["paper_0_id"],
            "title": api_data["paper_0_title"],
            "abstract": api_data["paper_0_abstract"],
            "published_date": api_data["paper_0_published_date"],
            "pdf_url": api_data["paper_0_pdf_url"],
            "repository_url": api_data["paper_0_repository_url"],
            "citation_count": api_data["paper_0_citation_count"],
            "authors": api_data["paper_0_authors"]
        },
        {
            "id": api_data["paper_1_id"],
            "title": api_data["paper_1_title"],
            "abstract": api_data["paper_1_abstract"],
            "published_date": api_data["paper_1_published_date"],
            "pdf_url": api_data["paper_1_pdf_url"],
            "repository_url": api_data["paper_1_repository_url"],
            "citation_count": api_data["paper_1_citation_count"],
            "authors": api_data["paper_1_authors"]
        }
    ]

    # Construct author info
    author_info = {
        "name": api_data["author_info_name"],
        "affiliation": api_data["author_info_affiliation"],
        "orcid": api_data["author_info_orcid"],
        "homepage": api_data["author_info_homepage"]
    }

    # Build final result structure
    result = {
        "papers": papers,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "items_per_page": api_data["items_per_page"],
        "has_next_page": api_data["has_next_page"],
        "has_previous_page": api_data["has_previous_page"],
        "author_info": author_info
    }

    return result