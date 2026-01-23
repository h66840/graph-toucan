from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for bioRxiv advanced search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first preprint result
        - result_0_abstract (str): Abstract of the first preprint
        - result_0_authors (str): Authors of the first preprint (comma-separated)
        - result_0_date (str): Publication date of the first preprint (YYYY-MM-DD)
        - result_0_doi (str): DOI of the first preprint
        - result_0_url (str): URL of the first preprint
        - result_0_category (str): Category of the first preprint
        - result_1_title (str): Title of the second preprint result
        - result_1_abstract (str): Abstract of the second preprint
        - result_1_authors (str): Authors of the second preprint (comma-separated)
        - result_1_date (str): Publication date of the second preprint (YYYY-MM-DD)
        - result_1_doi (str): DOI of the second preprint
        - result_1_url (str): URL of the second preprint
        - result_1_category (str): Category of the second preprint
        - total_count (int): Total number of results available for the query
        - query_used (str): The search term or combination of terms used in the query
        - execution_error (str): Description of any validation or execution error; empty if none
    """
    return {
        "result_0_title": "Genetic Basis of Neurodevelopmental Disorders",
        "result_0_abstract": "This study investigates the genetic underpinnings of neurodevelopmental disorders using whole-genome sequencing in a large cohort.",
        "result_0_authors": "Smith J, Johnson A, Lee M",
        "result_0_date": "2023-10-15",
        "result_0_doi": "10.1101/2023.10.15.562341",
        "result_0_url": "https://www.biorxiv.org/content/10.1101/2023.10.15.562341",
        "result_0_category": "Genetics",
        "result_1_title": "CRISPR-Based Therapeutic Approaches in Cancer Models",
        "result_1_abstract": "We evaluate the efficacy of CRISPR-Cas9 gene editing in preclinical cancer models, focusing on tumor suppression and immune response.",
        "result_1_authors": "Wang L, Patel R, Garcia S",
        "result_1_date": "2023-09-28",
        "result_1_doi": "10.1101/2023.09.28.559876",
        "result_1_url": "https://www.biorxiv.org/content/10.1101/2023.09.28.559876",
        "result_1_category": "Cancer Biology",
        "total_count": 2,
        "query_used": "cancer genetics",
        "execution_error": "",
    }


def biorxiv_mcp_server_search_biorxiv_advanced(
    abstract_title: Optional[str] = None,
    author1: Optional[str] = None,
    author2: Optional[str] = None,
    end_date: Optional[str] = None,
    num_results: Optional[int] = None,
    section: Optional[str] = None,
    start_date: Optional[str] = None,
    term: Optional[str] = None,
    text_abstract_title: Optional[str] = None,
    title: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Perform an advanced search on bioRxiv preprints using specified criteria.

    Args:
        abstract_title (Optional[str]): Search term for abstract or title.
        author1 (Optional[str]): First author name.
        author2 (Optional[str]): Second author name.
        end_date (Optional[str]): End date for publication range (YYYY-MM-DD).
        num_results (Optional[int]): Number of results to return.
        section (Optional[str]): Section/category of preprints (e.g., Genetics, Neuroscience).
        start_date (Optional[str]): Start date for publication range (YYYY-MM-DD).
        term (Optional[str]): General search term.
        text_abstract_title (Optional[str]): Text to search in abstract or title.
        title (Optional[str]): Exact or partial title to search.

    Returns:
        Dict containing:
        - results (List[Dict]): List of preprint papers with fields: title, abstract, authors, date, doi, url, category.
        - total_count (int): Total number of results available.
        - query_used (str): The actual search query used.
        - execution_error (str): Error message if any occurred; empty otherwise.
    """
    try:
        # Simulate building query from inputs
        query_parts = []
        for field in [term, title, abstract_title, text_abstract_title, author1, author2, section]:
            if field:
                query_parts.append(field)
        query_used = " ".join(query_parts) if query_parts else "all preprints"

        # Call external API (simulated)
        api_data = call_external_api("biorxiv-mcp-server-search_biorxiv_advanced")

        # Construct results list from flattened API response
        results = [
            {
                "title": api_data["result_0_title"],
                "abstract": api_data["result_0_abstract"],
                "authors": api_data["result_0_authors"].split(", "),
                "date": api_data["result_0_date"],
                "doi": api_data["result_0_doi"],
                "url": api_data["result_0_url"],
                "category": api_data["result_0_category"],
            },
            {
                "title": api_data["result_1_title"],
                "abstract": api_data["result_1_abstract"],
                "authors": api_data["result_1_authors"].split(", "),
                "date": api_data["result_1_date"],
                "doi": api_data["result_1_doi"],
                "url": api_data["result_1_url"],
                "category": api_data["result_1_category"],
            },
        ]

        # Apply num_results limit if specified
        if num_results is not None and num_results > 0:
            results = results[:num_results]

        # Return final structured response
        return {
            "results": results,
            "total_count": api_data["total_count"],
            "query_used": api_data["query_used"],
            "execution_error": api_data["execution_error"] or "",
        }

    except Exception as e:
        return {
            "results": [],
            "total_count": 0,
            "query_used": "",
            "execution_error": str(e),
        }