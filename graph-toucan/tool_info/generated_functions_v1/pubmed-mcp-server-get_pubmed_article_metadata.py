from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching PubMed article metadata from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - PMID (str): unique identifier for the article in PubMed
        - Title (str): title of the scientific article
        - Authors (str): comma-separated list of author names
        - Journal (str): name of the journal in which the article was published
        - Publication_Date (str): year (or full date if available) when the article was published
        - Abstract (str or None): summary of the article's content; may be null if not available
    """
    return {
        "PMID": "12345678",
        "Title": "A study on the effects of climate change on marine biodiversity",
        "Authors": "Smith J, Johnson M, Lee K",
        "Journal": "Nature Climate Change",
        "Publication_Date": "2023-05-15",
        "Abstract": "This study investigates the impact of rising sea temperatures on marine species distribution across tropical regions. Using long-term observational data from 1980 to 2020, we analyzed shifts in species richness and community composition. Results indicate a significant poleward migration of warm-water species and local extinctions in equatorial zones. These findings highlight the urgent need for adaptive conservation strategies in marine ecosystems."
    }

def pubmed_mcp_server_get_pubmed_article_metadata(pmid: str) -> Dict[str, Any]:
    """
    Retrieves metadata for a PubMed article using its PMID.
    
    Args:
        pmid (str): The PubMed ID of the article to retrieve metadata for.
        
    Returns:
        Dict containing the article metadata with the following keys:
        - PMID (str): unique identifier for the article in PubMed
        - Title (str): title of the scientific article
        - Authors (str): comma-separated list of author names
        - Journal (str): name of the journal in which the article was published
        - Publication Date (str): year (or full date if available) when the article was published
        - Abstract (str or None): summary of the article's content; may be null if not available
        
    Raises:
        ValueError: If pmid is empty or invalid.
    """
    if not pmid or not pmid.strip():
        raise ValueError("pmid is required and cannot be empty")
    
    # Call the external API simulation
    api_data = call_external_api("pubmed_mcp_server_get_pubmed_article_metadata")
    
    # Construct the result dictionary matching the expected output schema
    result = {
        "PMID": api_data["PMID"],
        "Title": api_data["Title"],
        "Authors": api_data["Authors"],
        "Journal": api_data["Journal"],
        "Publication Date": api_data["Publication_Date"],
        "Abstract": api_data["Abstract"] if api_data["Abstract"] is not None else None
    }
    
    return result