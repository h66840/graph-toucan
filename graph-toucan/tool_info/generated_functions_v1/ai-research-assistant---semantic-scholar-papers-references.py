from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar papers references.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - reference_0_title (str): Title of the first referenced paper
        - reference_0_year (int): Year of the first referenced paper
        - reference_0_authors (str): Comma-separated authors of the first referenced paper
        - reference_0_url (str): URL of the first referenced paper
        - reference_0_influential (bool): Whether the first reference is influential
        - reference_1_title (str): Title of the second referenced paper
        - reference_1_year (int): Year of the second referenced paper
        - reference_1_authors (str): Comma-separated authors of the second referenced paper
        - reference_1_url (str): URL of the second referenced paper
        - reference_1_influential (bool): Whether the second reference is influential
        - total_count_message (str): Message indicating total count and pagination suggestion
    """
    return {
        "reference_0_title": "Attention Is All You Need",
        "reference_0_year": 2017,
        "reference_0_authors": "Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin",
        "reference_0_url": "https://www.semanticscholar.org/paper/Attention-Is-All-You-Need-Vaswani-Shazeer/...",
        "reference_0_influential": True,
        "reference_1_title": "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "reference_1_year": 2018,
        "reference_1_authors": "Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        "reference_1_url": "https://www.semanticscholar.org/paper/BERT%3A-Pre-training-of-Deep-Bidirectional-Devlin-Chang/...",
        "reference_1_influential": True,
        "total_count_message": "More than 2 references available. Use offset=2 to retrieve the next set."
    }

def ai_research_assistant_semantic_scholar_papers_references(
    paperId: str, 
    limit: Optional[int] = None, 
    offset: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get papers cited by a specific paper using its Semantic Scholar ID, arXiv ID, or DOI.
    
    Args:
        paperId (str): Required. The ID of the paper (Semantic Scholar ID, arXiv ID, DOI, etc.)
        limit (Optional[int]): Maximum number of references to return. Defaults to None.
        offset (Optional[int]): Offset for pagination. Defaults to None.
    
    Returns:
        Dict containing:
        - references (List[Dict]): List of reference papers with 'title', 'year', 'authors', 'url', and optional 'influential'
        - total_count_message (str): Message indicating more references are available and suggests using offset for pagination
    
    Raises:
        ValueError: If paperId is empty or not provided
    """
    if not paperId or not paperId.strip():
        raise ValueError("paperId is required and cannot be empty")

    # Fetch simulated external data
    api_data = call_external_api("ai-research-assistant---semantic-scholar-papers-references")
    
    # Construct references list from flattened API response
    references: List[Dict[str, Any]] = []
    
    for i in range(2):  # Two references as per simulation
        title_key = f"reference_{i}_title"
        year_key = f"reference_{i}_year"
        authors_key = f"reference_{i}_authors"
        url_key = f"reference_{i}_url"
        influential_key = f"reference_{i}_influential"
        
        if title_key in api_data:
            reference: Dict[str, Any] = {
                "title": api_data[title_key],
                "year": api_data[year_key],
                "authors": api_data[authors_key],
                "url": api_data[url_key]
            }
            # Add optional 'influential' field if present and True
            if influential_key in api_data and api_data[influential_key]:
                reference["influential"] = api_data[influential_key]
            references.append(reference)
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        references = references[:limit]
    
    return {
        "references": references,
        "total_count_message": api_data["total_count_message"]
    }