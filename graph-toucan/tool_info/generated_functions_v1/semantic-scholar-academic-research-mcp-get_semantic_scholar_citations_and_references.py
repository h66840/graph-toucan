from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching citations and references data from external API for a paper.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - citation_0_contexts_0 (str): First context string for first citation
        - citation_0_contexts_1 (str): Second context string for first citation
        - citation_0_isInfluential (bool): Whether first citation is influential
        - citation_0_citingPaper_paperId (str): Paper ID of first citing paper
        - citation_0_citingPaper_title (str): Title of first citing paper
        - citation_0_citingPaper_authors (str): Authors of first citing paper (comma-separated)
        - citation_0_citingPaper_year (int): Year of first citing paper
        - citation_0_citingPaper_venue (str): Venue of first citing paper
        - citation_1_contexts_0 (str): First context string for second citation
        - citation_1_contexts_1 (str): Second context string for second citation
        - citation_1_isInfluential (bool): Whether second citation is influential
        - citation_1_citingPaper_paperId (str): Paper ID of second citing paper
        - citation_1_citingPaper_title (str): Title of second citing paper
        - citation_1_citingPaper_authors (str): Authors of second citing paper (comma-separated)
        - citation_1_citingPaper_year (int): Year of second citing paper
        - citation_1_citingPaper_venue (str): Venue of second citing paper
        - reference_0_contexts_0 (str): First context string for first reference
        - reference_0_contexts_1 (str): Second context string for first reference
        - reference_0_isInfluential (bool): Whether first reference is influential
        - reference_0_citedPaper_paperId (str): Paper ID of first cited paper
        - reference_0_citedPaper_title (str): Title of first cited paper
        - reference_0_citedPaper_authors (str): Authors of first cited paper (comma-separated)
        - reference_0_citedPaper_year (int): Year of first cited paper
        - reference_0_citedPaper_venue (str): Venue of first cited paper
        - reference_1_contexts_0 (str): First context string for second reference
        - reference_1_contexts_1 (str): Second context string for second reference
        - reference_1_isInfluential (bool): Whether second reference is influential
        - reference_1_citedPaper_paperId (str): Paper ID of second cited paper
        - reference_1_citedPaper_title (str): Title of second cited paper
        - reference_1_citedPaper_authors (str): Authors of second cited paper (comma-separated)
        - reference_1_citedPaper_year (int): Year of second cited paper
        - reference_1_citedPaper_venue (str): Venue of second cited paper
    """
    return {
        "citation_0_contexts_0": "This paper builds upon the methodology introduced by Smith et al.",
        "citation_0_contexts_1": "We extend the framework proposed in this work to dynamic environments.",
        "citation_0_isInfluential": True,
        "citation_0_citingPaper_paperId": "corpusId:123456789",
        "citation_0_citingPaper_title": "Advancements in Machine Learning for NLP",
        "citation_0_citingPaper_authors": "Alice Johnson, Bob Lee",
        "citation_0_citingPaper_year": 2022,
        "citation_0_citingPaper_venue": "ACL",
        "citation_1_contexts_0": "Our model uses the attention mechanism described here.",
        "citation_1_contexts_1": "Inspired by the experimental setup in this paper.",
        "citation_1_isInfluential": False,
        "citation_1_citingPaper_paperId": "corpusId:987654321",
        "citation_1_citingPaper_title": "Efficient Transformers for Long Sequences",
        "citation_1_citingPaper_authors": "Charlie Davis, Diana Moore",
        "citation_1_citingPaper_year": 2023,
        "citation_1_citingPaper_venue": "NeurIPS",
        "reference_0_contexts_0": "This work relies on foundational concepts from earlier research.",
        "reference_0_contexts_1": "We adopt the theoretical framework established in this study.",
        "reference_0_isInfluential": True,
        "reference_0_citedPaper_paperId": "corpusId:112233445",
        "reference_0_citedPaper_title": "Foundations of Deep Learning",
        "reference_0_citedPaper_authors": "Geoffrey Hinton, Yann LeCun",
        "reference_0_citedPaper_year": 2015,
        "reference_0_citedPaper_venue": "Nature",
        "reference_1_contexts_0": "Our approach is based on the optimization technique introduced here.",
        "reference_1_contexts_1": "We follow the evaluation protocol from this paper.",
        "reference_1_isInfluential": True,
        "reference_1_citedPaper_paperId": "corpusId:556677889",
        "reference_1_citedPaper_title": "Optimization Methods in Neural Networks",
        "reference_1_citedPaper_authors": "Rachel Green, Paul Atreides",
        "reference_1_citedPaper_year": 2018,
        "reference_1_citedPaper_venue": "ICML"
    }

def semantic_scholar_academic_research_mcp_get_semantic_scholar_citations_and_references(paper_id: str) -> Dict[str, Any]:
    """
    Get citations and references for a specific paper on Semantic Scholar.

    Args:
        paper_id (str): ID of the paper

    Returns:
        Dictionary containing lists of citations and references
        - citations (List[Dict]): list of citation entries, each containing 'contexts' (List[str]), 
          'isInfluential' (bool), and 'citingPaper' (Dict with 'paperId', 'title', 'authors', 'year', 'venue')
        - references (List[Dict]): list of reference entries, each structurally similar to citations, 
          with 'contexts', 'isInfluential', and 'citedPaper' information
    """
    if not paper_id or not isinstance(paper_id, str):
        raise ValueError("paper_id must be a non-empty string")

    api_data = call_external_api("semantic-scholar-academic-research-mcp-get_semantic_scholar_citations_and_references")

    # Construct citations list
    citations = [
        {
            "contexts": [
                api_data["citation_0_contexts_0"],
                api_data["citation_0_contexts_1"]
            ],
            "isInfluential": api_data["citation_0_isInfluential"],
            "citingPaper": {
                "paperId": api_data["citation_0_citingPaper_paperId"],
                "title": api_data["citation_0_citingPaper_title"],
                "authors": api_data["citation_0_citingPaper_authors"].split(", "),
                "year": api_data["citation_0_citingPaper_year"],
                "venue": api_data["citation_0_citingPaper_venue"]
            }
        },
        {
            "contexts": [
                api_data["citation_1_contexts_0"],
                api_data["citation_1_contexts_1"]
            ],
            "isInfluential": api_data["citation_1_isInfluential"],
            "citingPaper": {
                "paperId": api_data["citation_1_citingPaper_paperId"],
                "title": api_data["citation_1_citingPaper_title"],
                "authors": api_data["citation_1_citingPaper_authors"].split(", "),
                "year": api_data["citation_1_citingPaper_year"],
                "venue": api_data["citation_1_citingPaper_venue"]
            }
        }
    ]

    # Construct references list
    references = [
        {
            "contexts": [
                api_data["reference_0_contexts_0"],
                api_data["reference_0_contexts_1"]
            ],
            "isInfluential": api_data["reference_0_isInfluential"],
            "citedPaper": {
                "paperId": api_data["reference_0_citedPaper_paperId"],
                "title": api_data["reference_0_citedPaper_title"],
                "authors": api_data["reference_0_citedPaper_authors"].split(", "),
                "year": api_data["reference_0_citedPaper_year"],
                "venue": api_data["reference_0_citedPaper_venue"]
            }
        },
        {
            "contexts": [
                api_data["reference_1_contexts_0"],
                api_data["reference_1_contexts_1"]
            ],
            "isInfluential": api_data["reference_1_isInfluential"],
            "citedPaper": {
                "paperId": api_data["reference_1_citedPaper_paperId"],
                "title": api_data["reference_1_citedPaper_title"],
                "authors": api_data["reference_1_citedPaper_authors"].split(", "),
                "year": api_data["reference_1_citedPaper_year"],
                "venue": api_data["reference_1_citedPaper_venue"]
            }
        }
    ]

    return {
        "citations": citations,
        "references": references
    }