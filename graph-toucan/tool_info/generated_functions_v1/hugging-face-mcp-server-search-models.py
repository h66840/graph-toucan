from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Hugging Face model search.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first model result
        - result_0_name (str): Name of the first model
        - result_0_author (str): Author of the first model
        - result_0_downloads (int): Download count of the first model
        - result_0_likes (int): Like count of the first model
        - result_0_lastModified (str): Last modified timestamp of the first model
        - result_0_tags_0 (str): First tag of the first model
        - result_0_tags_1 (str): Second tag of the first model
        - result_1_id (str): ID of the second model result
        - result_1_name (str): Name of the second model
        - result_1_author (str): Author of the second model
        - result_1_downloads (int): Download count of the second model
        - result_1_likes (int): Like count of the second model
        - result_1_lastModified (str): Last modified timestamp of the second model
        - result_1_tags_0 (str): First tag of the second model
        - result_1_tags_1 (str): Second tag of the second model
    """
    return {
        "result_0_id": "bert-base-uncased",
        "result_0_name": "BERT Base Uncased",
        "result_0_author": "huggingface",
        "result_0_downloads": 1500000,
        "result_0_likes": 12000,
        "result_0_lastModified": "2023-05-15T10:30:00Z",
        "result_0_tags_0": "fill-mask",
        "result_0_tags_1": "en",
        "result_1_id": "gpt2",
        "result_1_name": "GPT-2",
        "result_1_author": "openai",
        "result_1_downloads": 2000000,
        "result_1_likes": 18000,
        "result_1_lastModified": "2023-04-20T14:20:00Z",
        "result_1_tags_0": "text-generation",
        "result_1_tags_1": "en"
    }

def hugging_face_mcp_server_search_models(
    author: Optional[str] = None,
    limit: Optional[int] = None,
    query: Optional[str] = None,
    tags: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for models on Hugging Face Hub based on given criteria.
    
    Args:
        author (Optional[str]): Filter by author/organization (e.g., 'huggingface', 'google')
        limit (Optional[int]): Maximum number of results to return
        query (Optional[str]): Search term (e.g., 'bert', 'gpt')
        tags (Optional[str]): Filter by tags (e.g., 'text-classification', 'translation')
    
    Returns:
        Dict containing a list of model objects with fields:
        - id (str): Model identifier
        - name (str): Model name
        - author (str): Model author/organization
        - tags (List[str]): List of tags associated with the model
        - downloads (int): Number of downloads
        - likes (int): Number of likes
        - lastModified (str): ISO format timestamp of last modification
    
    Note:
        This is a simulation that returns mock data structured to match the expected schema.
        In a real implementation, this would query the Hugging Face Hub API.
    """
    # Validate inputs
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("limit must be a positive integer")
    
    # Get simulated API data
    api_data = call_external_api("hugging-face-mcp-server-search-models")
    
    # Construct results list from flattened API response
    results = []
    
    # Process first result
    result_0_tags = []
    if "result_0_tags_0" in api_data and api_data["result_0_tags_0"]:
        result_0_tags.append(api_data["result_0_tags_0"])
    if "result_0_tags_1" in api_data and api_data["result_0_tags_1"]:
        result_0_tags.append(api_data["result_0_tags_1"])
    
    model_0 = {
        "id": api_data["result_0_id"],
        "name": api_data["result_0_name"],
        "author": api_data["result_0_author"],
        "tags": result_0_tags,
        "downloads": api_data["result_0_downloads"],
        "likes": api_data["result_0_likes"],
        "lastModified": api_data["result_0_lastModified"]
    }
    
    # Apply filters
    include_0 = True
    if author and author.lower() not in model_0["author"].lower():
        include_0 = False
    if query and query.lower() not in model_0["name"].lower() and query.lower() not in model_0["id"].lower():
        include_0 = False
    if tags and not any(tag.lower() == tags.lower() for tag in model_0["tags"]):
        include_0 = False
    
    if include_0:
        results.append(model_0)
    
    # Process second result
    result_1_tags = []
    if "result_1_tags_0" in api_data and api_data["result_1_tags_0"]:
        result_1_tags.append(api_data["result_1_tags_0"])
    if "result_1_tags_1" in api_data and api_data["result_1_tags_1"]:
        result_1_tags.append(api_data["result_1_tags_1"])
    
    model_1 = {
        "id": api_data["result_1_id"],
        "name": api_data["result_1_name"],
        "author": api_data["result_1_author"],
        "tags": result_1_tags,
        "downloads": api_data["result_1_downloads"],
        "likes": api_data["result_1_likes"],
        "lastModified": api_data["result_1_lastModified"]
    }
    
    # Apply filters
    include_1 = True
    if author and author.lower() not in model_1["author"].lower():
        include_1 = False
    if query and query.lower() not in model_1["name"].lower() and query.lower() not in model_1["id"].lower():
        include_1 = False
    if tags and not any(tag.lower() == tags.lower() for tag in model_1["tags"]):
        include_1 = False
    
    if include_1:
        results.append(model_1)
    
    # Apply limit
    if limit is not None:
        results = results[:limit]
    
    return {"results": results}