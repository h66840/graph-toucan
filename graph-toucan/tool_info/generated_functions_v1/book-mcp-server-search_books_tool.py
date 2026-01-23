from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for book search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first found book
        - result_0_authors_0 (str): First author of the first book
        - result_0_authors_1 (str): Second author of the first book (if exists)
        - result_1_title (str): Title of the second found book
        - result_1_authors_0 (str): First author of the second book
        - result_1_authors_1 (str): Second author of the second book (if exists)
        - found_books_count (int): Number of books found in the search
        - error_message (str): Error message if no books found or other issues
    """
    # Simulate realistic book search results based on tool name
    if tool_name == "book-mcp-server-search_books_tool":
        return {
            "result_0_title": "The Great Gatsby",
            "result_0_authors_0": "F. Scott Fitzgerald",
            "result_0_authors_1": "",
            "result_1_title": "To Kill a Mockingbird",
            "result_1_authors_0": "Harper Lee",
            "result_1_authors_1": "",
            "found_books_count": 2,
            "error_message": ""
        }
    else:
        return {
            "result_0_title": "",
            "result_0_authors_0": "",
            "result_0_authors_1": "",
            "result_1_title": "",
            "result_1_authors_0": "",
            "result_1_authors_1": "",
            "found_books_count": 0,
            "error_message": "Unknown tool name"
        }

def book_mcp_server_search_books_tool(query: str) -> Dict[str, Any]:
    """
    Kullanıcıdan gelen sorguyla kitap araması yapar.

    Args:
        query (str): Arama sorgusu (örneğin: 'Gatsby', 'Harper Lee')

    Returns:
        Dict containing:
        - results (List[Dict]): list of book entries, each containing 'title' and 'authors' fields
          where 'authors' is a List[str]
        - found_books_count (int): number of books found in the search
        - error_message (str): message indicating no books were found or other search-related issues,
          present when results are empty

    Example:
        {
            "results": [
                {
                    "title": "The Great Gatsby",
                    "authors": ["F. Scott Fitzgerald"]
                },
                {
                    "title": "To Kill a Mockingbird",
                    "authors": ["Harper Lee"]
                }
            ],
            "found_books_count": 2,
            "error_message": ""
        }
    """
    # Input validation
    if not query or not query.strip():
        return {
            "results": [],
            "found_books_count": 0,
            "error_message": "Query parameter is required and cannot be empty"
        }

    # Call external API simulation
    api_data = call_external_api("book-mcp-server-search_books_tool")

    # Extract and construct results list
    results: List[Dict[str, Any]] = []
    
    # Process first book
    if api_data.get("result_0_title"):
        authors_0 = []
        if api_data.get("result_0_authors_0"):
            authors_0.append(api_data["result_0_authors_0"])
        if api_data.get("result_0_authors_1"):
            authors_0.append(api_data["result_0_authors_1"])
        
        results.append({
            "title": api_data["result_0_title"],
            "authors": authors_0
        })

    # Process second book
    if api_data.get("result_1_title"):
        authors_1 = []
        if api_data.get("result_1_authors_0"):
            authors_1.append(api_data["result_1_authors_0"])
        if api_data.get("result_1_authors_1"):
            authors_1.append(api_data["result_1_authors_1"])
        
        results.append({
            "title": api_data["result_1_title"],
            "authors": authors_1
        })

    # Construct final response
    found_books_count = api_data.get("found_books_count", 0)
    error_message: Optional[str] = api_data.get("error_message", "")

    # If no books found, ensure error message is set
    if found_books_count == 0 and not error_message:
        error_message = "No books found matching the query"

    return {
        "results": results,
        "found_books_count": found_books_count,
        "error_message": error_message if error_message else ""
    }