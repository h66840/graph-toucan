from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed keyword search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_PMID (str): PMID of the first publication
        - result_0_Title (str): Title of the first publication
        - result_0_Authors (str): Authors of the first publication (semicolon-separated)
        - result_0_Journal (str): Journal name of the first publication
        - result_0_Publication_Date (str): Publication date of the first publication (YYYY-MM-DD)
        - result_0_Abstract (str): Abstract of the first publication
        - result_1_PMID (str): PMID of the second publication
        - result_1_Title (str): Title of the second publication
        - result_1_Authors (str): Authors of the second publication (semicolon-separated)
        - result_1_Journal (str): Journal name of the second publication
        - result_1_Publication_Date (str): Publication date of the second publication (YYYY-MM-DD)
        - result_1_Abstract (str): Abstract of the second publication
    """
    return {
        "result_0_PMID": "12345678",
        "result_0_Title": "Effects of Exercise on Mental Health: A Comprehensive Review",
        "result_0_Authors": "Smith J; Johnson M; Lee A",
        "result_0_Journal": "Journal of Health Sciences",
        "result_0_Publication_Date": "2023-05-15",
        "result_0_Abstract": "This study examines the impact of regular physical activity on mental well-being, showing significant improvements in anxiety and depression symptoms.",
        
        "result_1_PMID": "87654321",
        "result_1_Title": "Nutritional Interventions in Chronic Disease Management",
        "result_1_Authors": "Brown K; Davis R; Wilson T",
        "result_1_Journal": "International Journal of Clinical Nutrition",
        "result_1_Publication_Date": "2022-11-23",
        "result_1_Abstract": "We review current evidence on dietary approaches for managing type 2 diabetes and cardiovascular diseases, highlighting key benefits of Mediterranean diet patterns."
    }

def pubmed_mcp_server_search_pubmed_key_words(key_words: str, num_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    Searches PubMed using provided keywords and returns a list of publication records.
    
    Args:
        key_words (str): Keywords to search in PubMed. Must be a non-empty string.
        num_results (Optional[int]): Number of results to return (maximum 10). Defaults to 10.
    
    Returns:
        Dict[str, Any]: Dictionary containing a 'results' key with a list of publication records.
                       Each record is a dict with keys: 'PMID', 'Title', 'Authors', 'Journal',
                       'Publication Date', and 'Abstract'.
    
    Raises:
        ValueError: If key_words is empty or None.
        TypeError: If key_words is not a string or num_results is not an integer.
    """
    if key_words is None or not isinstance(key_words, str) or not key_words.strip():
        raise ValueError("key_words must be a non-empty string.")
    
    if num_results is not None and (not isinstance(num_results, int) or num_results <= 0):
        raise ValueError("num_results must be a positive integer.")
    
    # Limit maximum results to avoid excessive data
    effective_num_results = min(num_results or 10, 10)
    
    # Fetch simulated external data
    api_data = call_external_api("pubmed-mcp-server-search_pubmed_key_words")
    
    # Construct results list from flat API data
    results: List[Dict[str, Any]] = []
    
    for i in range(min(effective_num_results, 2)):  # Only 2 simulated results available
        result = {
            "PMID": api_data.get(f"result_{i}_PMID", ""),
            "Title": api_data.get(f"result_{i}_Title", ""),
            "Authors": api_data.get(f"result_{i}_Authors", ""),
            "Journal": api_data.get(f"result_{i}_Journal", ""),
            "Publication Date": api_data.get(f"result_{i}_Publication_Date", ""),
            "Abstract": api_data.get(f"result_{i}_Abstract", "")
        }
        results.append(result)
    
    return {"results": results}