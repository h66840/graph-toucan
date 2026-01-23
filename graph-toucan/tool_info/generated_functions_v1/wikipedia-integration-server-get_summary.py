from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the Wikipedia article
        - summary (str): Comprehensive summary text of the Wikipedia article
    """
    return {
        "title": "Python (programming language)",
        "summary": "Python is a high-level, interpreted programming language known for its simplicity and readability. "
                   "Created by Guido van Rossum and first released in 1991, Python emphasizes code readability with "
                   "its use of significant indentation. It supports multiple programming paradigms, including "
                   "procedural, object-oriented, and functional programming. Python is dynamically typed and "
                   "garbage-collected, making it suitable for rapid application development. It has a large standard "
                   "library and a vibrant ecosystem of third-party packages, particularly in data science, machine "
                   "learning, web development, and automation. Python's design philosophy is outlined in the Zen of "
                   "Python, which includes principles like 'Readability counts' and 'Simple is better than complex.'"
    }

def wikipedia_integration_server_get_summary(title: str) -> Dict[str, str]:
    """
    Get a summary of a Wikipedia article.
    
    This function simulates retrieving a summary from a Wikipedia article based on the given title.
    It uses a mock external API call to obtain the data and returns the article's title and summary.
    
    Args:
        title (str): The title of the Wikipedia article to retrieve.
        
    Returns:
        Dict[str, str]: A dictionary containing:
            - title (str): The title of the Wikipedia article.
            - summary (str): A comprehensive summary of the article covering key historical, conceptual, and contextual information.
            
    Raises:
        ValueError: If the title is empty or not a string.
    """
    if not title or not isinstance(title, str):
        raise ValueError("Title must be a non-empty string.")
    
    # Simulate external API call
    api_data = call_external_api("wikipedia-integration-server-get_summary")
    
    # Construct result matching output schema
    result = {
        "title": api_data["title"],
        "summary": api_data["summary"]
    }
    
    return result