from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed article metadata.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - PMID (str): PubMed ID of the article as a string
        - Title (str): title of the article
        - Authors (str): comma-separated list of author names as a single string
        - Journal (str): name of the journal in which the article was published
        - Publication_Date (str): year (or full date if available) when the article was published
        - Abstract (str): abstract text of the article; may be "No abstract available" if none exists
    """
    return {
        "PMID": "12345678",
        "Title": "A study on the effects of sleep on cognitive performance",
        "Authors": "Smith J, Johnson A, Williams R",
        "Journal": "Journal of Cognitive Neuroscience",
        "Publication_Date": "2023",
        "Abstract": "This study investigates the impact of sleep duration on cognitive functions such as memory, attention, and decision-making. Results indicate a strong correlation between adequate sleep and improved performance."
    }

def pubmed_article_search_and_analysis_server_get_pubmed_article_metadata(pmid: str) -> Dict[str, Any]:
    """
    Retrieves metadata for a PubMed article using its PubMed ID (PMID).
    
    Args:
        pmid (str): The PubMed ID of the article to retrieve metadata for. Required.
    
    Returns:
        Dict[str, Any]: A dictionary containing the article metadata with the following keys:
            - PMID (str): PubMed ID of the article as a string
            - Title (str): title of the article
            - Authors (str): comma-separated list of author names as a single string
            - Journal (str): name of the journal in which the article was published
            - Publication Date (str): year (or full date if available) when the article was published
            - Abstract (str): abstract text of the article; may be "No abstract available" if none exists
    
    Raises:
        ValueError: If pmid is empty or not provided.
    """
    if not pmid:
        raise ValueError("Parameter 'pmid' is required and cannot be empty.")
    
    # Call the external API simulation to get flat data
    api_data = call_external_api("pubmed-article-search-and-analysis-server-get_pubmed_article_metadata")
    
    # Construct the result dictionary matching the expected output schema
    result = {
        "PMID": api_data["PMID"],
        "Title": api_data["Title"],
        "Authors": api_data["Authors"],
        "Journal": api_data["Journal"],
        "Publication Date": api_data["Publication_Date"],
        "Abstract": api_data["Abstract"]
    }
    
    return result