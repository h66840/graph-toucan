from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar batch paper retrieval.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - paper_0_title (str): Title of the first retrieved paper
        - paper_0_authors (str): Authors of the first paper as a comma-separated string
        - paper_0_abstract (str): Abstract of the first paper
        - paper_0_year (int): Publication year of the first paper
        - paper_0_citation_count (int): Number of citations for the first paper
        - paper_0_reference_count (int): Number of references in the first paper
        - paper_0_doi (str): DOI of the first paper
        - paper_0_url (str): URL to the first paper
        - paper_1_title (str): Title of the second retrieved paper
        - paper_1_authors (str): Authors of the second paper as a comma-separated string
        - paper_1_abstract (str): Abstract of the second paper
        - paper_1_year (int): Publication year of the second paper
        - paper_1_citation_count (int): Number of citations for the second paper
        - paper_1_reference_count (int): Number of references in the second paper
        - paper_1_doi (str): DOI of the second paper
        - paper_1_url (str): URL to the second paper
        - not_found_0 (str): First paper ID that was not found
        - not_found_1 (str): Second paper ID that was not found
        - total_requested (int): Total number of paper IDs in the input request
        - total_retrieved (int): Number of papers successfully retrieved
        - batch_status (str): Status of batch processing ('partial_success' or 'complete_success')
        - execution_time_seconds (float): Time taken to process the batch in seconds
    """
    return {
        "paper_0_title": "Attention Is All You Need",
        "paper_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin",
        "paper_0_abstract": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
        "paper_0_year": 2017,
        "paper_0_citation_count": 45000,
        "paper_0_reference_count": 120,
        "paper_0_doi": "10.48550/arXiv.1706.03762",
        "paper_0_url": "https://www.semanticscholar.org/paper/Attention-Is-All-You-Need-Vaswani-Shazeer/0e85dc67a49a7979b05ea7b3537e2fb5c4117c4d",
        "paper_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "paper_1_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "paper_1_abstract": "We introduce a new language representation model called BERT, which stands for Bidirectional Encoder Representations from Transformers. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers.",
        "paper_1_year": 2018,
        "paper_1_citation_count": 62000,
        "paper_1_reference_count": 98,
        "paper_1_doi": "10.48550/arXiv.1810.04805",
        "paper_1_url": "https://www.semanticscholar.org/paper/BERT%3A-Pre-training-of-Deep-Bidirectional-Transformers-Devlin-Chang/df2b0e26d0599ce3e70df8a9da02e51594e12816",
        "not_found_0": "invalid-paper-id-123",
        "not_found_1": "nonexistent-paper-456",
        "total_requested": 4,
        "total_retrieved": 2,
        "batch_status": "partial_success",
        "execution_time_seconds": 0.87
    }

def semantic_scholar_academic_research_mcp_get_semantic_scholar_papers_batch(paper_ids: List[str]) -> Dict[str, Any]:
    """
    Get details for multiple papers at once using batch API.
    
    Args:
        paper_ids (List[str]): List of paper IDs (max 500)
    
    Returns:
        Dict containing:
        - papers (List[Dict]): List of dictionaries with detailed information about each retrieved paper
        - not_found (List[str]): List of paper IDs that were not found
        - total_requested (int): Total number of paper IDs provided in the input
        - total_retrieved (int): Number of papers successfully retrieved
        - batch_status (str): Indicator of overall batch processing outcome
        - execution_time_seconds (float): Time taken to process the batch request
    
    Raises:
        ValueError: If paper_ids is empty or exceeds 500 items
    """
    if not paper_ids:
        raise ValueError("paper_ids list cannot be empty")
    
    if len(paper_ids) > 500:
        raise ValueError("paper_ids list cannot exceed 500 items")
    
    # Call external API to get flattened data
    api_data = call_external_api("semantic-scholar-academic-research-mcp-get_semantic_scholar_papers_batch")
    
    # Construct papers list from indexed fields
    papers = []
    for i in range(api_data["total_retrieved"]):
        paper_key = f"paper_{i}"
        if f"{paper_key}_title" in api_data:
            paper = {
                "title": api_data[f"{paper_key}_title"],
                "authors": api_data[f"{paper_key}_authors"].split(", "),
                "abstract": api_data[f"{paper_key}_abstract"],
                "year": api_data[f"{paper_key}_year"],
                "citation_count": api_data[f"{paper_key}_citation_count"],
                "reference_count": api_data[f"{paper_key}_reference_count"],
                "doi": api_data[f"{paper_key}_doi"],
                "url": api_data[f"{paper_key}_url"]
            }
            papers.append(paper)
    
    # Construct not_found list from indexed fields
    not_found = []
    for i in range(2):  # We generated 2 not_found items
        not_found_key = f"not_found_{i}"
        if not_found_key in api_data and api_data[not_found_key]:
            not_found.append(api_data[not_found_key])
    
    # Construct final result dictionary matching output schema
    result = {
        "papers": papers,
        "not_found": not_found,
        "total_requested": api_data["total_requested"],
        "total_retrieved": api_data["total_retrieved"],
        "batch_status": api_data["batch_status"],
        "execution_time_seconds": api_data["execution_time_seconds"]
    }
    
    return result