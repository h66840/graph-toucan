from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external TabNews API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): The title of the content
        - body (str): The main content body in markdown format
        - author (str): The username of the user who published the content
        - created_at (str): Timestamp when the content was created, in ISO 8601 format
        - updated_at (str): Timestamp when the content was last updated, in ISO 8601 format
        - slug (str): The unique identifier slug for the content
        - status (str): Current status of the content (e.g., 'published', 'draft')
        - parent_id (str): ID of the parent content if this is a reply, otherwise null
        - is_official (bool): Indicates whether the content is marked as official by the platform
        - tags_0 (str): First tag associated with the content
        - tags_1 (str): Second tag associated with the content
        - metadata_views (int): Number of views for the content
        - metadata_score (int): Engagement score of the content
        - metadata_children_count (int): Number of child replies
    """
    return {
        "title": "Understanding Python Asyncio",
        "body": "# Asyncio Explained\n\nAsyncio is a powerful library for concurrent programming in Python.",
        "author": "python_enthusiast",
        "created_at": "2023-10-05T08:30:00Z",
        "updated_at": "2023-10-05T10:15:00Z",
        "slug": "understanding-python-asyncio",
        "status": "published",
        "parent_id": None,
        "is_official": False,
        "tags_0": "python",
        "tags_1": "asyncio",
        "metadata_views": 1250,
        "metadata_score": 42,
        "metadata_children_count": 8
    }

def tabnews_integration_get_content(slug: str, username: str) -> Dict[str, Any]:
    """
    Retrieve content from TabNews API based on slug and username.
    
    Args:
        slug (str): The slug to get the content
        username (str): The username to get the content
    
    Returns:
        Dict containing the full content with nested structures as per schema:
        - title (str)
        - body (str)
        - author (str)
        - created_at (str)
        - updated_at (str)
        - slug (str)
        - tags (List[str])
        - status (str)
        - metadata (Dict): Contains 'views', 'score', 'children_count'
        - parent_id (str)
        - is_official (bool)
    
    Raises:
        ValueError: If slug or username is empty
    """
    if not slug:
        raise ValueError("slug is required")
    if not username:
        raise ValueError("username is required")
    
    # Call external API to get flat data
    api_data = call_external_api("tabnews-integration-get content")
    
    # Construct nested output structure as per schema
    result = {
        "title": api_data["title"],
        "body": api_data["body"],
        "author": api_data["author"],
        "created_at": api_data["created_at"],
        "updated_at": api_data["updated_at"],
        "slug": api_data["slug"],
        "status": api_data["status"],
        "parent_id": api_data["parent_id"],
        "is_official": api_data["is_official"],
        "tags": [
            api_data["tags_0"],
            api_data["tags_1"]
        ],
        "metadata": {
            "views": api_data["metadata_views"],
            "score": api_data["metadata_score"],
            "children_count": api_data["metadata_children_count"]
        }
    }
    
    return result