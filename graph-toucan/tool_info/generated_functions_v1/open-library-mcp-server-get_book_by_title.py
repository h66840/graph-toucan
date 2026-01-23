from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Open Library book search by title.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first book result
        - result_0_authors (str): Authors of the first book (comma-separated)
        - result_0_first_publish_year (int): First publish year of the first book
        - result_0_open_library_work_key (str): Open Library work key of the first book
        - result_0_edition_count (int): Number of editions for the first book
        - result_0_cover_url (str): Cover URL of the first book
        - result_1_title (str): Title of the second book result
        - result_1_authors (str): Authors of the second book (comma-separated)
        - result_1_first_publish_year (int): First publish year of the second book
        - result_1_open_library_work_key (str): Open Library work key of the second book
        - result_1_edition_count (int): Number of editions for the second book
        - result_1_cover_url (str): Cover URL of the second book
        - error_message (str): Error message if any, otherwise empty string
    """
    return {
        "result_0_title": "The Great Gatsby",
        "result_0_authors": "F. Scott Fitzgerald",
        "result_0_first_publish_year": 1925,
        "result_0_open_library_work_key": "OL123456W",
        "result_0_edition_count": 150,
        "result_0_cover_url": "https://covers.openlibrary.org/w/id/123456-M.jpg",
        "result_1_title": "The Great Gatsby: A Novel",
        "result_1_authors": "F. Scott Fitzgerald",
        "result_1_first_publish_year": 1926,
        "result_1_open_library_work_key": "OL789012W",
        "result_1_edition_count": 89,
        "result_1_cover_url": "https://covers.openlibrary.org/w/id/789012-M.jpg",
        "error_message": ""
    }

def open_library_mcp_server_get_book_by_title(title: str) -> Dict[str, Any]:
    """
    Search for a book by its title on Open Library.
    
    Args:
        title (str): The title of the book to search for.
        
    Returns:
        Dict containing:
        - results (List[Dict]): List of book entries with 'title', 'authors', 'first_publish_year',
          'open_library_work_key', 'edition_count', and optionally 'cover_url' fields
        - error_message (str): Description of the error when no books are found or another issue occurs
    """
    if not title or not title.strip():
        return {
            "results": [],
            "error_message": "Title parameter is required and cannot be empty"
        }
    
    # Call the external API simulation
    api_data = call_external_api("open-library-mcp-server-get_book_by_title")
    
    # Extract error message
    error_message = api_data.get("error_message", "")
    
    # Construct results list from indexed fields
    results: List[Dict[str, Any]] = []
    
    # Process first result
    if "result_0_title" in api_data and api_data["result_0_title"]:
        result_0 = {
            "title": api_data["result_0_title"],
            "authors": api_data["result_0_authors"],
            "first_publish_year": api_data["result_0_first_publish_year"],
            "open_library_work_key": api_data["result_0_open_library_work_key"],
            "edition_count": api_data["result_0_edition_count"]
        }
        # Add cover_url only if it exists and is not empty
        if api_data.get("result_0_cover_url"):
            result_0["cover_url"] = api_data["result_0_cover_url"]
        results.append(result_0)
    
    # Process second result
    if "result_1_title" in api_data and api_data["result_1_title"]:
        result_1 = {
            "title": api_data["result_1_title"],
            "authors": api_data["result_1_authors"],
            "first_publish_year": api_data["result_1_first_publish_year"],
            "open_library_work_key": api_data["result_1_open_library_work_key"],
            "edition_count": api_data["result_1_edition_count"]
        }
        # Add cover_url only if it exists and is not empty
        if api_data.get("result_1_cover_url"):
            result_1["cover_url"] = api_data["result_1_cover_url"]
        results.append(result_1)
    
    # If there was an error message but we have results, we still return results
    # according to typical API behavior where error might be a warning
    return {
        "results": results,
        "error_message": error_message
    }