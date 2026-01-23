from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar citations and references.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - citation_0_paperId (str): Paper ID of the first citing paper
        - citation_0_title (str): Title of the first citing paper
        - citation_0_authors (str): Authors of the first citing paper (as comma-separated string)
        - citation_0_year (int): Publication year of the first citing paper
        - citation_0_citationCount (int): Citation count of the first citing paper
        - citation_0_influentialCitationCount (int): Influential citation count of the first citing paper
        - citation_0_abstract (str): Abstract of the first citing paper
        - citation_1_paperId (str): Paper ID of the second citing paper
        - citation_1_title (str): Title of the second citing paper
        - citation_1_authors (str): Authors of the second citing paper (as comma-separated string)
        - citation_1_year (int): Publication year of the second citing paper
        - citation_1_citationCount (int): Citation count of the second citing paper
        - citation_1_influentialCitationCount (int): Influential citation count of the second citing paper
        - citation_1_abstract (str): Abstract of the second citing paper
        - reference_0_paperId (str): Paper ID of the first referenced paper
        - reference_0_title (str): Title of the first referenced paper
        - reference_0_authors (str): Authors of the first referenced paper (as comma-separated string)
        - reference_0_year (int): Publication year of the first referenced paper
        - reference_0_citationCount (int): Citation count of the first referenced paper
        - reference_0_influentialCitationCount (int): Influential citation count of the first referenced paper
        - reference_0_abstract (str): Abstract of the first referenced paper
        - reference_1_paperId (str): Paper ID of the second referenced paper
        - reference_1_title (str): Title of the second referenced paper
        - reference_1_authors (str): Authors of the second referenced paper (as comma-separated string)
        - reference_1_year (int): Publication year of the second referenced paper
        - reference_1_citationCount (int): Citation count of the second referenced paper
        - reference_1_influentialCitationCount (int): Influential citation count of the second referenced paper
        - reference_1_abstract (str): Abstract of the second referenced paper
    """
    return {
        "citation_0_paperId": "CIT001",
        "citation_0_title": "Advancements in Neural Networks",
        "citation_0_authors": "John Doe, Jane Smith",
        "citation_0_year": 2022,
        "citation_0_citationCount": 45,
        "citation_0_influentialCitationCount": 12,
        "citation_0_abstract": "This paper explores recent developments in deep learning architectures.",
        
        "citation_1_paperId": "CIT002",
        "citation_1_title": "A Survey on Transformer Models",
        "citation_1_authors": "Alice Johnson, Bob Lee",
        "citation_1_year": 2021,
        "citation_1_citationCount": 67,
        "citation_1_influentialCitationCount": 18,
        "citation_1_abstract": "We review the evolution and applications of transformer-based models.",
        
        "reference_0_paperId": "REF001",
        "reference_0_title": "Attention Is All You Need",
        "reference_0_authors": "Vaswani Ashish, et al.",
        "reference_0_year": 2017,
        "reference_0_citationCount": 35000,
        "reference_0_influentialCitationCount": 2100,
        "reference_0_abstract": "Introducing the transformer architecture for sequence transduction.",
        
        "reference_1_paperId": "REF002",
        "reference_1_title": "BERT: Pre-training of Deep Bidirectional Transformers",
        "reference_1_authors": "Devlin Jacob, et al.",
        "reference_1_year": 2018,
        "reference_1_citationCount": 28000,
        "reference_1_influentialCitationCount": 1900,
        "reference_1_abstract": "Presenting BERT, a method for pre-training bidirectional transformers."
    }

def semantic_scholar_server_get_semantic_scholar_citations_and_references(paper_id: str) -> Dict[str, Any]:
    """
    Fetches citations and references for a given academic paper from Semantic Scholar.
    
    Args:
        paper_id (str): The unique identifier of the paper to retrieve citations and references for.
    
    Returns:
        Dict containing:
        - citations (List[Dict]): List of papers that cite the given paper, each with fields:
            - paperId (str)
            - title (str)
            - authors (List[str])
            - year (int)
            - citationCount (int)
            - influentialCitationCount (int)
            - abstract (str)
        - references (List[Dict]): List of papers referenced by the given paper, each with fields:
            - paperId (str)
            - title (str)
            - authors (List[str])
            - year (int)
            - citationCount (int)
            - influentialCitationCount (int)
            - abstract (str)
    
    Raises:
        ValueError: If paper_id is empty or None.
    """
    if not paper_id:
        raise ValueError("paper_id is required and cannot be empty")

    api_data = call_external_api("semantic-scholar-server-get_semantic_scholar_citations_and_references")
    
    # Construct citations list
    citations = [
        {
            "paperId": api_data["citation_0_paperId"],
            "title": api_data["citation_0_title"],
            "authors": [author.strip() for author in api_data["citation_0_authors"].split(",")],
            "year": api_data["citation_0_year"],
            "citationCount": api_data["citation_0_citationCount"],
            "influentialCitationCount": api_data["citation_0_influentialCitationCount"],
            "abstract": api_data["citation_0_abstract"]
        },
        {
            "paperId": api_data["citation_1_paperId"],
            "title": api_data["citation_1_title"],
            "authors": [author.strip() for author in api_data["citation_1_authors"].split(",")],
            "year": api_data["citation_1_year"],
            "citationCount": api_data["citation_1_citationCount"],
            "influentialCitationCount": api_data["citation_1_influentialCitationCount"],
            "abstract": api_data["citation_1_abstract"]
        }
    ]
    
    # Construct references list
    references = [
        {
            "paperId": api_data["reference_0_paperId"],
            "title": api_data["reference_0_title"],
            "authors": [author.strip() for author in api_data["reference_0_authors"].split(",")],
            "year": api_data["reference_0_year"],
            "citationCount": api_data["reference_0_citationCount"],
            "influentialCitationCount": api_data["reference_0_influentialCitationCount"],
            "abstract": api_data["reference_0_abstract"]
        },
        {
            "paperId": api_data["reference_1_paperId"],
            "title": api_data["reference_1_title"],
            "authors": [author.strip() for author in api_data["reference_1_authors"].split(",")],
            "year": api_data["reference_1_year"],
            "citationCount": api_data["reference_1_citationCount"],
            "influentialCitationCount": api_data["reference_1_influentialCitationCount"],
            "abstract": api_data["reference_1_abstract"]
        }
    ]
    
    return {
        "citations": citations,
        "references": references
    }