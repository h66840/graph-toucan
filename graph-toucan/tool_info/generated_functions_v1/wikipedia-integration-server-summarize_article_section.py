from typing import Dict, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia article section summarization.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Wikipedia article
        - section_title (str): Title of the requested section
        - summary (str): Summary of the specified section
    """
    return {
        "title": "Artificial Intelligence",
        "section_title": "History",
        "summary": "The history of artificial intelligence (AI) began in antiquity, with myths and stories of artificial beings endowed with intelligence. The modern field of AI was founded in 1956. Early research focused on problem solving and symbolic methods. By the 1980s, AI research shifted to machine learning and statistical approaches. In the 21st century, advances in computing power and data availability have led to breakthroughs in deep learning and neural networks."
    }

def wikipedia_integration_server_summarize_article_section(
    title: str, 
    section_title: str, 
    max_length: Optional[int] = None
) -> Dict[str, str]:
    """
    Get a summary of a specific section of a Wikipedia article.
    
    This function simulates querying an external Wikipedia integration server
    to retrieve a summary of a given section from a specified article.
    
    Args:
        title (str): Title of the Wikipedia article being referenced (required)
        section_title (str): Title of the section within the article that was requested (required)
        max_length (Optional[int]): Maximum length of the summary in characters (optional)
        
    Returns:
        Dict[str, str]: Dictionary containing:
            - title (str): Title of the Wikipedia article
            - section_title (str): Title of the requested section
            - summary (str): Concise summary of the specified section; may contain text indicating 
              the section was not found or is empty
              
    Raises:
        ValueError: If title or section_title is empty or None
    """
    # Input validation
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string")
    
    if not section_title or not isinstance(section_title, str):
        raise ValueError("Section title must be a non-empty string")
    
    # Call external API (simulated)
    api_data = call_external_api("wikipedia-integration-server-summarize_article_section")
    
    # Construct result matching output schema
    result = {
        "title": api_data["title"],
        "section_title": api_data["section_title"],
        "summary": api_data["summary"]
    }
    
    # Apply max_length constraint if specified
    if max_length is not None and max_length > 0:
        if len(result["summary"]) > max_length:
            # Truncate and add ellipsis if needed
            truncated_summary = result["summary"][:max_length].rsplit(' ', 1)[0]
            if len(truncated_summary) < max_length:
                result["summary"] = truncated_summary
            else:
                result["summary"] = result["summary"][:max_length]
            result["summary"] += "..."
    
    return result