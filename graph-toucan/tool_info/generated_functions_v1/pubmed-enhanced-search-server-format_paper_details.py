from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for PubMed article details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - pubmed_id_0 (str): PubMed ID for first article
        - link_0 (str): Direct URL to first article on PubMed
        - title_0 (str): Full title of first publication
        - author_0_0 (str): First author of first article
        - author_0_1 (str): Second author of first article
        - source_0 (str): Journal name for first article
        - volume_0 (str): Volume number for first article
        - issue_0 (str): Issue number for first article
        - pages_0 (str): Page range for first article
        - doi_0 (str): DOI for first article
        - pubdate_0 (str): Publication date for first article
        - abstract_0 (str): Abstract text for first article
        - keyword_0_0 (str): First keyword for first article
        - keyword_0_1 (str): Second keyword for first article
        - pubmed_id_1 (str): PubMed ID for second article
        - link_1 (str): Direct URL to second article on PubMed
        - title_1 (str): Full title of second publication
        - author_1_0 (str): First author of second article
        - author_1_1 (str): Second author of second article
        - source_1 (str): Journal name for second article
        - volume_1 (str): Volume number for second article
        - issue_1 (str): Issue number for second article
        - pages_1 (str): Page range for second article
        - doi_1 (str): DOI for second article
        - pubdate_1 (str): Publication date for second article
        - abstract_1 (str): Abstract text for second article
        - keyword_1_0 (str): First keyword for second article
        - keyword_1_1 (str): Second keyword for second article
    """
    return {
        "pubmed_id_0": "12345678",
        "link_0": "https://pubmed.ncbi.nlm.nih.gov/12345678",
        "title_0": "A Study on Artificial Intelligence in Healthcare Applications",
        "author_0_0": "Smith J",
        "author_0_1": "Johnson A",
        "source_0": "Journal of Medical AI",
        "volume_0": "15",
        "issue_0": "3",
        "pages_0": "123-135",
        "doi_0": "10.1234/jmai.2023.12345",
        "pubdate_0": "2023-Mar",
        "abstract_0": "INTRODUCTION: Artificial intelligence is transforming healthcare. METHODS: We analyzed...",
        "keyword_0_0": "Artificial Intelligence",
        "keyword_0_1": "Healthcare",
        "pubmed_id_1": "87654321",
        "link_1": "https://pubmed.ncbi.nlm.nih.gov/87654321",
        "title_1": "Machine Learning Approaches for Disease Prediction",
        "author_1_0": "Williams R",
        "author_1_1": "Brown T",
        "source_1": "Nature Medicine",
        "volume_1": "28",
        "issue_1": "7",
        "pages_1": "789-801",
        "doi_1": "10.1038/s41591-023-02456-w",
        "pubdate_1": "2023-Jul",
        "abstract_1": "BACKGROUND: Machine learning models show promise in early disease detection. RESULTS: Our model achieved...",
        "keyword_1_0": "Machine Learning",
        "keyword_1_1": "Disease Prediction"
    }

def pubmed_enhanced_search_server_format_paper_details(pubmed_ids: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch and format details of multiple PubMed articles.
    
    This function retrieves details for a list of PubMed IDs and formats them
    into a list of dictionaries containing article information.
    
    Parameters:
    - pubmed_ids (List[str]): A list of PubMed IDs to fetch details for.
    
    Returns:
    - List[Dict[str, Any]]: A list of dictionaries, each containing details of a PubMed article.
    """
    if not pubmed_ids or not isinstance(pubmed_ids, list):
        raise ValueError("pubmed_ids must be a non-empty list of strings")
    
    # Fetch data from external API
    api_data = call_external_api("pubmed-enhanced-search-server-format_paper_details")
    
    results = []
    
    # Process up to 2 articles (based on available simulated data)
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
        
        # Extract authors
        authors = []
        for j in range(2):  # 2 authors per article in simulation
            author_key = f"author_{i}_{j}"
            if author_key in api_data and api_data[author_key]:
                authors.append(api_data[author_key])
        
        # Extract keywords
        keywords = []
        for j in range(2):  # 2 keywords per article in simulation
            keyword_key = f"keyword_{i}_{j}"
            if keyword_key in api_data and api_data[keyword_key]:
                keywords.append(api_data[keyword_key])
        
        # Construct article dictionary
        article = {
            "pubmed_id": api_data.get(pubmed_id_key, pubmed_ids[i]),
            "link": api_data.get(link_key, f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_ids[i]}"),
            "title": api_data.get(title_key, f"Title for PMID {pubmed_ids[i]}"),
            "authors": authors if authors else [],
            "source": api_data.get(source_key, "N/A"),
            "volume": api_data.get(volume_key, "N/A"),
            "issue": api_data.get(issue_key, "N/A"),
            "pages": api_data.get(pages_key, "N/A"),
            "doi": api_data.get(doi_key, ""),
            "pubdate": api_data.get(pubdate_key, "N/A"),
            "abstract": api_data.get(abstract_key, "N/A"),
            "keywords": keywords
        }
        
        results.append(article)
    
    # If we have more pubmed_ids than simulated articles, create placeholder entries
    for i in range(2, len(pubmed_ids)):
        results.append({
            "pubmed_id": pubmed_ids[i],
            "link": f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_ids[i]}",
            "title": f"Title for PMID {pubmed_ids[i]}",
            "authors": [],
            "source": "N/A",
            "volume": "N/A",
            "issue": "N/A",
            "pages": "N/A",
            "doi": "",
            "pubdate": "N/A",
            "abstract": "N/A",
            "keywords": []
        })
    
    return results