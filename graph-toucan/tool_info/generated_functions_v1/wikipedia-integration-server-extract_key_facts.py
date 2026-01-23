from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia integration.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Wikipedia article
        - topic_within_article (str or None): Specific topic or section within the article; None if not provided
        - fact_0 (str): First key fact extracted from the article
        - fact_1 (str): Second key fact extracted from the article
    """
    return {
        "title": "Python (programming language)",
        "topic_within_article": "History",
        "fact_0": "Python was created by Guido van Rossum and first released in 1991.",
        "fact_1": "Python emphasizes code readability and allows developers to express concepts in fewer lines of code than many other languages."
    }

def wikipedia_integration_server_extract_key_facts(title: str, count: Optional[int] = None, topic_within_article: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract key facts from a Wikipedia article, optionally focused on a specific topic.

    Args:
        title (str): The title of the Wikipedia article to extract facts from. Required.
        count (Optional[int]): The number of key facts to extract. If not provided, defaults to 2.
        topic_within_article (Optional[str]): A specific topic or section within the article to focus on. If not provided, facts are extracted from the entire article.

    Returns:
        Dict[str, Any]: A dictionary containing:
            - title (str): Title of the Wikipedia article.
            - topic_within_article (str or None): The focused topic, or None if not specified.
            - facts (List[str]): List of key factual statements extracted, ordered by relevance.

    Raises:
        ValueError: If 'title' is empty or None.
    """
    if not title:
        raise ValueError("The 'title' parameter is required and cannot be empty.")

    # Use default count of 2 if not provided
    effective_count = count if count is not None else 2

    # Call external API to simulate data retrieval
    api_data = call_external_api("wikipedia-integration-server-extract_key_facts")

    # Construct the facts list from indexed fields
    facts = []
    for i in range(effective_count):
        fact_key = f"fact_{i}"
        if fact_key in api_data:
            facts.append(api_data[fact_key])
        else:
            # If API doesn't have enough pre-defined facts, generate fallback ones
            facts.append(f"Additional fact {i} about {title} related to {topic_within_article or 'general overview'}.")

    # Construct final result matching output schema
    result = {
        "title": api_data["title"],
        "topic_within_article": api_data.get("topic_within_article"),
        "facts": facts
    }

    return result