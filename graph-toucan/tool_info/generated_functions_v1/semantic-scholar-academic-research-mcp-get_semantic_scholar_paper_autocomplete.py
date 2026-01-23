from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Semantic Scholar paper autocomplete.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - suggestion_0_title (str): First suggested paper title
        - suggestion_0_score (float): Relevance score for first suggestion
        - suggestion_1_title (str): Second suggested paper title
        - suggestion_1_score (float): Relevance score for second suggestion
        - count (int): Total number of suggestions returned
        - query_truncated (bool): Whether the input query was truncated
    """
    return {
        "suggestion_0_title": "Attention Is All You Need",
        "suggestion_0_score": 0.98,
        "suggestion_1_title": "A Survey on Transformer-based Models in Natural Language Processing",
        "suggestion_1_score": 0.92,
        "count": 2,
        "query_truncated": False
    }

def semantic_scholar_academic_research_mcp_get_semantic_scholar_paper_autocomplete(query: str) -> Dict[str, Any]:
    """
    Get paper title autocompletion suggestions for a partial query.

    Args:
        query (str): Partial paper title query (will be truncated to 100 characters)

    Returns:
        Dict containing:
        - suggestions (List[Dict]): List of autocomplete suggestion objects, each with 'title' and 'score'
        - count (int): Total number of suggestions returned
        - query_truncated (bool): Whether the input query was truncated to 100 characters
    """
    if not isinstance(query, str):
        raise TypeError("Query must be a string")

    if len(query) > 100:
        truncated_query = query[:100]
        query_truncated = True
    else:
        truncated_query = query
        query_truncated = False

    # Call external API simulation (only uses the original query for realistic behavior)
    api_data = call_external_api("semantic-scholar-academic-research-mcp-get_semantic_scholar_paper_autocomplete")

    # Construct suggestions list from flattened API response
    suggestions = [
        {
            "title": api_data["suggestion_0_title"],
            "score": api_data["suggestion_0_score"]
        },
        {
            "title": api_data["suggestion_1_title"],
            "score": api_data["suggestion_1_score"]
        }
    ]

    # Return structured response matching output schema
    return {
        "suggestions": suggestions,
        "count": api_data["count"],
        "query_truncated": api_data["query_truncated"]
    }