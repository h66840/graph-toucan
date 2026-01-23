from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Old School RuneScape objtypes search.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_id (int): ID of the first matching object
        - result_0_value (str): Value/name of the first matching object
        - result_0_line (str): Full line text from objtypes.txt for the first result
        - result_0_lineNumber (int): Line number in the file for the first result
        - result_0_formatted (str): Formatted display string for the first result
        - result_1_id (int): ID of the second matching object
        - result_1_value (str): Value/name of the second matching object
        - result_1_line (str): Full line text from objtypes.txt for the second result
        - result_1_lineNumber (int): Line number in the file for the second result
        - result_1_formatted (str): Formatted display string for the second result
        - pagination_page (int): Current page number
        - pagination_pageSize (int): Number of results per page
        - pagination_totalResults (int): Total number of matching results
        - pagination_totalPages (int): Total number of pages
        - pagination_hasNextPage (bool): Whether there is a next page
        - pagination_hasPreviousPage (bool): Whether there is a previous page
    """
    return {
        "result_0_id": 1234,
        "result_0_value": "Iron dagger",
        "result_0_line": "1234=Iron dagger",
        "result_0_lineNumber": 123,
        "result_0_formatted": "Iron dagger (ID: 1234)",
        "result_1_id": 1235,
        "result_1_value": "Iron dagger(p)",
        "result_1_line": "1235=Iron dagger(p)",
        "result_1_lineNumber": 124,
        "result_1_formatted": "Iron dagger(p) (ID: 1235)",
        "pagination_page": 1,
        "pagination_pageSize": 10,
        "pagination_totalResults": 2,
        "pagination_totalPages": 1,
        "pagination_hasNextPage": False,
        "pagination_hasPreviousPage": False,
    }

def old_school_runescape_wiki_and_data_server_search_objtypes(
    query: str, 
    page: Optional[int] = 1, 
    pageSize: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Search the objtypes.txt file for object/item definitions in Old School RuneScape.

    Args:
        query (str): The term to search for in the objtypes.txt file (required)
        page (int, optional): Page number for pagination (default: 1)
        pageSize (int, optional): Number of results per page (default: 10)

    Returns:
        Dict containing:
        - results (List[Dict]): List of object entries matching the search query,
          each containing 'id', 'value', 'line', 'lineNumber', and 'formatted' fields
        - pagination (Dict): Pagination metadata including 'page', 'pageSize',
          'totalResults', 'totalPages', 'hasNextPage', and 'hasPreviousPage'

    Raises:
        ValueError: If query is empty or None
        TypeError: If page or pageSize are not integers
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty")
    
    if page is not None and not isinstance(page, int):
        raise TypeError("Page must be an integer")
    
    if pageSize is not None and not isinstance(pageSize, int):
        raise TypeError("pageSize must be an integer")
    
    if page is not None and page < 1:
        raise ValueError("Page must be a positive integer")
    
    if pageSize is not None and pageSize < 1:
        raise ValueError("pageSize must be a positive integer")
    
    # Call external API to get data (with only simple fields)
    api_data = call_external_api("old-school-runescape-wiki-and-data-server-search_objtypes")
    
    # Construct results list from flattened API response
    results = [
        {
            "id": api_data["result_0_id"],
            "value": api_data["result_0_value"],
            "line": api_data["result_0_line"],
            "lineNumber": api_data["result_0_lineNumber"],
            "formatted": api_data["result_0_formatted"]
        },
        {
            "id": api_data["result_1_id"],
            "value": api_data["result_1_value"],
            "line": api_data["result_1_line"],
            "lineNumber": api_data["result_1_lineNumber"],
            "formatted": api_data["result_1_formatted"]
        }
    ]
    
    # Construct pagination object from flattened API response
    pagination = {
        "page": api_data["pagination_page"],
        "pageSize": api_data["pagination_pageSize"],
        "totalResults": api_data["pagination_totalResults"],
        "totalPages": api_data["pagination_totalPages"],
        "hasNextPage": api_data["pagination_hasNextPage"],
        "hasPreviousPage": api_data["pagination_hasPreviousPage"]
    }
    
    # Apply pagination if needed (filter results based on page and pageSize)
    start_idx = (page - 1) * pageSize if page else 0
    end_idx = start_idx + pageSize if pageSize else len(results)
    paginated_results = results[start_idx:end_idx]
    
    # Update pagination metadata based on actual slicing
    total_results = len(results)
    total_pages = max(1, (total_results + pageSize - 1) // pageSize) if pageSize else 1
    
    final_pagination = {
        "page": page,
        "pageSize": pageSize,
        "totalResults": total_results,
        "totalPages": total_pages,
        "hasNextPage": page < total_pages if pageSize else False,
        "hasPreviousPage": page > 1
    }
    
    return {
        "results": paginated_results,
        "pagination": final_pagination
    }