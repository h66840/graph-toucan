from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for article details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - pmid (str): PubMed ID of the article
        - pmcid (str): PubMed Central ID if available
        - date (str): publication date in ISO format (YYYY-MM-DDTHH:MM:SSZ)
        - journal (str): name of the journal where the article was published
        - title (str): full title of the article
        - abstract (str): abstract text of the article
        - full_text (str): full text content of the article when available
        - pubmed_url (str): URL linking to the article on PubMed
        - pmc_url (str): URL linking to the article on PubMed Central
        - author_0 (str): First author name
        - author_1 (str): Second author name
    """
    return {
        "pmid": "34397683",
        "pmcid": "PMC8455555",
        "date": "2021-08-20T00:00:00Z",
        "journal": "Nature Genetics",
        "title": "Genome-wide association study identifies new loci associated with psoriasis susceptibility",
        "abstract": "Psoriasis is a chronic inflammatory skin disease affecting approximately 2% of the population. We conducted a genome-wide association study to identify new genetic variants associated with psoriasis risk. Our analysis revealed several novel susceptibility loci, including variants near IL23R and TNFAIP3.",
        "full_text": "This is a simulated full text of the article discussing genetic associations with psoriasis. The study included over 10,000 participants and used advanced sequencing techniques to identify risk variants. Results were validated in independent cohorts and showed strong reproducibility.",
        "pubmed_url": "https://pubmed.ncbi.nlm.nih.gov/34397683",
        "pmc_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8455555",
        "author_0": "Smith J",
        "author_1": "Johnson A"
    }

def biomcp_article_details(call_benefit: str, pmid: str) -> Dict[str, Any]:
    """
    Retrieves details for a single PubMed article given its PubMed ID (PMID).
    
    This function simulates calling an external API to fetch article metadata,
    including title, abstract, full text (if available), authors, and publication details.
    
    Parameters:
        call_benefit (str): Define and summarize why this function is being called and the intended benefit
        pmid (str): A single PubMed ID (e.g., 34397683)
    
    Returns:
        Dict containing the following keys:
            - pmid (str): PubMed ID of the article
            - pmcid (str): PubMed Central ID if available
            - date (str): publication date in ISO format (YYYY-MM-DDTHH:MM:SSZ)
            - journal (str): name of the journal where the article was published
            - title (str): full title of the article
            - abstract (str): abstract text of the article
            - full_text (str): full text content of the article when available
            - pubmed_url (str): URL linking to the article on PubMed
            - pmc_url (str): URL linking to the article on PubMed Central
            - authors (List[str]): list of author names as strings
    """
    # Input validation
    if not call_benefit.strip():
        raise ValueError("Parameter 'call_benefit' is required and cannot be empty.")
    if not pmid.strip():
        raise ValueError("Parameter 'pmid' is required and cannot be empty.")
    
    # Call external API (simulated)
    api_data = call_external_api("biomcp-article_details")
    
    # Construct output structure matching schema
    result = {
        "pmid": api_data["pmid"],
        "pmcid": api_data["pmcid"],
        "date": api_data["date"],
        "journal": api_data["journal"],
        "title": api_data["title"],
        "abstract": api_data["abstract"],
        "full_text": api_data["full_text"],
        "pubmed_url": api_data["pubmed_url"],
        "pmc_url": api_data["pmc_url"],
        "authors": [
            api_data["author_0"],
            api_data["author_1"]
        ]
    }
    
    return result