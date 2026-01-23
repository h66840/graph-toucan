from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia related topics.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Wikipedia article
        - related_topics_0_title (str): Title of the first related topic
        - related_topics_0_type (str): Type of the first related topic ('link' or 'category')
        - related_topics_0_summary (str): Summary of the first related topic (if available)
        - related_topics_0_url (str): URL of the first related topic (if available)
        - related_topics_1_title (str): Title of the second related topic
        - related_topics_1_type (str): Type of the second related topic ('link' or 'category')
        - related_topics_1_summary (str): Summary of the second related topic (if available)
        - related_topics_1_url (str): URL of the second related topic (if available)
    """
    return {
        "title": "Artificial Intelligence",
        "related_topics_0_title": "Machine Learning",
        "related_topics_0_type": "link",
        "related_topics_0_summary": "Method of teaching computers to learn from data.",
        "related_topics_0_url": "https://en.wikipedia.org/wiki/Machine_Learning",
        "related_topics_1_title": "Natural Language Processing",
        "related_topics_1_type": "category",
        "related_topics_1_summary": "Branch of AI focused on interaction between computers and human language.",
        "related_topics_1_url": "https://en.wikipedia.org/wiki/Natural_Language_Processing"
    }

def wikipedia_integration_server_get_related_topics(title: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Get topics related to a Wikipedia article based on links and categories.
    
    Args:
        title (str): Title of the Wikipedia article for which related topics are retrieved (required)
        limit (Optional[int]): Maximum number of related topics to return (optional)
    
    Returns:
        Dict containing:
        - title (str): Title of the Wikipedia article
        - related_topics (List[Dict]): List of related topics, each containing:
            - title (str): Title of the related topic
            - type (str): Type of the related topic ('link' or 'category')
            - summary (Optional[str]): Summary of the related topic if available
            - url (Optional[str]): URL of the related topic if available
    
    Raises:
        ValueError: If title is empty or None
    """
    if not title:
        raise ValueError("Title is required and cannot be empty")
    
    # Fetch simulated external data
    api_data = call_external_api("wikipedia-integration-server-get_related_topics")
    
    # Construct related topics list from flattened API response
    related_topics = []
    
    # Process first related topic
    if "related_topics_0_title" in api_data:
        topic_0 = {
            "title": api_data["related_topics_0_title"],
            "type": api_data["related_topics_0_type"]
        }
        if "related_topics_0_summary" in api_data:
            topic_0["summary"] = api_data["related_topics_0_summary"]
        if "related_topics_0_url" in api_data:
            topic_0["url"] = api_data["related_topics_0_url"]
        related_topics.append(topic_0)
    
    # Process second related topic
    if "related_topics_1_title" in api_data:
        topic_1 = {
            "title": api_data["related_topics_1_title"],
            "type": api_data["related_topics_1_type"]
        }
        if "related_topics_1_summary" in api_data:
            topic_1["summary"] = api_data["related_topics_1_summary"]
        if "related_topics_1_url" in api_data:
            topic_1["url"] = api_data["related_topics_1_url"]
        related_topics.append(topic_1)
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        related_topics = related_topics[:limit]
    
    # Construct final result
    result = {
        "title": api_data["title"],
        "related_topics": related_topics
    }
    
    return result