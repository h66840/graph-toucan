from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - success (bool): Indicates whether the search was successful
        - total_results (int): Total number of results returned by the search
        - result_0_pubmed_id (str): PubMed ID of the first result
        - result_0_link (str): Link to the first result
        - result_0_title (str): Title of the first result
        - result_0_author_0 (str): First author of the first result
        - result_0_author_1 (str): Second author of the first result
        - result_0_source (str): Source journal of the first result
        - result_0_volume (str): Volume of the first result
        - result_0_issue (str): Issue of the first result
        - result_0_pages (str): Page range of the first result
        - result_0_doi (str): DOI of the first result
        - result_0_pubdate (str): Publication date of the first result
        - result_0_abstract (str): Abstract of the first result
        - result_1_pubmed_id (str): PubMed ID of the second result
        - result_1_link (str): Link to the second result
        - result_1_title (str): Title of the second result
        - result_1_author_0 (str): First author of the second result
        - result_1_author_1 (str): Second author of the second result
        - result_1_source (str): Source journal of the second result
        - result_1_volume (str): Volume of the second result
        - result_1_issue (str): Issue of the second result
        - result_1_pages (str): Page range of the second result
        - result_1_doi (str): DOI of the second result
        - result_1_pubdate (str): Publication date of the second result
        - result_1_abstract (str): Abstract of the second result
    """
    return {
        "success": True,
        "total_results": 2,
        "result_0_pubmed_id": "12345678",
        "result_0_link": "https://pubmed.ncbi.nlm.nih.gov/12345678",
        "result_0_title": "A Study on Artificial Intelligence in Healthcare",
        "result_0_author_0": "Smith AB",
        "result_0_author_1": "Johnson CD",
        "result_0_source": "Journal of Medical AI",
        "result_0_volume": "15",
        "result_0_issue": "3",
        "result_0_pages": "100-115",
        "result_0_doi": "10.1234/jmai.2023.12345",
        "result_0_pubdate": "2023 Mar",
        "result_0_abstract": "This study explores the use of artificial intelligence in modern healthcare systems, focusing on diagnostic accuracy and patient outcomes.",
        "result_1_pubmed_id": "87654321",
        "result_1_link": "https://pubmed.ncbi.nlm.nih.gov/87654321",
        "result_1_title": "Machine Learning Approaches for Disease Prediction",
        "result_1_author_0": "Williams EF",
        "result_1_author_1": "Brown GH",
        "result_1_source": "AI in Medicine Review",
        "result_1_volume": "8",
        "result_1_issue": "2",
        "result_1_pages": "45-60",
        "result_1_doi": "10.5678/aimr.2023.87654",
        "result_1_pubdate": "2023 Feb",
        "result_1_abstract": "We present novel machine learning models for early detection of chronic diseases using electronic health records.",
    }

def pubmedsearch_search_pubmed(
    title_abstract_keywords: Optional[List[str]] = None,
    authors: Optional[List[str]] = None,
    num_results: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the PubMed database using specified keywords and/or author names.
    
    This function allows users to search the PubMed database by providing keywords
    for titles or abstracts and/or author names. It returns a specified number of
    results in a formatted dictionary.
    
    Parameters:
        title_abstract_keywords (List[str], optional): Keywords to search for in the title or abstract.
        authors (List[str], optional): Author names to include in the search. Format: surname followed by initials, e.g., "Doe JP".
        num_results (int, optional): Maximum number of results to return. Default is 10.
    
    Returns:
        Dict[str, Any]: A dictionary containing the success status, a list of results with publication details,
                        and the total number of results found.
                        - success (bool): Indicates whether the search was successful
                        - results (List[Dict]): List of publication records with fields:
                            'pubmed_id', 'link', 'title', 'authors' (List[str]), 'source', 'volume', 'issue',
                            'pages', 'doi', 'pubdate', 'abstract'
                        - total_results (int): Total number of results returned by the search
    """
    # Input validation
    if num_results is None:
        num_results = 10
    if num_results <= 0:
        return {
            "success": False,
            "results": [],
            "total_results": 0
        }
    
    # Call external API (simulated)
    api_data = call_external_api("pubmedsearch-search_pubmed")
    
    if not api_data.get("success", False):
        return {
            "success": False,
            "results": [],
            "total_results": 0
        }
    
    # Construct results list from flattened API data
    results = []
    max_items = min(num_results, 2)  # Only 2 simulated results available
    
    for i in range(max_items):
        result_key_prefix = f"result_{i}"
        if f"{result_key_prefix}_pubmed_id" not in api_data:
            continue
            
        # Collect authors for this result
        authors_list = []
        author_idx = 0
        while f"{result_key_prefix}_author_{author_idx}" in api_data:
            authors_list.append(api_data[f"{result_key_prefix}_author_{author_idx}"])
            author_idx += 1
        
        result = {
            "pubmed_id": api_data[f"{result_key_prefix}_pubmed_id"],
            "link": api_data[f"{result_key_prefix}_link"],
            "title": api_data[f"{result_key_prefix}_title"],
            "authors": authors_list,
            "source": api_data[f"{result_key_prefix}_source"],
            "volume": api_data[f"{result_key_prefix}_volume"],
            "issue": api_data[f"{result_key_prefix}_issue"],
            "pages": api_data[f"{result_key_prefix}_pages"],
            "doi": api_data[f"{result_key_prefix}_doi"],
            "pubdate": api_data[f"{result_key_prefix}_pubdate"],
            "abstract": api_data[f"{result_key_prefix}_abstract"]
        }
        results.append(result)
    
    total_results = min(api_data.get("total_results", 0), num_results)
    
    return {
        "success": True,
        "results": results,
        "total_results": total_results
    }