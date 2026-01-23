from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external Wikipedia API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): the title of the Wikipedia article
        - pageid (int): unique identifier for the Wikipedia page
        - summary (str): a concise summary of the article's content
        - text (str): the full plain-text content of the article
        - url (str): the full URL to the Wikipedia article
        - section_0_title (str): title of the first section
        - section_0_level (int): heading level of the first section
        - section_0_text (str): text content of the first section
        - section_1_title (str): title of the second section
        - section_1_level (int): heading level of the second section
        - section_1_text (str): text content of the second section
        - category_0 (str): first category associated with the article
        - category_1 (str): second category associated with the article
        - link_0 (str): title of the first linked Wikipedia page
        - link_1 (str): title of the second linked Wikipedia page
        - exists (bool): indicates whether the requested article exists
    """
    return {
        "title": "Python (programming language)",
        "pageid": 23862,
        "summary": "Python is a high-level, general-purpose programming language.",
        "text": "Python is a high-level, general-purpose programming language. It is widely used for web development, data analysis, artificial intelligence, and more. Python emphasizes code readability and allows developers to express concepts in fewer lines of code than many other languages.",
        "url": "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "section_0_title": "History",
        "section_0_level": 2,
        "section_0_text": "Python was created in the late 1980s by Guido van Rossum at Centrum Wiskunde & Informatica (CWI) in the Netherlands.",
        "section_1_title": "Features",
        "section_1_level": 2,
        "section_1_text": "Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured, object-oriented, and functional programming.",
        "category_0": "Programming languages",
        "category_1": "Python (programming language)",
        "link_0": "Guido van Rossum",
        "link_1": "Object-oriented programming",
        "exists": True
    }

def wikipedia_integration_server_get_article(title: str) -> Dict[str, Any]:
    """
    Get the full content of a Wikipedia article.
    
    Args:
        title (str): The title of the Wikipedia article to retrieve.
        
    Returns:
        Dict containing the following keys:
        - title (str): the title of the Wikipedia article
        - pageid (int): unique identifier for the Wikipedia page
        - summary (str): a concise summary of the article's content
        - text (str): the full plain-text content of the article
        - url (str): the full URL to the Wikipedia article
        - sections (List[Dict]): list of section objects with 'title', 'level', 'text', and 'sections' fields
        - categories (List[str]): list of Wikipedia categories associated with the article
        - links (List[str]): list of titles of other Wikipedia pages linked within this article
        - exists (bool): indicates whether the requested article exists on Wikipedia
    """
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string.")
        
    api_data = call_external_api("wikipedia-integration-server-get_article")
    
    # Construct sections list
    sections = [
        {
            "title": api_data["section_0_title"],
            "level": api_data["section_0_level"],
            "text": api_data["section_0_text"],
            "sections": []
        },
        {
            "title": api_data["section_1_title"],
            "level": api_data["section_1_level"],
            "text": api_data["section_1_text"],
            "sections": []
        }
    ]
    
    # Construct categories list
    categories = [
        api_data["category_0"],
        api_data["category_1"]
    ]
    
    # Construct links list
    links = [
        api_data["link_0"],
        api_data["link_1"]
    ]
    
    # Build final result structure
    result = {
        "title": api_data["title"],
        "pageid": api_data["pageid"],
        "summary": api_data["summary"],
        "text": api_data["text"],
        "url": api_data["url"],
        "sections": sections,
        "categories": categories,
        "links": links,
        "exists": api_data["exists"]
    }
    
    return result