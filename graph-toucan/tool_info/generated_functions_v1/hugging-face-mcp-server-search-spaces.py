from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face Spaces search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first result
        - result_0_author (str): Author of the first result
        - result_0_name (str): Name of the first result
        - result_0_sdk (str): SDK used in the first result
        - result_0_title (str): Title of the first result
        - result_0_last_updated (str): Last updated timestamp (ISO format) of the first result
        - result_0_url (str): URL of the first result
        - result_0_tag_0 (str): First tag of the first result
        - result_0_tag_1 (str): Second tag of the first result
        - result_0_card_data_title (str): Card data title of the first result
        - result_0_card_data_description (str): Card data description of the first result
        - result_1_id (str): ID of the second result
        - result_1_author (str): Author of the second result
        - result_1_name (str): Name of the second result
        - result_1_sdk (str): SDK used in the second result
        - result_1_title (str): Title of the second result
        - result_1_last_updated (str): Last updated timestamp (ISO format) of the second result
        - result_1_url (str): URL of the second result
        - result_1_tag_0 (str): First tag of the second result
        - result_1_tag_1 (str): Second tag of the second result
        - result_1_card_data_title (str): Card data title of the second result
        - result_1_card_data_description (str): Card data description of the second result
        - total_count (int): Total number of matching spaces
        - has_more (bool): Whether more results exist beyond limit
        - query_used (str): The actual query string used
        - filter_applied_author (str): Author filter applied, if any
        - filter_applied_sdk (str): SDK filter applied, if any
        - filter_applied_tags (str): Tags filter applied, if any
        - limit (int): Maximum number of results returned
    """
    return {
        "result_0_id": "user1/space-one",
        "result_0_author": "user1",
        "result_0_name": "space-one",
        "result_0_sdk": "gradio",
        "result_0_title": "Text to Image Generator",
        "result_0_last_updated": "2023-10-05T14:48:00Z",
        "result_0_url": "https://huggingface.co/spaces/user1/space-one",
        "result_0_tag_0": "text-to-image",
        "result_0_tag_1": "generation",
        "result_0_card_data_title": "Text to Image Generator",
        "result_0_card_data_description": "A Gradio app that generates images from text prompts.",
        
        "result_1_id": "org2/translator-app",
        "result_1_author": "org2",
        "result_1_name": "translator-app",
        "result_1_sdk": "streamlit",
        "result_1_title": "Language Translator",
        "result_1_last_updated": "2023-09-28T09:15:30Z",
        "result_1_url": "https://huggingface.co/spaces/org2/translator-app",
        "result_1_tag_0": "translation",
        "result_1_tag_1": "nlp",
        "result_1_card_data_title": "Language Translator App",
        "result_1_card_data_description": "Translate text between multiple languages using deep learning models.",
        
        "total_count": 42,
        "has_more": True,
        "query_used": "translate",
        "filter_applied_author": "org2",
        "filter_applied_sdk": "streamlit",
        "filter_applied_tags": "nlp",
        "limit": 2
    }

def hugging_face_mcp_server_search_spaces(
    author: Optional[str] = None,
    limit: Optional[int] = None,
    query: Optional[str] = None,
    sdk: Optional[str] = None,
    tags: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for Spaces on Hugging Face Hub based on provided filters.
    
    Args:
        author (Optional[str]): Filter by author/organization
        limit (Optional[int]): Maximum number of results to return
        query (Optional[str]): Search term
        sdk (Optional[str]): Filter by SDK (e.g., 'streamlit', 'gradio', 'docker')
        tags (Optional[str]): Filter by tags
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of space objects with fields: id, author, name, sdk, tags, 
          title, last_updated, card_data, url
        - total_count (int): Total number of spaces matching the query
        - has_more (bool): Whether more results exist beyond current limit
        - query_used (str): The actual search query applied
        - filters_applied (Dict): Summary of filters applied (author, sdk, tags)
        - limit (int): Maximum number of results returned
    
    Raises:
        ValueError: If limit is negative
    """
    if limit is not None and limit < 0:
        raise ValueError("Limit cannot be negative")
    
    # Call the simulated external API
    api_data = call_external_api("hugging-face-mcp-server-search-spaces")
    
    # Construct results list from flattened API data
    results = []
    
    # Process first result
    result_0_tags = [
        api_data["result_0_tag_0"],
        api_data["result_0_tag_1"]
    ]
    result_0_card_data = {
        "title": api_data["result_0_card_data_title"],
        "description": api_data["result_0_card_data_description"]
    }
    results.append({
        "id": api_data["result_0_id"],
        "author": api_data["result_0_author"],
        "name": api_data["result_0_name"],
        "sdk": api_data["result_0_sdk"],
        "tags": result_0_tags,
        "title": api_data["result_0_title"],
        "last_updated": api_data["result_0_last_updated"],
        "card_data": result_0_card_data,
        "url": api_data["result_0_url"]
    })
    
    # Process second result
    result_1_tags = [
        api_data["result_1_tag_0"],
        api_data["result_1_tag_1"]
    ]
    result_1_card_data = {
        "title": api_data["result_1_card_data_title"],
        "description": api_data["result_1_card_data_description"]
    }
    results.append({
        "id": api_data["result_1_id"],
        "author": api_data["result_1_author"],
        "name": api_data["result_1_name"],
        "sdk": api_data["result_1_sdk"],
        "tags": result_1_tags,
        "title": api_data["result_1_title"],
        "last_updated": api_data["result_1_last_updated"],
        "card_data": result_1_card_data,
        "url": api_data["result_1_url"]
    })
    
    # Apply limit if specified
    final_limit = limit if limit is not None else 100
    limited_results = results[:final_limit]
    
    # Build filters_applied dict
    filters_applied = {}
    if author:
        filters_applied["author"] = author
    if sdk:
        filters_applied["sdk"] = sdk
    if tags:
        filters_applied["tags"] = tags
    
    # Construct final response
    response = {
        "results": limited_results,
        "total_count": api_data["total_count"],
        "has_more": api_data["has_more"],
        "query_used": api_data["query_used"],
        "filters_applied": filters_applied,
        "limit": final_limit
    }
    
    return response