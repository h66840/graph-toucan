from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for posts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_count (int): Total number of posts available
        - retrieved (int): Number of posts returned in this response
        - processed_in (int): Time in milliseconds the request took
        - post_0_id (str): ID of the first post
        - post_0_title (str): Title of the first post
        - post_0_abstract (str): Abstract of the first post
        - post_0_type (str): Type of the first post
        - post_0_link (str): Link to the first post
        - post_0_additional_link_0 (str): First additional link of the first post
        - post_0_additional_link_1 (str): Second additional link of the first post
        - post_0_portal_link (str): Portal link of the first post
        - post_0_portal_name (str): Portal name of the first post
        - post_0_tag_0 (str): First tag of the first post
        - post_0_tag_1 (str): Second tag of the first post
        - post_0_language (str): Language of the first post
        - post_0_date (str): Date of the first post in ISO format
        - post_1_id (str): ID of the second post
        - post_1_title (str): Title of the second post
        - post_1_abstract (str): Abstract of the second post
        - post_1_type (str): Type of the second post
        - post_1_link (str): Link to the second post
        - post_1_additional_link_0 (str): First additional link of the second post
        - post_1_additional_link_1 (str): Second additional link of the second post
        - post_1_portal_link (str): Portal link of the second post
        - post_1_portal_name (str): Portal name of the second post
        - post_1_tag_0 (str): First tag of the second post
        - post_1_tag_1 (str): Second tag of the second post
        - post_1_language (str): Language of the second post
        - post_1_date (str): Date of the second post in ISO format
    """
    return {
        "total_count": 150,
        "retrieved": 2,
        "processed_in": 45,
        "post_0_id": "post123",
        "post_0_title": "Introduction to Python",
        "post_0_abstract": "A beginner's guide to Python programming.",
        "post_0_type": "tutorial",
        "post_0_link": "https://example.com/python-intro",
        "post_0_additional_link_0": "https://example.com/python-basics",
        "post_0_additional_link_1": "https://example.com/python-examples",
        "post_0_portal_link": "https://portal.example.com",
        "post_0_portal_name": "DevPortal",
        "post_0_tag_0": "python",
        "post_0_tag_1": "programming",
        "post_0_language": "en",
        "post_0_date": "2023-10-05T08:00:00Z",
        "post_1_id": "post456",
        "post_1_title": "Advanced JavaScript Techniques",
        "post_1_abstract": "Deep dive into modern JavaScript features.",
        "post_1_type": "article",
        "post_1_link": "https://example.com/advanced-js",
        "post_1_additional_link_0": "https://example.com/js-closures",
        "post_1_additional_link_1": "https://example.com/js-promises",
        "post_1_portal_link": "https://portal.example.com",
        "post_1_portal_name": "DevPortal",
        "post_1_tag_0": "javascript",
        "post_1_tag_1": "webdev",
        "post_1_language": "en",
        "post_1_date": "2023-10-04T10:30:00Z",
    }

def erick_wendel_contributions_get_posts(
    id: Optional[str] = None,
    language: Optional[str] = None,
    limit: Optional[int] = None,
    portal: Optional[str] = None,
    skip: Optional[int] = None,
    title: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get a list of posts with optional filtering and pagination.

    Args:
        id (Optional[str]): Filter posts by ID.
        language (Optional[str]): Filter posts by language.
        limit (Optional[int]): Maximum number of posts to return.
        portal (Optional[str]): Filter posts by portal.
        skip (Optional[int]): Number of posts to skip.
        title (Optional[str]): Filter posts by title.

    Returns:
        Dict containing:
        - totalCount (int): total number of posts available across all results
        - retrieved (int): number of posts returned in this response
        - processedIn (int): time in milliseconds that the request took to process
        - posts (List[Dict]): list of post objects with '_id', 'title', 'abstract', 'type',
          'link', 'additionalLinks', 'portal', 'tags', 'language', and 'date'
    """
    # Fetch data from external API (simulated)
    api_data = call_external_api("erick-wendel-contributions-get_posts")

    # Extract scalar values
    total_count = api_data["total_count"]
    retrieved = api_data["retrieved"]
    processed_in = api_data["processed_in"]

    # Construct posts list from indexed fields
    posts = []

    for i in range(2):  # We have two posts in the mock data
        post_id_key = f"post_{i}_id"
        if post_id_key not in api_data or not api_data[post_id_key]:
            continue

        # Apply filters
        post_title = api_data[f"post_{i}_title"]
        post_language = api_data[f"post_{i}_language"]
        post_portal_name = api_data[f"post_{i}_portal_name"]

        if id and api_data[f"post_{i}_id"] != id:
            continue
        if language and post_language != language:
            continue
        if title and title.lower() not in post_title.lower():
            continue
        if portal and post_portal_name != portal:
            continue

        # Build additional links list
        additional_links = []
        if api_data.get(f"post_{i}_additional_link_0"):
            additional_links.append(api_data[f"post_{i}_additional_link_0"])
        if api_data.get(f"post_{i}_additional_link_1"):
            additional_links.append(api_data[f"post_{i}_additional_link_1"])

        # Build tags list
        tags = []
        if api_data.get(f"post_{i}_tag_0"):
            tags.append(api_data[f"post_{i}_tag_0"])
        if api_data.get(f"post_{i}_tag_1"):
            tags.append(api_data[f"post_{i}_tag_1"])

        # Build portal dict
        portal_info = {
            "link": api_data[f"post_{i}_portal_link"],
            "name": api_data[f"post_{i}_portal_name"]
        }

        # Build post dict
        post = {
            "_id": api_data[f"post_{i}_id"],
            "title": post_title,
            "abstract": api_data[f"post_{i}_abstract"],
            "type": api_data[f"post_{i}_type"],
            "link": api_data[f"post_{i}_link"],
            "additionalLinks": additional_links,
            "portal": portal_info,
            "tags": tags,
            "language": post_language,
            "date": api_data[f"post_{i}_date"]
        }

        posts.append(post)

    # Apply limit and skip
    if skip:
        posts = posts[skip:]
    if limit is not None:
        posts = posts[:limit]
        retrieved = min(len(posts), retrieved)

    # Final result
    result = {
        "totalCount": total_count,
        "retrieved": retrieved,
        "processedIn": processed_in,
        "posts": posts
    }

    return result