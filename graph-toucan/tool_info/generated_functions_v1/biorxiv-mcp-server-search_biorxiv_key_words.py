from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BioRxiv keyword search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first preprint paper
        - result_0_authors (str): Authors of the first preprint paper
        - result_0_abstract (str): Abstract of the first preprint paper
        - result_0_doi (str): DOI of the first preprint paper
        - result_0_published_date (str): Published date of the first preprint paper
        - result_0_version (int): Version number of the first preprint paper
        - result_0_url (str): URL of the first preprint paper
        - result_1_title (str): Title of the second preprint paper
        - result_1_authors (str): Authors of the second preprint paper
        - result_1_abstract (str): Abstract of the second preprint paper
        - result_1_doi (str): DOI of the second preprint paper
        - result_1_published_date (str): Published date of the second preprint paper
        - result_1_version (int): Version number of the second preprint paper
        - result_1_url (str): URL of the second preprint paper
        - total_count (int): Total number of results returned by the search
        - query (str): The keyword query used in the search
    """
    return {
        "result_0_title": "A Study on Gene Expression in Cancer Cells",
        "result_0_authors": "John Doe, Jane Smith",
        "result_0_abstract": "This study investigates gene expression patterns in various types of cancer cells using RNA sequencing.",
        "result_0_doi": "10.1101/2023.01.01.498271",
        "result_0_published_date": "2023-01-15",
        "result_0_version": 1,
        "result_0_url": "https://www.biorxiv.org/content/10.1101/2023.01.01.498271v1",
        "result_1_title": "Neural Mechanisms of Decision Making in Primates",
        "result_1_authors": "Alice Johnson, Robert Brown",
        "result_1_abstract": "We explore the neural basis of decision-making in non-human primates through electrophysiological recordings.",
        "result_1_doi": "10.1101/2023.02.10.499123",
        "result_1_published_date": "2023-02-20",
        "result_1_version": 1,
        "result_1_url": "https://www.biorxiv.org/content/10.1101/2023.02.10.499123v1",
        "total_count": 2,
        "query": "gene expression cancer"
    }


def biorxiv_mcp_server_search_biorxiv_key_words(key_words: str, num_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    Searches BioRxiv preprint papers using specified keywords.

    Args:
        key_words (str): Keywords to search for in BioRxiv preprints (required).
        num_results (Optional[int]): Number of results to return (optional, default is 10).

    Returns:
        Dict containing:
        - results (List[Dict]): List of preprint paper records with 'title', 'authors', 'abstract',
          'doi', 'published_date', 'version', and 'url' fields.
        - total_count (int): Total number of results returned by the search.
        - query (str): The keyword query used in the search.

    Raises:
        ValueError: If key_words is empty or not a string.
    """
    if not key_words or not isinstance(key_words, str):
        raise ValueError("key_words must be a non-empty string.")

    # Call external API (simulated)
    api_data = call_external_api("biorxiv-mcp-server-search_biorxiv_key_words")

    # Construct results list from flattened API response
    results = [
        {
            "title": api_data["result_0_title"],
            "authors": api_data["result_0_authors"],
            "abstract": api_data["result_0_abstract"],
            "doi": api_data["result_0_doi"],
            "published_date": api_data["result_0_published_date"],
            "version": api_data["result_0_version"],
            "url": api_data["result_0_url"]
        },
        {
            "title": api_data["result_1_title"],
            "authors": api_data["result_1_authors"],
            "abstract": api_data["result_1_abstract"],
            "doi": api_data["result_1_doi"],
            "published_date": api_data["result_1_published_date"],
            "version": api_data["result_1_version"],
            "url": api_data["result_1_url"]
        }
    ]

    # Apply num_results limit if specified
    limited_results = results[:num_results] if num_results is not None else results

    return {
        "results": limited_results,
        "total_count": api_data["total_count"],
        "query": api_data["query"]
    }