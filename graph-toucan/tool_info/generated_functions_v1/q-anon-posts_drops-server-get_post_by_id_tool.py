from typing import Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for retrieving a post by ID.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - post_id (int): The ID of the post
        - post_content (str): The content/text of the post
        - post_author (str): The author of the post
        - post_timestamp (str): The timestamp when the post was created
        - post_metadata_title (str): Title of the post
        - post_metadata_likes (int): Number of likes on the post
        - post_metadata_shares (int): Number of shares of the post
        - found (bool): Whether the post was found
        - error_message (str): Error message if any occurred; null if successful
    """
    return {
        "post_id": 12345,
        "post_content": "This is a sample anonymous post about technology trends in 2025.",
        "post_author": "anon_user_789",
        "post_timestamp": "2025-04-05T10:30:00Z",
        "post_metadata_title": "Future of AI",
        "post_metadata_likes": 150,
        "post_metadata_shares": 45,
        "found": True,
        "error_message": None
    }

def q_anon_posts_drops_server_get_post_by_id_tool(post_id: int) -> Dict[str, Any]:
    """
    Retrieve a specific post by its ID.
    
    Args:
        post_id (int): The ID of the post to retrieve
    
    Returns:
        Dict containing:
        - post (Dict): Contains detailed information about the retrieved post,
          including id, content, author, timestamp, and other metadata
        - found (bool): Indicates whether a post with the given ID was successfully retrieved
        - error_message (str or None): Describes any error that occurred during retrieval;
          None if successful
    """
    if not isinstance(post_id, int) or post_id <= 0:
        return {
            "post": None,
            "found": False,
            "error_message": "Invalid post_id: must be a positive integer."
        }
    
    api_data = call_external_api("q-anon-posts/drops-server-get_post_by_id_tool")
    
    # Construct the nested post object from flattened API data
    post = {
        "id": api_data["post_id"],
        "content": api_data["post_content"],
        "author": api_data["post_author"],
        "timestamp": api_data["post_timestamp"],
        "metadata": {
            "title": api_data["post_metadata_title"],
            "likes": api_data["post_metadata_likes"],
            "shares": api_data["post_metadata_shares"]
        }
    } if api_data["found"] else None
    
    return {
        "post": post,
        "found": api_data["found"],
        "error_message": api_data["error_message"]
    }