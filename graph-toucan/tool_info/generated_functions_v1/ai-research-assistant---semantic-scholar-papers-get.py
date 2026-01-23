from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for a specific paper.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the paper
        - authors_0 (str): First author name
        - authors_1 (str): Second author name
        - year (int): Publication year
        - venue (str): Publication venue (e.g., journal, conference)
        - citations (int): Number of citations
        - fields_of_study_0 (str): First field of study
        - fields_of_study_1 (str): Second field of study
        - abstract (str): Full abstract text of the paper
        - url (str): Semantic Scholar URL for the paper
        - open_access (bool): Whether the paper is open access
        - pdf_url (str): Direct URL to the PDF version of the paper, if available
    """
    return {
        "title": "A Comprehensive Study on Neural Networks",
        "authors_0": "John Smith",
        "authors_1": "Jane Doe",
        "year": 2022,
        "venue": "NeurIPS",
        "citations": 150,
        "fields_of_study_0": "Computer Science",
        "fields_of_study_1": "Artificial Intelligence",
        "abstract": "This paper presents a comprehensive analysis of neural networks, focusing on deep learning architectures and their applications in various domains such as computer vision and natural language processing. We review recent advances and discuss future directions.",
        "url": "https://www.semanticscholar.org/paper/A-Comprehensive-Study-on-Neural-Networks/1234567890",
        "open_access": True,
        "pdf_url": "https://www.semanticscholar.org/paper/A-Comprehensive-Study-on-Neural-Networks/1234567890/pdf"
    }

def ai_research_assistant_semantic_scholar_papers_get(paperId: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific paper using its paper ID.
    
    Args:
        paperId (str): Paper ID (Semantic Scholar ID, arXiv ID, DOI, etc.)
    
    Returns:
        Dict containing:
            - title (str): title of the paper
            - authors (List[str]): list of author names
            - year (int): publication year
            - venue (str): publication venue (e.g., journal, conference)
            - citations (int): number of citations
            - fields_of_study (List[str]): academic fields or domains the paper belongs to
            - abstract (str): full abstract text of the paper
            - url (str): Semantic Scholar URL for the paper
            - open_access (bool): whether the paper is open access
            - pdf_url (str): direct URL to the PDF version of the paper, if available
    
    Raises:
        ValueError: If paperId is empty or invalid
    """
    if not paperId or not paperId.strip():
        raise ValueError("paperId is required and cannot be empty")

    # Call the external API simulation
    api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-get")

    # Construct the output structure matching the schema
    result = {
        "title": api_data["title"],
        "authors": [
            api_data["authors_0"],
            api_data["authors_1"]
        ],
        "year": api_data["year"],
        "venue": api_data["venue"],
        "citations": api_data["citations"],
        "fields_of_study": [
            api_data["fields_of_study_0"],
            api_data["fields_of_study_1"]
        ],
        "abstract": api_data["abstract"],
        "url": api_data["url"],
        "open_access": api_data["open_access"],
        "pdf_url": api_data["pdf_url"]
    }

    return result