from typing import Dict, List, Any


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed search count.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Indicates whether the query was successful
        - count_0_term (str): First search term
        - count_0_value (int): Publication count for the first search term
        - count_1_term (str): Second search term
        - count_1_value (int): Publication count for the second search term
    """
    return {
        "success": True,
        "count_0_term": "cancer",
        "count_0_value": 1500000,
        "count_1_term": "diabetes",
        "count_1_value": 1200000,
    }


def pubmed_enhanced_search_server_get_pubmed_count(search_terms: List[str]) -> Dict[str, Any]:
    """
    Get the number of PubMed results for multiple search terms.

    This function queries PubMed and returns the count of results for each provided search term.
    Useful for comparing the prevalence of different medical terms or concepts in the literature.

    Parameters:
        search_terms (List[str]): List of search terms to query in PubMed.

    Returns:
        Dict[str, Any]: A dictionary containing success status and counts for each search term.
            - success (bool): Indicates whether the PubMed query was executed successfully.
            - counts (Dict): Mapping of search terms to their respective publication counts.
    """
    if not isinstance(search_terms, list):
        return {
            "success": False,
            "counts": {}
        }

    if len(search_terms) == 0:
        return {
            "success": True,
            "counts": {}
        }

    # Call the external API to simulate PubMed query
    api_data = call_external_api("pubmed-enhanced-search-server-get_pubmed_count")

    # Initialize result structure
    success = api_data.get("success", False)
    counts = {}

    # Construct counts dictionary from flattened API response
    for i in range(2):  # Expecting up to 2 items as per implementation instructions
        term_key = f"count_{i}_term"
        value_key = f"count_{i}_value"
        if term_key in api_data and value_key in api_data:
            term = api_data[term_key]
            value = api_data[value_key]
            if isinstance(term, str) and isinstance(value, int):
                counts[term] = value

    # Ensure all requested search terms are present (simulate realistic behavior)
    for term in search_terms:
        if term not in counts:
            # Simulate a realistic count based on term length as a proxy for specificity
            counts[term] = max(1000, 100000 // (len(term) + 1))

    return {
        "success": success,
        "counts": counts
    }