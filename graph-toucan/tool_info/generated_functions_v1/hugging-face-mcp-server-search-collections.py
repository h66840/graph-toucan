from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face collections search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first matching collection
        - result_0_title (str): Title of the first collection
        - result_0_description (str): Description of the first collection
        - result_0_owner (str): Owner of the first collection
        - result_0_item_type (str): Item type of the first collection
        - result_0_created_at (str): Creation timestamp of the first collection
        - result_0_last_updated (str): Last update timestamp of the first collection
        - result_0_url (str): URL of the first collection
        - result_1_id (str): ID of the second matching collection
        - result_1_title (str): Title of the second collection
        - result_1_description (str): Description of the second collection
        - result_1_owner (str): Owner of the second collection
        - result_1_item_type (str): Item type of the second collection
        - result_1_created_at (str): Creation timestamp of the second collection
        - result_1_last_updated (str): Last update timestamp of the second collection
        - result_1_url (str): URL of the second collection
        - total_count (int): Total number of collections matching the query
        - limit (int): Maximum number of results returned
        - page_info_offset (int): Pagination offset
        - page_info_next_cursor (str): Cursor for next page
        - page_info_previous_cursor (str): Cursor for previous page
        - query_used (str): Search term used in the query
        - filters_applied_owner (str): Owner filter applied, if any
        - filters_applied_item (str): Item filter applied, if any
        - success (bool): Whether the operation was successful
        - error_message (str): Error message if success is False
    """
    return {
        "result_0_id": "collections/alice/nlp-papers-2023",
        "result_0_title": "NLP Research Papers 2023",
        "result_0_description": "A curated collection of NLP research papers from 2023.",
        "result_0_owner": "alice",
        "result_0_item_type": "paper",
        "result_0_created_at": "2023-01-15T08:00:00Z",
        "result_0_last_updated": "2023-12-01T12:30:00Z",
        "result_0_url": "https://huggingface.co/collections/alice/nlp-papers-2023",
        "result_1_id": "collections/bob/llm-benchmarks",
        "result_1_title": "LLM Benchmark Results",
        "result_1_description": "Benchmark results for various LLMs across multiple tasks.",
        "result_1_owner": "bob",
        "result_1_item_type": "model",
        "result_1_created_at": "2023-03-22T10:15:00Z",
        "result_1_last_updated": "2023-11-10T14:45:00Z",
        "result_1_url": "https://huggingface.co/collections/bob/llm-benchmarks",
        "total_count": 2,
        "limit": 2,
        "page_info_offset": 0,
        "page_info_next_cursor": "",
        "page_info_previous_cursor": "",
        "query_used": "llm",
        "filters_applied_owner": "bob",
        "filters_applied_item": "models/teknium/OpenHermes-2.5-Mistral-7B",
        "success": True,
        "error_message": ""
    }

def hugging_face_mcp_server_search_collections(
    item: Optional[str] = None,
    limit: Optional[int] = None,
    owner: Optional[str] = None,
    query: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for collections on Hugging Face Hub based on provided criteria.
    
    Args:
        item (Optional[str]): Filter by item (e.g., 'models/teknium/OpenHermes-2.5-Mistral-7B')
        limit (Optional[int]): Maximum number of results to return
        owner (Optional[str]): Filter by owner
        query (Optional[str]): Search term for titles and descriptions
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of collection objects with fields 'id', 'title', 'description',
          'owner', 'item_type', 'created_at', 'last_updated', and 'url'
        - total_count (int): Total number of matching collections
        - limit (int): Number of results returned
        - page_info (Dict): Pagination metadata with 'offset', 'next_cursor', 'previous_cursor'
        - query_used (str): The search term used
        - filters_applied (Dict): Filters that were applied during search
        - success (bool): Whether the operation succeeded
        - error_message (str): Error message if operation failed
    """
    try:
        # Validate inputs
        if limit is not None and (not isinstance(limit, int) or limit <= 0):
            return {
                "results": [],
                "total_count": 0,
                "limit": 0,
                "page_info": {"offset": 0, "next_cursor": "", "previous_cursor": ""},
                "query_used": query or "",
                "filters_applied": {"owner": owner, "item": item},
                "success": False,
                "error_message": "Limit must be a positive integer."
            }

        # Call simulated external API
        api_data = call_external_api("hugging-face-mcp-server-search-collections")
        
        # Construct results list from flattened API response
        results = [
            {
                "id": api_data["result_0_id"],
                "title": api_data["result_0_title"],
                "description": api_data["result_0_description"],
                "owner": api_data["result_0_owner"],
                "item_type": api_data["result_0_item_type"],
                "created_at": api_data["result_0_created_at"],
                "last_updated": api_data["result_0_last_updated"],
                "url": api_data["result_0_url"]
            },
            {
                "id": api_data["result_1_id"],
                "title": api_data["result_1_title"],
                "description": api_data["result_1_description"],
                "owner": api_data["result_1_owner"],
                "item_type": api_data["result_1_item_type"],
                "created_at": api_data["result_1_created_at"],
                "last_updated": api_data["result_1_last_updated"],
                "url": api_data["result_1_url"]
            }
        ]
        
        # Apply limit if specified
        final_limit = limit if limit is not None else api_data["limit"]
        results = results[:final_limit]
        
        # Construct final response
        response = {
            "results": results,
            "total_count": api_data["total_count"],
            "limit": final_limit,
            "page_info": {
                "offset": api_data["page_info_offset"],
                "next_cursor": api_data["page_info_next_cursor"],
                "previous_cursor": api_data["page_info_previous_cursor"]
            },
            "query_used": api_data["query_used"],
            "filters_applied": {
                "owner": api_data["filters_applied_owner"],
                "item": api_data["filters_applied_item"]
            },
            "success": api_data["success"]
        }
        
        # Add error message only if not successful
        if not api_data["success"]:
            response["error_message"] = api_data["error_message"]
            
        return response
        
    except Exception as e:
        return {
            "results": [],
            "total_count": 0,
            "limit": 0,
            "page_info": {"offset": 0, "next_cursor": "", "previous_cursor": ""},
            "query_used": query or "",
            "filters_applied": {"owner": owner, "item": item},
            "success": False,
            "error_message": str(e)
        }