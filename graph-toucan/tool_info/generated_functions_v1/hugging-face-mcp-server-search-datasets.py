from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching dataset search results from Hugging Face Hub API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (str): ID of the first dataset result
        - result_0_name (str): Name of the first dataset
        - result_0_author (str): Author of the first dataset
        - result_0_tags (str): Tags of the first dataset as comma-separated string
        - result_0_downloads (int): Download count for the first dataset
        - result_0_likes (int): Like count for the first dataset
        - result_0_lastModified (str): Last modified timestamp of the first dataset (ISO format)
        - result_1_id (str): ID of the second dataset result
        - result_1_name (str): Name of the second dataset
        - result_1_author (str): Author of the second dataset
        - result_1_tags (str): Tags of the second dataset as comma-separated string
        - result_1_downloads (int): Download count for the second dataset
        - result_1_likes (int): Like count for the second dataset
        - result_1_lastModified (str): Last modified timestamp of the second dataset (ISO format)
    """
    return {
        "result_0_id": "dataset_123",
        "result_0_name": "Common Voice",
        "result_0_author": "mozilla",
        "result_0_tags": "audio,speech,voice",
        "result_0_downloads": 150000,
        "result_0_likes": 250,
        "result_0_lastModified": "2023-10-05T14:48:00Z",
        "result_1_id": "dataset_456",
        "result_1_name": "SQuAD",
        "result_1_author": "allenai",
        "result_1_tags": "question-answering,qa,reading-comprehension",
        "result_1_downloads": 200000,
        "result_1_likes": 400,
        "result_1_lastModified": "2023-09-20T08:30:00Z"
    }

def hugging_face_mcp_server_search_datasets(
    author: Optional[str] = None,
    limit: Optional[int] = None,
    query: Optional[str] = None,
    tags: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for datasets on Hugging Face Hub based on provided filters.
    
    Args:
        author (Optional[str]): Filter by author/organization name
        limit (Optional[int]): Maximum number of results to return (default: 2)
        query (Optional[str]): Search term to match in dataset names or descriptions
        tags (Optional[str]): Filter by tags (comma-separated string)
    
    Returns:
        Dict containing a list of dataset objects with the following fields:
        - results (List[Dict]): List of dataset dictionaries, each containing:
            - id (str): Dataset identifier
            - name (str): Dataset name
            - author (str): Dataset author/organization
            - tags (List[str]): List of tags associated with the dataset
            - downloads (int): Number of downloads
            - likes (int): Number of likes
            - lastModified (str): Last modified timestamp in ISO format
    
    Note:
        This is a simulation function that returns mock data structured to match
        the expected output schema. In a real implementation, this would make
        actual API calls to Hugging Face Hub.
    """
    # Validate inputs
    if limit is not None and (not isinstance(limit, int) or limit <= 0):
        raise ValueError("limit must be a positive integer")
    
    # Get simulated API response
    api_data = call_external_api("hugging-face-mcp-server-search-datasets")
    
    # Construct results list from flattened API data
    results = []
    
    # Process first result
    if "result_0_id" in api_data:
        result_0 = {
            "id": api_data["result_0_id"],
            "name": api_data["result_0_name"],
            "author": api_data["result_0_author"],
            "tags": api_data["result_0_tags"].split(",") if api_data["result_0_tags"] else [],
            "downloads": api_data["result_0_downloads"],
            "likes": api_data["result_0_likes"],
            "lastModified": api_data["result_0_lastModified"]
        }
        results.append(result_0)
    
    # Process second result
    if "result_1_id" in api_data:
        result_1 = {
            "id": api_data["result_1_id"],
            "name": api_data["result_1_name"],
            "author": api_data["result_1_author"],
            "tags": api_data["result_1_tags"].split(",") if api_data["result_1_tags"] else [],
            "downloads": api_data["result_1_downloads"],
            "likes": api_data["result_1_likes"],
            "lastModified": api_data["result_1_lastModified"]
        }
        results.append(result_1)
    
    # Apply limit if specified
    if limit is not None:
        results = results[:limit]
    
    # Apply author filter if specified
    if author is not None:
        results = [r for r in results if author.lower() in r["author"].lower()]
    
    # Apply tags filter if specified
    if tags is not None:
        tag_list = [tag.strip().lower() for tag in tags.split(",")]
        results = [r for r in results if any(t in [rt.lower() for rt in r["tags"]] for t in tag_list)]
    
    # Apply query filter if specified
    if query is not None:
        query_lower = query.lower()
        results = [r for r in results if 
                  query_lower in r["name"].lower() or 
                  query_lower in r["id"].lower()]
    
    return {"results": results}