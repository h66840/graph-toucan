from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for searching posts/drops.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_post_id (int): ID of the first matching post
        - result_0_author (str): Author name of the first post
        - result_0_author_id (str): Author ID of the first post
        - result_0_tripcode (str): Tripcode of the first post author
        - result_0_source (str): Source board/thread of the first post
        - result_0_date (str): Date string of the first post
        - result_0_text (str): Text content of the first post
        - result_0_referenced_posts_0 (int): First referenced post ID in the first post
        - result_0_referenced_posts_1 (int): Second referenced post ID in the first post
        - result_1_post_id (int): ID of the second matching post
        - result_1_author (str): Author name of the second post
        - result_1_author_id (str): Author ID of the second post
        - result_1_tripcode (str): Tripcode of the second post author
        - result_1_source (str): Source board/thread of the second post
        - result_1_date (str): Date string of the second post
        - result_1_text (str): Text content of the second post
        - result_1_referenced_posts_0 (int): First referenced post ID in the second post
        - result_1_referenced_posts_1 (int): Second referenced post ID in the second post
        - total_matches (int): Total number of posts matching the query
        - displayed_count (int): Number of results shown in the response
    """
    return {
        "result_0_post_id": 1001,
        "result_0_author": "Anonymous",
        "result_0_author_id": "abc123",
        "result_0_tripcode": "!!Secure123",
        "result_0_source": "/b/",
        "result_0_date": "2023-10-05T14:30:00Z",
        "result_0_text": "This is a test post about cats and dogs.",
        "result_0_referenced_posts_0": 999,
        "result_0_referenced_posts_1": 998,
        "result_1_post_id": 1002,
        "result_1_author": "User456",
        "result_1_author_id": "def456",
        "result_1_tripcode": "!!Cool789",
        "result_1_source": "/tech/",
        "result_1_date": "2023-10-05T15:45:00Z",
        "result_1_text": "Discussing AI and machine learning advancements.",
        "result_1_referenced_posts_0": 1000,
        "result_1_referenced_posts_1": 997,
        "total_matches": 25,
        "displayed_count": 2
    }

def q_anon_posts_drops_server_search_posts(query: str, limit: Optional[int] = 10) -> Dict[str, Any]:
    """
    Search for posts/drops containing a specific keyword or phrase.
    
    Args:
        query (str): The keyword or phrase to search for (required)
        limit (int, optional): Maximum number of results to return (default: 10)
    
    Returns:
        Dict containing:
        - results (List[Dict]): list of post objects with fields 'post_id', 'author', 'author_id',
          'tripcode', 'source', 'date', 'text', and optionally 'referenced_posts'
        - total_matches (int): total number of posts matching the query regardless of limit
        - displayed_count (int): number of results actually shown in the response
    
    Raises:
        ValueError: If query is empty or not provided
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if limit is None:
        limit = 10
    elif limit <= 0:
        raise ValueError("Limit must be a positive integer.")
    
    # Fetch simulated external data
    api_data = call_external_api("q-anon-posts/drops-server-search_posts")
    
    # Construct results list from flattened API data
    results: List[Dict[str, Any]] = []
    
    for i in range(2):  # We have two results from the API simulation
        if i >= limit:
            break
            
        post_key = f"result_{i}"
        if f"{post_key}_post_id" not in api_data:
            continue
            
        # Extract referenced posts if available
        referenced_posts = []
        ref_idx = 0
        while f"{post_key}_referenced_posts_{ref_idx}" in api_data:
            referenced_posts.append(api_data[f"{post_key}_referenced_posts_{ref_idx}"])
            ref_idx += 1
        
        post = {
            "post_id": api_data[f"{post_key}_post_id"],
            "author": api_data[f"{post_key}_author"],
            "author_id": api_data[f"{post_key}_author_id"],
            "tripcode": api_data[f"{post_key}_tripcode"],
            "source": api_data[f"{post_key}_source"],
            "date": api_data[f"{post_key}_date"],
            "text": api_data[f"{post_key}_text"]
        }
        
        if referenced_posts:
            post["referenced_posts"] = referenced_posts
            
        results.append(post)
    
    # Return structured response matching output schema
    return {
        "results": results,
        "total_matches": api_data["total_matches"],
        "displayed_count": api_data["displayed_count"]
    }