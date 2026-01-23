from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PapersWithCode paper search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_id (str): ID of the first paper result
        - result_0_title (str): Title of the first paper
        - result_0_abstract (str): Abstract of the first paper
        - result_0_arxiv_id (str): ArXiv ID of the first paper
        - result_0_url_pdf (str): PDF URL of the first paper
        - result_0_date_published (str): Publication date of the first paper (ISO format)
        - result_1_id (str): ID of the second paper result
        - result_1_title (str): Title of the second paper
        - result_1_abstract (str): Abstract of the second paper
        - result_1_arxiv_id (str): ArXiv ID of the second paper
        - result_1_url_pdf (str): PDF URL of the second paper
        - result_1_date_published (str): Publication date of the second paper (ISO format)
        - count (int): Total number of results available
        - next_page (str): URL to next page of results, or empty string if none
        - previous_page (str): URL to previous page of results, or empty string if none
    """
    return {
        "result_0_id": "paper-12345",
        "result_0_title": "Attention Is All You Need",
        "result_0_abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms.",
        "result_0_arxiv_id": "1706.03762",
        "result_0_url_pdf": "https://arxiv.org/pdf/1706.03762.pdf",
        "result_0_date_published": "2017-06-12T00:00:00Z",
        "result_1_id": "paper-67890",
        "result_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "result_1_abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers.",
        "result_1_arxiv_id": "1810.04805",
        "result_1_url_pdf": "https://arxiv.org/pdf/1810.04805.pdf",
        "result_1_date_published": "2018-10-11T00:00:00Z",
        "count": 2,
        "next_page": "",
        "previous_page": ""
    }

def paperswithcode_client_search_papers(
    abstract: Optional[str] = None,
    arxiv_id: Optional[str] = None,
    items_per_page: Optional[int] = None,
    page: Optional[int] = None,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for a paper in PapersWithCode.
    
    Args:
        abstract (Optional[str]): Filter by paper abstract content.
        arxiv_id (Optional[str]): Filter by ArXiv ID.
        items_per_page (Optional[int]): Number of items to return per page.
        page (Optional[int]): Page number to retrieve.
        title (Optional[str]): Filter by paper title.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of paper objects with metadata including 'id', 'title', 'abstract', 
          'arxiv_id', 'url_pdf', 'date_published', and other fields.
        - count (int): Total number of results available for the query.
        - next_page (str): URL to fetch the next page of results, or None if on last page.
        - previous_page (str): URL to fetch the previous page of results, or None if on first page.
    
    Example:
        >>> paperswithcode_client_search_papers(title="attention")
        {
            'results': [
                {
                    'id': 'paper-12345',
                    'title': 'Attention Is All You Need',
                    'abstract': 'The dominant sequence transduction models...',
                    'arxiv_id': '1706.03762',
                    'url_pdf': 'https://arxiv.org/pdf/1706.03762.pdf',
                    'date_published': '2017-06-12T00:00:00Z'
                },
                ...
            ],
            'count': 2,
            'next_page': None,
            'previous_page': None
        }
    """
    # Validate inputs
    if items_per_page is not None and (not isinstance(items_per_page, int) or items_per_page <= 0):
        raise ValueError("items_per_page must be a positive integer")
    
    if page is not None and (not isinstance(page, int) or page <= 0):
        raise ValueError("page must be a positive integer")
    
    # Call external API (simulated)
    api_data = call_external_api("paperswithcode-client-search_papers")
    
    # Construct results list from flattened API response
    results = []
    
    # Process first result if present
    if "result_0_id" in api_data and api_data["result_0_id"]:
        results.append({
            "id": api_data["result_0_id"],
            "title": api_data["result_0_title"],
            "abstract": api_data["result_0_abstract"],
            "arxiv_id": api_data["result_0_arxiv_id"],
            "url_pdf": api_data["result_0_url_pdf"],
            "date_published": api_data["result_0_date_published"]
        })
    
    # Process second result if present
    if "result_1_id" in api_data and api_data["result_1_id"]:
        results.append({
            "id": api_data["result_1_id"],
            "title": api_data["result_1_title"],
            "abstract": api_data["result_1_abstract"],
            "arxiv_id": api_data["result_1_arxiv_id"],
            "url_pdf": api_data["result_1_url_pdf"],
            "date_published": api_data["result_1_date_published"]
        })
    
    # Apply filtering based on input parameters
    filtered_results = []
    for paper in results:
        # Filter by title if specified
        if title and title.lower() not in paper["title"].lower():
            continue
        # Filter by abstract if specified
        if abstract and abstract.lower() not in paper["abstract"].lower():
            continue
        # Filter by arxiv_id if specified
        if arxiv_id and arxiv_id != paper["arxiv_id"]:
            continue
        filtered_results.append(paper)
    
    # Apply pagination
    total_count = len(filtered_results)
    start_idx = 0
    end_idx = total_count
    
    if items_per_page is not None and page is not None:
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        filtered_results = filtered_results[start_idx:end_idx]
    elif items_per_page is not None:
        end_idx = items_per_page
        filtered_results = filtered_results[:end_idx]
    elif page is not None:
        items_per_page = 10  # default
        start_idx = (page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        filtered_results = filtered_results[start_idx:end_idx]
    
    # Determine next and previous page URLs
    next_page_url = None
    prev_page_url = None
    
    if end_idx < total_count:
        next_page_url = f"?page={page + 1 if page else 2}&items_per_page={items_per_page or 10}"
    
    if start_idx > 0:
        prev_page_url = f"?page={page - 1 if page and page > 1 else 1}&items_per_page={items_per_page or 10}"
    
    # Convert empty strings to None for next/previous page
    next_page = api_data["next_page"] if api_data["next_page"] else None
    previous_page = api_data["previous_page"] if api_data["previous_page"] else None
    
    # Use generated pagination if API didn't provide it
    if next_page is None:
        next_page = next_page_url
    if previous_page is None:
        previous_page = prev_page_url
    
    return {
        "results": filtered_results,
        "count": total_count,
        "next_page": next_page,
        "previous_page": previous_page
    }