from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed article search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_PMID (str): PMID of the first article
        - result_0_Title (str): Title of the first article
        - result_0_Authors (str): Authors of the first article (semicolon-separated)
        - result_0_Journal (str): Journal name of the first article
        - result_0_Publication_Date (str): Publication date of the first article
        - result_0_Abstract (str): Abstract of the first article
        - result_1_PMID (str): PMID of the second article
        - result_1_Title (str): Title of the second article
        - result_1_Authors (str): Authors of the second article (semicolon-separated)
        - result_1_Journal (str): Journal name of the second article
        - result_1_Publication_Date (str): Publication date of the second article
        - result_1_Abstract (str): Abstract of the second article
    """
    return {
        "result_0_PMID": "12345678",
        "result_0_Title": "Effects of Regular Exercise on Cognitive Function in Older Adults",
        "result_0_Authors": "Smith J; Johnson A; Williams L",
        "result_0_Journal": "Journal of Aging and Health",
        "result_0_Publication_Date": "2023-05-15",
        "result_0_Abstract": "This study investigates the impact of regular physical activity on cognitive performance among individuals over 65 years of age. Results indicate a significant positive correlation between aerobic exercise frequency and memory retention.",
        
        "result_1_PMID": "87654321",
        "result_1_Title": "Dietary Patterns and Cardiovascular Risk: A Meta-Analysis",
        "result_1_Authors": "Brown K; Davis M; Miller R",
        "result_1_Journal": "American Journal of Preventive Cardiology",
        "result_1_Publication_Date": "2023-04-22",
        "result_1_Abstract": "A comprehensive meta-analysis of 45 studies reveals that Mediterranean-style diets are associated with a 30% reduction in major cardiovascular events. The findings support dietary interventions as a key component of heart disease prevention."
    }

def pubmed_article_search_and_analysis_server_search_pubmed_key_words(key_words: str, num_results: Optional[int] = 10) -> Dict[str, Any]:
    """
    Searches PubMed for articles matching the given keywords and returns structured article data.
    
    Args:
        key_words (str): The search terms to query in PubMed (required)
        num_results (Optional[int]): The number of results to return (optional, default is 10)
    
    Returns:
        Dict containing a list of article records with the following fields:
        - results (List[Dict]): List of article records, each containing:
            - 'PMID' (str): PubMed ID
            - 'Title' (str): Article title
            - 'Authors' (List[str]): List of author names
            - 'Journal' (str): Journal name
            - 'Publication Date' (str): Publication date in YYYY-MM-DD format
            - 'Abstract' (str): Article abstract
    
    Raises:
        ValueError: If key_words is empty or None
        TypeError: If num_results is not None and not a positive integer
    """
    # Input validation
    if not key_words or not key_words.strip():
        raise ValueError("key_words parameter is required and cannot be empty")
    
    if num_results is not None:
        if not isinstance(num_results, int):
            raise TypeError("num_results must be an integer")
        if num_results <= 0:
            raise ValueError("num_results must be a positive integer")
    
    # Call external API to get simulated data
    api_data = call_external_api("pubmed-article-search-and-analysis-server-search_pubmed_key_words")
    
    # Construct results list from flattened API response
    results: List[Dict[str, Any]] = []
    
    # Process up to 2 results (since our simulated API returns 2 items)
    max_items = min(2, num_results or 2)
    
    for i in range(max_items):
        result_key_prefix = f"result_{i}"
        
        # Skip if data for this index doesn't exist
        if f"{result_key_prefix}_PMID" not in api_data:
            continue
            
        # Split authors string into list
        authors_str = api_data.get(f"{result_key_prefix}_Authors", "")
        authors_list = [author.strip() for author in authors_str.split(";")] if authors_str else []
        
        article = {
            "PMID": api_data[f"{result_key_prefix}_PMID"],
            "Title": api_data[f"{result_key_prefix}_Title"],
            "Authors": authors_list,
            "Journal": api_data[f"{result_key_prefix}_Journal"],
            "Publication Date": api_data[f"{result_key_prefix}_Publication_Date"],
            "Abstract": api_data[f"{result_key_prefix}_Abstract"]
        }
        results.append(article)
    
    return {"results": results}