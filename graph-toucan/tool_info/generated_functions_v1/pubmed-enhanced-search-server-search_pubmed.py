from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external PubMed API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the search was successful
        - total_results (int): Total number of results found
        - result_0_pmid (str): PubMed ID of first result
        - result_0_title (str): Title of first result
        - result_0_authors (str): Authors of first result (comma-separated)
        - result_0_source (str): Source journal of first result
        - result_0_pub_date (str): Publication date of first result
        - result_0_abstract (str): Abstract of first result
        - result_0_doi (str): DOI of first result
        - result_0_keywords (str): Keywords of first result (comma-separated)
        - result_1_pmid (str): PubMed ID of second result
        - result_1_title (str): Title of second result
        - result_1_authors (str): Authors of second result (comma-separated)
        - result_1_source (str): Source journal of second result
        - result_1_pub_date (str): Publication date of second result
        - result_1_abstract (str): Abstract of second result
        - result_1_doi (str): DOI of second result
        - result_1_keywords (str): Keywords of second result (comma-separated)
    """
    return {
        "success": True,
        "total_results": 25,
        "result_0_pmid": "12345678",
        "result_0_title": "A Study on the Effects of Exercise on Mental Health",
        "result_0_authors": "Smith J, Johnson A, Lee B",
        "result_0_source": "Journal of Health Psychology",
        "result_0_pub_date": "2023-05-15",
        "result_0_abstract": "This study investigates the relationship between regular physical activity and improved mental well-being in adults. Results show a significant correlation between exercise frequency and reduced anxiety levels.",
        "result_0_doi": "10.1234/jhp.2023.12345",
        "result_0_keywords": "exercise, mental health, anxiety, physical activity",
        "result_1_pmid": "12345679",
        "result_1_title": "Nutritional Interventions for Cognitive Decline in Elderly Patients",
        "result_1_authors": "Brown C, Davis R, Wilson M",
        "result_1_source": "American Journal of Clinical Nutrition",
        "result_1_pub_date": "2023-04-22",
        "result_1_abstract": "We examined the impact of dietary changes on cognitive function in individuals over 65. Findings suggest that increased intake of omega-3 fatty acids is associated with slower cognitive decline.",
        "result_1_doi": "10.1234/ajcn.2023.12346",
        "result_1_keywords": "nutrition, cognitive decline, elderly, omega-3"
    }

def pubmed_enhanced_search_server_search_pubmed(
    keywords: Optional[List[str]] = None,
    journal: Optional[str] = None,
    num_results: int = 10,
    sort_by: str = "relevance"
) -> Dict[str, Any]:
    """
    Search the PubMed database using specified keywords and optional journal name.
    
    This function allows users to search the PubMed database by providing keywords
    and an optional journal name. It returns a specified number of
    results in a formatted dictionary.
    
    Parameters:
        keywords (List[str], optional): Keywords to search for in PubMed without field restrictions.
        journal (str, optional): Journal name to limit the search to a specific journal.
        num_results (int, optional): Maximum number of results to return. Default is 10.
        sort_by (str, optional): Sort order for results. Options: "relevance", "date_desc", "date_asc". Default is "relevance".
    
    Returns:
        Dict[str, Any]: A dictionary containing:
            - success (bool): Whether the search was successful
            - results (List[Dict]): List of publication records with details like PubMed ID, title, authors, source, 
              publication date, abstract, DOI, and keywords
            - total_results (int): Total number of results found for the query
    """
    # Input validation
    if keywords is None:
        keywords = []
    
    if not isinstance(keywords, list):
        return {
            "success": False,
            "results": [],
            "total_results": 0
        }
    
    if num_results <= 0:
        num_results = 10
    
    if sort_by not in ["relevance", "date_desc", "date_asc"]:
        sort_by = "relevance"
    
    # Call external API to get data
    api_data = call_external_api("pubmed-enhanced-search-server-search_pubmed")
    
    # Construct results list from flattened API response
    results = []
    
    # Process first result if available
    if api_data.get("success", False):
        for i in range(2):  # We expect 2 results from the API mock
            pmid_key = f"result_{i}_pmid"
            if pmid_key in api_data and api_data[pmid_key]:
                result = {
                    "pmid": api_data[f"result_{i}_pmid"],
                    "title": api_data[f"result_{i}_title"],
                    "authors": api_data[f"result_{i}_authors"].split(", ") if api_data[f"result_{i}_authors"] else [],
                    "source": api_data[f"result_{i}_source"],
                    "publication_date": api_data[f"result_{i}_pub_date"],
                    "abstract": api_data[f"result_{i}_abstract"],
                    "doi": api_data[f"result_{i}_doi"],
                    "keywords": api_data[f"result_{i}_keywords"].split(", ") if api_data[f"result_{i}_keywords"] else []
                }
                results.append(result)
    
    # Limit results based on num_results parameter
    results = results[:num_results]
    
    # Return structured response
    return {
        "success": api_data.get("success", False),
        "results": results,
        "total_results": api_data.get("total_results", 0)
    }