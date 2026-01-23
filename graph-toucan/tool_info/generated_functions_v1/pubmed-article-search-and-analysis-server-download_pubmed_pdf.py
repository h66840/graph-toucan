from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed PDF retrieval.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): Status of the PDF retrieval attempt
        - message (str): Descriptive message explaining the outcome
        - pmc_id (str): PMC identifier if available, otherwise empty string
        - pubmed_url (str): Direct URL to the article on PubMed or PMC
    """
    return {
        "status": "not_open_access",
        "message": "Article is not available in open access; PDF cannot be retrieved.",
        "pmc_id": "PMC1234567",
        "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/12345678"
    }

def pubmed_article_search_and_analysis_server_download_pubmed_pdf(pmid: str) -> Dict[str, Any]:
    """
    Retrieves and analyzes metadata about a PubMed article, attempting to download the PDF.
    Simulates interaction with a server to check PDF availability and returns status and metadata.
    
    Parameters:
        pmid (str): PubMed ID of the article to search and analyze.
        
    Returns:
        Dict[str, Any] with the following keys:
        - status (str): Status of the PDF retrieval attempt ('failed', 'not_open_access', etc.)
        - message (str): Descriptive message explaining the outcome or reason for failure
        - pmc_id (Optional[str]): PMC identifier if available, otherwise None
        - pubmed_url (str): Direct URL to the article on PubMed or PMC
    """
    if not pmid or not pmid.strip():
        return {
            "status": "failed",
            "message": "Invalid input: pmid is required and cannot be empty.",
            "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/"
        }
    
    # Call simulated external API
    api_data = call_external_api("pubmed-article-search-and-analysis-server-download_pubmed_pdf")
    
    # Construct result according to output schema
    result: Dict[str, Any] = {
        "status": api_data["status"],
        "message": api_data["message"],
        "pubmed_url": api_data["pubmed_url"]
    }
    
    # Include pmc_id only if present in API response (non-empty)
    pmc_id = api_data.get("pmc_id", "")
    if pmc_id and pmc_id.strip():
        result["pmc_id"] = pmc_id.strip()
    
    return result