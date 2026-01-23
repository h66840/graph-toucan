from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar paper recommendations.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - recommendation_0_paperId (str): Paper ID of first recommended paper
        - recommendation_0_title (str): Title of first recommended paper
        - recommendation_0_abstract (str): Abstract of first recommended paper
        - recommendation_0_year (int): Publication year of first paper
        - recommendation_0_citationCount (int): Citation count of first paper
        - recommendation_0_influentialCitationCount (int): Influential citation count of first paper
        - recommendation_0_fieldsOfStudy_0 (str): First field of study for first paper
        - recommendation_0_fieldsOfStudy_1 (str): Second field of study for first paper
        - recommendation_0_score (float): Relevance score of first paper
        - recommendation_0_author_0_name (str): First author name of first paper
        - recommendation_0_author_1_name (str): Second author name of first paper
        - recommendation_0_url (str): URL of first paper
        - recommendation_0_publicationDate (str): Publication date of first paper
        - recommendation_0_venue (str): Venue of first paper
        - recommendation_1_paperId (str): Paper ID of second recommended paper
        - recommendation_1_title (str): Title of second recommended paper
        - recommendation_1_abstract (str): Abstract of second recommended paper
        - recommendation_1_year (int): Publication year of second paper
        - recommendation_1_citationCount (int): Citation count of second paper
        - recommendation_1_influentialCitationCount (int): Influential citation count of second paper
        - recommendation_1_fieldsOfStudy_0 (str): First field of study for second paper
        - recommendation_1_fieldsOfStudy_1 (str): Second field of study for second paper
        - recommendation_1_score (float): Relevance score of second paper
        - recommendation_1_author_0_name (str): First author name of second paper
        - recommendation_1_author_1_name (str): Second author name of second paper
        - recommendation_1_url (str): URL of second paper
        - recommendation_1_publicationDate (str): Publication date of second paper
        - recommendation_1_venue (str): Venue of second paper
        - total_results (int): Total number of results available
        - next_page_token (str): Token for next page, or null if none
    """
    return {
        "recommendation_0_paperId": "1234567890abcdef",
        "recommendation_0_title": "A Study on Machine Learning Techniques in Academic Research",
        "recommendation_0_abstract": "This paper explores the application of machine learning techniques in academic research with a focus on citation analysis and paper recommendation systems.",
        "recommendation_0_year": 2022,
        "recommendation_0_citationCount": 45,
        "recommendation_0_influentialCitationCount": 12,
        "recommendation_0_fieldsOfStudy_0": "Computer Science",
        "recommendation_0_fieldsOfStudy_1": "Artificial Intelligence",
        "recommendation_0_score": 0.95,
        "recommendation_0_author_0_name": "Alice Johnson",
        "recommendation_0_author_1_name": "Bob Smith",
        "recommendation_0_url": "https://www.semanticscholar.org/paper/1234567890abcdef",
        "recommendation_0_publicationDate": "2022-05-15",
        "recommendation_0_venue": "NeurIPS",
        "recommendation_1_paperId": "fedcba0987654321",
        "recommendation_1_title": "Advancements in Natural Language Processing for Scholarly Articles",
        "recommendation_1_abstract": "We present novel NLP methods tailored for processing and understanding scholarly articles, improving retrieval and recommendation accuracy.",
        "recommendation_1_year": 2023,
        "recommendation_1_citationCount": 32,
        "recommendation_1_influentialCitationCount": 8,
        "recommendation_1_fieldsOfStudy_0": "Natural Language Processing",
        "recommendation_1_fieldsOfStudy_1": "Information Retrieval",
        "recommendation_1_score": 0.87,
        "recommendation_1_author_0_name": "Carol Davis",
        "recommendation_1_author_1_name": "David Wilson",
        "recommendation_1_url": "https://www.semanticscholar.org/paper/fedcba0987654321",
        "recommendation_1_publicationDate": "2023-02-20",
        "recommendation_1_venue": "ACL",
        "total_results": 150,
        "next_page_token": "next_page_abc123"
    }

def semantic_scholar_academic_research_mcp_get_semantic_scholar_paper_recommendations_from_lists(
    positive_paper_ids: List[str],
    negative_paper_ids: Optional[List[str]] = None,
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Get recommended papers based on lists of positive and negative example papers.
    
    Args:
        positive_paper_ids (List[str]): List of paper IDs that represent positive examples (papers you like/want similar to)
        negative_paper_ids (Optional[List[str]]): Optional list of paper IDs that represent negative examples (papers you don't want similar to)
        limit (Optional[int]): Number of recommendations to return (default: 10, max: 500)
    
    Returns:
        Dict containing:
        - recommendations (List[Dict]): list of recommended papers with their details and relevance scores
        - next_page_token (str): token to use for retrieving the next page of results, if available; null if no more pages
        - total_results (int): total number of results available for this recommendation query
    
    Raises:
        ValueError: If positive_paper_ids is empty or None
        TypeError: If inputs are not of expected types
    """
    # Input validation
    if not positive_paper_ids:
        raise ValueError("positive_paper_ids must be a non-empty list")
    
    if not isinstance(positive_paper_ids, list):
        raise TypeError("positive_paper_ids must be a list")
    
    if negative_paper_ids is not None and not isinstance(negative_paper_ids, list):
        raise TypeError("negative_paper_ids must be a list or None")
    
    if limit is not None:
        if not isinstance(limit, int):
            raise TypeError("limit must be an integer")
        if limit < 1:
            raise ValueError("limit must be at least 1")
        if limit > 500:
            raise ValueError("limit cannot exceed 500")
    
    # Call external API to get data (simulated)
    api_data = call_external_api("semantic-scholar-academic-research-mcp-get_semantic_scholar_paper_recommendations_from_lists")
    
    # Construct recommendations list from flattened API data
    recommendations = []
    
    # Process first recommendation
    if "recommendation_0_paperId" in api_data:
        recommendation_0 = {
            "paperId": api_data["recommendation_0_paperId"],
            "title": api_data["recommendation_0_title"],
            "abstract": api_data["recommendation_0_abstract"],
            "year": api_data["recommendation_0_year"],
            "citationCount": api_data["recommendation_0_citationCount"],
            "influentialCitationCount": api_data["recommendation_0_influentialCitationCount"],
            "fieldsOfStudy": [
                api_data["recommendation_0_fieldsOfStudy_0"],
                api_data["recommendation_0_fieldsOfStudy_1"]
            ],
            "score": api_data["recommendation_0_score"],
            "authors": [
                {"name": api_data["recommendation_0_author_0_name"]},
                {"name": api_data["recommendation_0_author_1_name"]}
            ],
            "url": api_data["recommendation_0_url"],
            "publicationDate": api_data["recommendation_0_publicationDate"],
            "venue": api_data["recommendation_0_venue"]
        }
        recommendations.append(recommendation_0)
    
    # Process second recommendation
    if "recommendation_1_paperId" in api_data:
        recommendation_1 = {
            "paperId": api_data["recommendation_1_paperId"],
            "title": api_data["recommendation_1_title"],
            "abstract": api_data["recommendation_1_abstract"],
            "year": api_data["recommendation_1_year"],
            "citationCount": api_data["recommendation_1_citationCount"],
            "influentialCitationCount": api_data["recommendation_1_influentialCitationCount"],
            "fieldsOfStudy": [
                api_data["recommendation_1_fieldsOfStudy_0"],
                api_data["recommendation_1_fieldsOfStudy_1"]
            ],
            "score": api_data["recommendation_1_score"],
            "authors": [
                {"name": api_data["recommendation_1_author_0_name"]},
                {"name": api_data["recommendation_1_author_1_name"]}
            ],
            "url": api_data["recommendation_1_url"],
            "publicationDate": api_data["recommendation_1_publicationDate"],
            "venue": api_data["recommendation_1_venue"]
        }
        recommendations.append(recommendation_1)
    
    # Construct and return final result
    result = {
        "recommendations": recommendations,
        "next_page_token": api_data.get("next_page_token"),
        "total_results": api_data.get("total_results", 0)
    }
    
    return result