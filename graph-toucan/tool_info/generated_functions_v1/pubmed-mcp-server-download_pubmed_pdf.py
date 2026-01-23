from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed PDF retrieval.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - status (str): status of the PDF retrieval attempt
        - message (str): human-readable explanation of the outcome
        - pmc_link (str): direct URL to the PMC article page
        - is_open_access (bool): indicates whether the article is open access
    """
    return {
        "status": "available",
        "message": "Full text is available in PubMed Central.",
        "pmc_link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1234567/",
        "is_open_access": True
    }

def pubmed_mcp_server_download_pubmed_pdf(pmid: str) -> Dict[str, Any]:
    """
    Retrieves metadata about the availability of a PubMed Central article's PDF.

    Args:
        pmid (str): PubMed ID of the article to retrieve PDF availability for.

    Returns:
        Dict containing:
        - status (str): status of the PDF retrieval attempt ('access restricted', 'not found', 'available')
        - message (str): human-readable explanation of the outcome
        - pmc_link (str): direct URL to the PMC article page if available
        - is_open_access (bool): whether the article is fully open access
    """
    if not pmid or not pmid.strip():
        return {
            "status": "not found",
            "message": "PMID is required and cannot be empty.",
            "pmc_link": "",
            "is_open_access": False
        }

    api_data = call_external_api("pubmed-mcp-server-download_pubmed_pdf")

    return {
        "status": str(api_data["status"]),
        "message": str(api_data["message"]),
        "pmc_link": str(api_data["pmc_link"]),
        "is_open_access": bool(api_data["is_open_access"])
    }