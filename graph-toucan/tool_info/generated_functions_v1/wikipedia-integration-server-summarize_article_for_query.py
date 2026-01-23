from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia article summarization.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Wikipedia article that was summarized
        - query (str): The original query used to tailor the summary
        - summary (str): Generated concise summary text tailored to the given query
    """
    return {
        "title": "Artificial Intelligence",
        "query": "applications in healthcare",
        "summary": "Artificial intelligence has been increasingly applied in healthcare for tasks such as medical imaging analysis, diagnosis support, drug discovery, and personalized treatment planning. AI systems can process large volumes of patient data to identify patterns and support clinical decision-making."
    }

def wikipedia_integration_server_summarize_article_for_query(
    title: str, 
    query: str, 
    max_length: Optional[int] = None
) -> Dict[str, Any]:
    """
    Get a summary of a Wikipedia article tailored to a specific query.
    
    This function simulates retrieving and summarizing a Wikipedia article based on the provided title,
    with the summary focused on the aspect specified in the query. The summary length may be constrained
    if max_length is provided.
    
    Args:
        title (str): The title of the Wikipedia article to summarize. Required.
        query (str): The specific aspect or focus for tailoring the summary. Required.
        max_length (Optional[int]): Maximum number of characters for the summary. If None, no limit is applied.
        
    Returns:
        Dict[str, Any] with the following structure:
        - title (str): Title of the Wikipedia article that was summarized
        - query (str): The original query used to tailor the summary
        - summary (str): The generated concise summary text from the Wikipedia article, tailored to the given query
    """
    if not title:
        raise ValueError("Parameter 'title' is required and cannot be empty.")
    if not query:
        raise ValueError("Parameter 'query' is required and cannot be empty.")
    
    # Simulate calling external API to get summary data
    api_data = call_external_api("wikipedia-integration-server-summarize_article_for_query")
    
    # Construct result matching output schema
    result = {
        "title": api_data["title"],
        "query": api_data["query"],
        "summary": api_data["summary"]
    }
    
    # Apply max_length constraint if specified
    if max_length is not None and len(result["summary"]) > max_length:
        result["summary"] = result["summary"][:max_length].rsplit(' ', 1)[0] + "..."
    
    return result