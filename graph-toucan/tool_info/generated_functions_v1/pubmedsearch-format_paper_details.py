from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed article details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - pubmed_id_0 (str): PubMed ID of the first article
        - link_0 (str): Direct URL to the first article on PubMed
        - title_0 (str): Full title of the first publication
        - author_0_0 (str): First author of the first article
        - author_0_1 (str): Second author of the first article
        - source_0 (str): Journal name of the first article
        - volume_0 (str): Volume number of the first article
        - issue_0 (str): Issue number of the first article
        - pages_0 (str): Page range of the first article
        - doi_0 (str): DOI of the first article
        - pubdate_0 (str): Publication year of the first article
        - abstract_0 (str): Abstract of the first article
        - pubmed_id_1 (str): PubMed ID of the second article
        - link_1 (str): Direct URL to the second article on PubMed
        - title_1 (str): Full title of the second publication
        - author_1_0 (str): First author of the second article
        - author_1_1 (str): Second author of the second article
        - source_1 (str): Journal name of the second article
        - volume_1 (str): Volume number of the second article
        - issue_1 (str): Issue number of the second article
        - pages_1 (str): Page range of the second article
        - doi_1 (str): DOI of the second article
        - pubdate_1 (str): Publication year of the second article
        - abstract_1 (str): Abstract of the second article
    """
    return {
        "pubmed_id_0": "12345678",
        "link_0": "https://pubmed.ncbi.nlm.nih.gov/12345678",
        "title_0": "A Study on Artificial Intelligence in Healthcare",
        "author_0_0": "Smith J",
        "author_0_1": "Johnson A",
        "source_0": "Journal of Medical AI",
        "volume_0": "15",
        "issue_0": "3",
        "pages_0": "123-135",
        "doi_0": "10.1001/jama.2023.12345",
        "pubdate_0": "2023",
        "abstract_0": "This study explores the impact of artificial intelligence on modern healthcare systems, focusing on diagnostic accuracy and patient outcomes.",
        
        "pubmed_id_1": "87654321",
        "link_1": "https://pubmed.ncbi.nlm.nih.gov/87654321",
        "title_1": "Machine Learning Approaches for Genomic Analysis",
        "author_1_0": "Brown L",
        "author_1_1": "Davis M",
        "source_1": "Nature Genetics",
        "volume_1": "54",
        "issue_1": "7",
        "pages_1": "987-995",
        "doi_1": "10.1038/s41588-023-00456-7",
        "pubdate_1": "2023",
        "abstract_1": "We present novel machine learning models for identifying genetic markers associated with complex diseases using large-scale genomic datasets."
    }

def pubmedsearch_format_paper_details(pubmed_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch and format details of multiple PubMed articles.
    
    This function retrieves details for a list of PubMed IDs and formats them
    into a list of dictionaries containing article information.
    
    Parameters:
        pubmed_ids (List[str]): A list of PubMed IDs to fetch details for.
        
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing details of a PubMed article.
        Each dictionary contains:
            - pubmed_id (str): unique identifier for the PubMed article
            - link (str): direct URL to the article on PubMed
            - title (str): full title of the publication
            - authors (List[str]): list of author names in order
            - source (str): name of the journal or source where the article was published
            - volume (str): volume number of the journal issue, may be "N/A"
            - issue (str): issue number within the volume, may be "N/A"
            - pages (str): page range or article identifier, may be "N/A"
            - doi (str): Digital Object Identifier for the article
            - pubdate (str): year of publication
            - abstract (str): summary of the article's content; may be "N/A" if not available
    """
    if not pubmed_ids:
        return []
    
    # Fetch data from external API
    api_data = call_external_api("pubmedsearch-format_paper_details")
    
    results = []
    
    # Process up to 2 articles based on available data
    for i in range(min(2, len(pubmed_ids))):
        pubmed_id_key = f"pubmed_id_{i}"
        link_key = f"link_{i}"
        title_key = f"title_{i}"
        source_key = f"source_{i}"
        volume_key = f"volume_{i}"
        issue_key = f"issue_{i}"
        pages_key = f"pages_{i}"
        doi_key = f"doi_{i}"
        pubdate_key = f"pubdate_{i}"
        abstract_key = f"abstract_{i}"
        
        # Build authors list
        authors = []
        for j in range(2):  # Assume max 2 authors in mock data
            author_key = f"author_{i}_{j}"
            if author_key in api_data and api_data[author_key]:
                authors.append(api_data[author_key])
        
        # Construct article details
        article = {
            "pubmed_id": api_data.get(pubmed_id_key, "N/A"),
            "link": api_data.get(link_key, "N/A"),
            "title": api_data.get(title_key, "N/A"),
            "authors": authors,
            "source": api_data.get(source_key, "N/A"),
            "volume": api_data.get(volume_key, "N/A"),
            "issue": api_data.get(issue_key, "N/A"),
            "pages": api_data.get(pages_key, "N/A"),
            "doi": api_data.get(doi_key, "N/A"),
            "pubdate": api_data.get(pubdate_key, "N/A"),
            "abstract": api_data.get(abstract_key, "N/A")
        }
        
        results.append(article)
    
    return results