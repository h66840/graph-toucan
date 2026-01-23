from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external TabNews API for comments.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - comment_0_id (str): ID of the first comment
        - comment_0_username (str): Author username of the first comment
        - comment_0_body (str): Body text of the first comment
        - comment_0_upvotes (int): Upvote count for the first comment
        - comment_0_downvotes (int): Downvote count for the first comment
        - comment_0_published_at (str): Publication timestamp of the first comment (ISO format)
        - comment_0_updated_at (str): Update timestamp of the first comment (ISO format, optional)
        - comment_0_reply_to_comment_id (str): Parent comment ID for the first comment (nullable)
        - comment_1_id (str): ID of the second comment
        - comment_1_username (str): Author username of the second comment
        - comment_1_body (str): Body text of the second comment
        - comment_1_upvotes (int): Upvote count for the second comment
        - comment_1_downvotes (int): Downvote count for the second comment
        - comment_1_published_at (str): Publication timestamp of the second comment (ISO format)
        - comment_1_updated_at (str): Update timestamp of the second comment (ISO format, optional)
        - comment_1_reply_to_comment_id (str): Parent comment ID for the second comment (nullable)
        - comment_0_child_0_id (str): ID of the first nested reply in the first comment
        - comment_0_child_0_username (str): Author username of the first nested reply
        - comment_0_child_0_body (str): Body text of the first nested reply
        - comment_0_child_0_upvotes (int): Upvotes for the first nested reply
        - comment_0_child_0_downvotes (int): Downvotes for the first nested reply
        - comment_0_child_0_published_at (str): Publication timestamp of the first nested reply (ISO format)
        - comment_0_child_0_updated_at (str): Update timestamp of the first nested reply (ISO format, optional)
        - comment_0_child_0_reply_to_comment_id (str): Parent comment ID for the first nested reply
        - comment_0_child_1_id (str): ID of the second nested reply in the first comment
        - comment_0_child_1_username (str): Author username of the second nested reply
        - comment_0_child_1_body (str): Body text of the second nested reply
        - comment_0_child_1_upvotes (int): Upvotes for the second nested reply
        - comment_0_child_1_downvotes (int): Downvotes for the second nested reply
        - comment_0_child_1_published_at (str): Publication timestamp of the second nested reply (ISO format)
        - comment_0_child_1_updated_at (str): Update timestamp of the second nested reply (ISO format, optional)
        - comment_0_child_1_reply_to_comment_id (str): Parent comment ID for the second nested reply
        - total_count (int): Total number of comments including nested replies
        - has_more (bool): Whether more pages of comments are available
        - metadata_retrieved_at (str): Timestamp when data was retrieved (ISO format)
        - metadata_content_slug (str): Slug of the content being commented on
        - metadata_content_owner (str): Owner username of the content
        - metadata_sort_method (str): Sorting method used for comments (e.g., 'newest', 'top')
    """
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "comment_0_id": "c1",
        "comment_0_username": "alice",
        "comment_0_body": "Great post! Very informative.",
        "comment_0_upvotes": 5,
        "comment_0_downvotes": 0,
        "comment_0_published_at": "2024-01-01T10:00:00Z",
        "comment_0_updated_at": None,
        "comment_0_reply_to_comment_id": None,
        "comment_1_id": "c2",
        "comment_1_username": "bob",
        "comment_1_body": "I have a different opinion on this.",
        "comment_1_upvotes": 2,
        "comment_1_downvotes": 1,
        "comment_1_published_at": "2024-01-01T11:00:00Z",
        "comment_1_updated_at": "2024-01-01T11:30:00Z",
        "comment_1_reply_to_comment_id": None,
        "comment_0_child_0_id": "c1r1",
        "comment_0_child_0_username": "charlie",
        "comment_0_child_0_body": "I agree with alice.",
        "comment_0_child_0_upvotes": 3,
        "comment_0_child_0_downvotes": 0,
        "comment_0_child_0_published_at": "2024-01-01T10:15:00Z",
        "comment_0_child_0_updated_at": None,
        "comment_0_child_0_reply_to_comment_id": "c1",
        "comment_0_child_1_id": "c1r2",
        "comment_0_child_1_username": "diana",
        "comment_0_child_1_body": "Thanks for sharing!",
        "comment_0_child_1_upvotes": 1,
        "comment_0_child_1_downvotes": 0,
        "comment_0_child_1_published_at": "2024-01-01T10:20:00Z",
        "comment_0_child_1_updated_at": None,
        "comment_0_child_1_reply_to_comment_id": "c1",
        "total_count": 4,
        "has_more": True,
        "metadata_retrieved_at": now,
        "metadata_content_slug": "how-to-learn-python",
        "metadata_content_owner": "john_doe",
        "metadata_sort_method": "newest"
    }

def tabnews_integration_get_comments(slug: str, username: str) -> Dict[str, Any]:
    """
    Fetch comments from a content on TabNews API based on slug and username.
    
    Args:
        slug (str): The slug to get the content
        username (str): The username to get the content
    
    Returns:
        Dict containing:
        - comments (List[Dict]): List of comment objects with nested replies
        - total_count (int): Total number of comments retrieved
        - has_more (bool): Whether additional pages are available
        - metadata (Dict): Contextual information about the response
    
    Each comment dict contains:
        - id (str)
        - username (str)
        - body (str)
        - upvotes (int)
        - downvotes (int)
        - published_at (str, ISO datetime)
        - updated_at (str, ISO datetime, optional)
        - reply_to_comment_id (str, nullable)
        - children (List[Dict], recursive structure for nested replies)
    
    Metadata contains:
        - retrieved_at (str, ISO datetime)
        - content_slug (str)
        - content_owner (str)
        - sort_method (str)
    """
    if not slug:
        raise ValueError("slug is required")
    if not username:
        raise ValueError("username is required")
    
    # Call external API to get flattened data
    api_data = call_external_api("tabnews-integration-get comments")
    
    # Construct nested children for first comment
    children_0 = [
        {
            "id": api_data["comment_0_child_0_id"],
            "username": api_data["comment_0_child_0_username"],
            "body": api_data["comment_0_child_0_body"],
            "upvotes": api_data["comment_0_child_0_upvotes"],
            "downvotes": api_data["comment_0_child_0_downvotes"],
            "published_at": api_data["comment_0_child_0_published_at"],
            "updated_at": api_data["comment_0_child_0_updated_at"],
            "reply_to_comment_id": api_data["comment_0_child_0_reply_to_comment_id"],
            "children": []
        },
        {
            "id": api_data["comment_0_child_1_id"],
            "username": api_data["comment_0_child_1_username"],
            "body": api_data["comment_0_child_1_body"],
            "upvotes": api_data["comment_0_child_1_upvotes"],
            "downvotes": api_data["comment_0_child_1_downvotes"],
            "published_at": api_data["comment_0_child_1_published_at"],
            "updated_at": api_data["comment_0_child_1_updated_at"],
            "reply_to_comment_id": api_data["comment_0_child_1_reply_to_comment_id"],
            "children": []
        }
    ]
    
    # Construct comments list
    comments = [
        {
            "id": api_data["comment_0_id"],
            "username": api_data["comment_0_username"],
            "body": api_data["comment_0_body"],
            "upvotes": api_data["comment_0_upvotes"],
            "downvotes": api_data["comment_0_downvotes"],
            "published_at": api_data["comment_0_published_at"],
            "updated_at": api_data["comment_0_updated_at"],
            "reply_to_comment_id": api_data["comment_0_reply_to_comment_id"],
            "children": children_0
        },
        {
            "id": api_data["comment_1_id"],
            "username": api_data["comment_1_username"],
            "body": api_data["comment_1_body"],
            "upvotes": api_data["comment_1_upvotes"],
            "downvotes": api_data["comment_1_downvotes"],
            "published_at": api_data["comment_1_published_at"],
            "updated_at": api_data["comment_1_updated_at"],
            "reply_to_comment_id": api_data["comment_1_reply_to_comment_id"],
            "children": []
        }
    ]
    
    # Construct metadata
    metadata = {
        "retrieved_at": api_data["metadata_retrieved_at"],
        "content_slug": api_data["metadata_content_slug"],
        "content_owner": api_data["metadata_content_owner"],
        "sort_method": api_data["metadata_sort_method"]
    }
    
    return {
        "comments": comments,
        "total_count": api_data["total_count"],
        "has_more": api_data["has_more"],
        "metadata": metadata
    }