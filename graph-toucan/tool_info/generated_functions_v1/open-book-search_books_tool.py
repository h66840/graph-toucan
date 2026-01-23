from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for book search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first book result
        - result_0_author (str): Author of the first book result
        - result_0_year (int): Publication year of the first book result
        - result_0_description (str): Description of the first book result
        - result_0_isbn (str): ISBN of the first book result
        - result_1_title (str): Title of the second book result
        - result_1_author (str): Author of the second book result
        - result_1_year (int): Publication year of the second book result
        - result_1_description (str): Description of the second book result
        - result_1_isbn (str): ISBN of the second book result
        - error_message (str): Error message if no books found (empty string if results exist)
    """
    return {
        "result_0_title": "The Great Gatsby",
        "result_0_author": "F. Scott Fitzgerald",
        "result_0_year": 1925,
        "result_0_description": "A classic American novel set in the Jazz Age.",
        "result_0_isbn": "978-0-7432-7356-5",
        "result_1_title": "To Kill a Mockingbird",
        "result_1_author": "Harper Lee",
        "result_1_year": 1960,
        "result_1_description": "A powerful story of racial injustice and childhood innocence.",
        "result_1_isbn": "978-0-06-112008-4",
        "error_message": ""
    }

def open_book_search_books_tool(query: str) -> Dict[str, Any]:
    """
    Performs a book search based on the user's query.
    
    Args:
        query (str): The search query for finding books.
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of book entries with 'title', 'author', 'year', 'description', and 'isbn'
        - error_message (Optional[str]): Error message if no books were found, otherwise None
        
    Raises:
        ValueError: If query is empty or not a string.
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string.")
    
    api_data = call_external_api("open-book-search_books_tool")
    
    # Check for error message from API
    if api_data.get("error_message"):
        return {
            "error_message": api_data["error_message"]
        }
    
    # Construct results list from flattened API response
    results = [
        {
            "title": api_data["result_0_title"],
            "author": api_data["result_0_author"],
            "year": api_data["result_0_year"],
            "description": api_data["result_0_description"],
            "isbn": api_data["result_0_isbn"]
        },
        {
            "title": api_data["result_1_title"],
            "author": api_data["result_1_author"],
            "year": api_data["result_1_year"],
            "description": api_data["result_1_description"],
            "isbn": api_data["result_1_isbn"]
        }
    ]
    
    return {
        "results": results
    }