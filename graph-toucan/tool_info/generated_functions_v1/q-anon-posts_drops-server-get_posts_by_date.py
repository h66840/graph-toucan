from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for q-anon-posts/drops-server-get_posts_by_date.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - total_count (int): Total number of posts found
        - date_range_start (str): ISO-formatted start datetime string
        - date_range_end (str): ISO-formatted end datetime string
        - limit (int): Maximum number of results requested
        - has_more (bool): Whether more results exist beyond limit
        - post_0_post_id (int): First post's unique identifier
        - post_0_author (str): First post's author name
        - post_0_author_id (str): First post's author hexadecimal ID
        - post_0_tripcode (str): First post's tripcode
        - post_0_source (str): First post's source platform and board
        - post_0_date (str): First post's ISO-formatted timestamp
        - post_0_text (str): First post's main content
        - post_0_images_0_file (str): First image SHA-256 hash for first post
        - post_0_images_0_name (str): First image filename for first post
        - post_0_images_1_file (str): Second image SHA-256 hash for first post
        - post_0_images_1_name (str): Second image filename for first post
        - post_0_referenced_posts_0_reference (str): First referenced post pointer for first post
        - post_0_referenced_posts_0_author_id (str): Author ID of first referenced post
        - post_0_referenced_posts_0_text (str): Text of first referenced post
        - post_0_referenced_posts_1_reference (str): Second referenced post pointer for first post
        - post_0_referenced_posts_1_author_id (str): Author ID of second referenced post
        - post_0_referenced_posts_1_text (str): Text of second referenced post
        - post_1_post_id (int): Second post's unique identifier
        - post_1_author (str): Second post's author name
        - post_1_author_id (str): Second post's author hexadecimal ID
        - post_1_tripcode (str): Second post's tripcode
        - post_1_source (str): Second post's source platform and board
        - post_1_date (str): Second post's ISO-formatted timestamp
        - post_1_text (str): Second post's main content
        - post_1_images_0_file (str): First image SHA-256 hash for second post
        - post_1_images_0_name (str): First image filename for second post
        - post_1_images_1_file (str): Second image SHA-256 hash for second post
        - post_1_images_1_name (str): Second image filename for second post
        - post_1_referenced_posts_0_reference (str): First referenced post pointer for second post
        - post_1_referenced_posts_0_author_id (str): Author ID of first referenced post
        - post_1_referenced_posts_0_text (str): Text of first referenced post
        - post_1_referenced_posts_1_reference (str): Second referenced post pointer for second post
        - post_1_referenced_posts_1_author_id (str): Author ID of second referenced post
        - post_1_referenced_posts_1_text (str): Text of second referenced post
    """
    return {
        "total_count": 25,
        "date_range_start": "2023-10-01T00:00:00",
        "date_range_end": "2023-10-02T23:59:59",
        "limit": 2,
        "has_more": True,
        "post_0_post_id": 1001,
        "post_0_author": "Q",
        "post_0_author_id": "a1b2c3d4",
        "post_0_tripcode": "!!Secure123",
        "post_0_source": "/qresearch on 8kun",
        "post_0_date": "2023-10-01 14:30:25",
        "post_0_text": "This is a sample post with references and images. https://example.com",
        "post_0_images_0_file": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "post_0_images_0_name": "image1.jpg",
        "post_0_images_1_file": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
        "post_0_images_1_name": "chart.png",
        "post_0_referenced_posts_0_reference": ">>999",
        "post_0_referenced_posts_0_author_id": "z9y8x7w6",
        "post_0_referenced_posts_0_text": "Previous claim about data",
        "post_0_referenced_posts_1_reference": ">>998",
        "post_0_referenced_posts_1_author_id": "m5n4o3p2",
        "post_0_referenced_posts_1_text": "Supporting evidence mentioned",
        "post_1_post_id": 1002,
        "post_1_author": "Q",
        "post_1_author_id": "e5f6g7h8",
        "post_1_tripcode": "!!Verified456",
        "post_1_source": "/qresearch on 8kun",
        "post_1_date": "2023-10-02 09:15:47",
        "post_1_text": "Follow-up analysis and new findings. See attached.",
        "post_1_images_0_file": "3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d",
        "post_1_images_0_name": "graph.jpg",
        "post_1_images_1_file": "2ef7bde608ce5404e97d5f042f95f89f1c232871",
        "post_1_images_1_name": "document.pdf",
        "post_1_referenced_posts_0_reference": ">>1001",
        "post_1_referenced_posts_0_author_id": "a1b2c3d4",
        "post_1_referenced_posts_0_text": "Initial report from yesterday",
        "post_1_referenced_posts_1_reference": ">>990",
        "post_1_referenced_posts_1_author_id": "k1j2i3h4",
        "post_1_referenced_posts_1_text": "Historical context provided earlier"
    }

def q_anon_posts_drops_server_get_posts_by_date(
    start_date: str,
    end_date: Optional[str] = None,
    limit: Optional[int] = 10
) -> Dict[str, Any]:
    """
    Get posts/drops within a specific date range.
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format (required)
        end_date (str, optional): End date in YYYY-MM-DD format (defaults to start_date if not provided)
        limit (int, optional): Maximum number of results to return (default: 10)
    
    Returns:
        Dict containing:
        - posts (List[Dict]): list of post objects with fields like 'post_id', 'author', 'text', etc.
        - total_count (int): total number of posts found in the specified date range
        - date_range (Dict): contains 'start' and 'end' datetime strings indicating the queried date range
        - limit (int): maximum number of results requested to be returned
        - has_more (bool): true if there are more results beyond the returned limit
    """
    # Input validation
    if not start_date:
        raise ValueError("start_date is required")
    
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("start_date must be in YYYY-MM-DD format")
    
    if end_date:
        try:
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("end_date must be in YYYY-MM-DD format")
    else:
        end = start  # Default to start_date if end_date not provided
    
    if limit is None:
        limit = 10
    if limit <= 0:
        raise ValueError("limit must be a positive integer")