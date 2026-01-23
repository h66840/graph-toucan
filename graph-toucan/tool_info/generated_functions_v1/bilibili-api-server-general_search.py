from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bilibili search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first search result
        - result_0_url (str): Video URL of the first search result
        - result_0_uploader (str): Uploader name of the first search result
        - result_0_play_count (int): Play count of the first search result
        - result_0_upload_date (str): Upload date of the first search result in YYYY-MM-DD format
        - result_1_title (str): Title of the second search result
        - result_1_url (str): Video URL of the second search result
        - result_1_uploader (str): Uploader name of the second search result
        - result_1_play_count (int): Play count of the second search result
        - result_1_upload_date (str): Upload date of the second search result in YYYY-MM-DD format
        - total_count (int): Total number of search results found
        - page (int): Current page number of the results
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results are available
        - cost_time_api (float): API response time in seconds
        - cost_time_total (float): Total processing time in seconds
        - metadata_keyword (str): Processed search keyword
        - metadata_search_type (str): Type of search performed
        - metadata_backend_id (str): Backend identifier for the search
    """
    return {
        "result_0_title": "How to Learn Python in 2024",
        "result_0_url": "https://www.bilibili.com/video/av123456789",
        "result_0_uploader": "PythonMaster",
        "result_0_play_count": 150000,
        "result_0_upload_date": "2024-01-15",
        "result_1_title": "Advanced Python Tips and Tricks",
        "result_1_url": "https://www.bilibili.com/video/av987654321",
        "result_1_uploader": "CodeWizard",
        "result_1_play_count": 89000,
        "result_1_upload_date": "2024-01-10",
        "total_count": 2345,
        "page": 1,
        "page_size": 20,
        "has_more": True,
        "cost_time_api": 0.234,
        "cost_time_total": 0.312,
        "metadata_keyword": "python tutorial",
        "metadata_search_type": "video",
        "metadata_backend_id": "search_backend_007"
    }

def bilibili_api_server_general_search(keyword: str) -> Dict[str, Any]:
    """
    Search Bilibili API with the given keyword.

    Args:
        keyword (str): Search term to look for on Bilibili

    Returns:
        Dictionary containing the search results from Bilibili with the following structure:
        - results (List[Dict]): List of individual search result items, each containing:
            - title (str)
            - url (str)
            - uploader (str)
            - play_count (int)
            - upload_date (str)
        - total_count (int): Total number of search results found
        - page (int): Current page number
        - page_size (int): Number of results per page
        - has_more (bool): Whether more results are available
        - cost_time (Dict): Performance timing info with keys 'api' and 'total' (in seconds)
        - metadata (Dict): Additional context like processed keyword, search_type, backend_id
    """
    if not keyword or not keyword.strip():
        raise ValueError("Keyword is required and cannot be empty or whitespace only")
    
    keyword = keyword.strip()
    
    # Call external API simulation
    api_data = call_external_api("bilibili-api-server-general_search")
    
    # Construct results list from indexed fields
    results = [
        {
            "title": api_data["result_0_title"],
            "url": api_data["result_0_url"],
            "uploader": api_data["result_0_uploader"],
            "play_count": api_data["result_0_play_count"],
            "upload_date": api_data["result_0_upload_date"]
        },
        {
            "title": api_data["result_1_title"],
            "url": api_data["result_1_url"],
            "uploader": api_data["result_1_uploader"],
            "play_count": api_data["result_1_play_count"],
            "upload_date": api_data["result_1_upload_date"]
        }
    ]
    
    # Construct cost_time dictionary
    cost_time = {
        "api": api_data["cost_time_api"],
        "total": api_data["cost_time_total"]
    }
    
    # Construct metadata dictionary
    metadata = {
        "keyword": api_data["metadata_keyword"],
        "search_type": api_data["metadata_search_type"],
        "backend_id": api_data["metadata_backend_id"]
    }
    
    # Assemble final result
    final_result = {
        "results": results,
        "total_count": api_data["total_count"],
        "page": api_data["page"],
        "page_size": api_data["page_size"],
        "has_more": api_data["has_more"],
        "cost_time": cost_time,
        "metadata": metadata
    }
    
    return final_result