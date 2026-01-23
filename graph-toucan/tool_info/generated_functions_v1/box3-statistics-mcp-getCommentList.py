from typing import Dict, List, Any, Optional
import random
import string
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for comment list.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - comment_0_id (int): First comment ID
        - comment_0_content (str): First comment content
        - comment_0_author_id (int): First comment author ID
        - comment_0_author_name (str): First comment author name
        - comment_0_timestamp (int): First comment timestamp (Unix epoch)
        - comment_0_status (str): First comment status ('active', 'deleted', etc.)
        - comment_1_id (int): Second comment ID
        - comment_1_content (str): Second comment content
        - comment_1_author_id (int): Second comment author ID
        - comment_1_author_name (str): Second comment author name
        - comment_1_timestamp (int): Second comment timestamp (Unix epoch)
        - comment_1_status (str): Second comment status ('active', 'deleted', etc.)
        - total_count (int): Total number of comments available
        - has_more (bool): Whether more comments exist beyond current page
        - next_offset (int): Next offset for pagination, or -1 if no more
        - request_id (str): Unique request identifier
        - rate_limit_remaining (int): Number of requests remaining in current window
        - rate_limit_reset (int): Unix timestamp when rate limit resets
    """
    now = int(datetime.now().timestamp())
    reset_time = int((datetime.now() + timedelta(minutes=1)).timestamp())

    return {
        "comment_0_id": 1001,
        "comment_0_content": "这是一条测试评论内容。",
        "comment_0_author_id": 2001,
        "comment_0_author_name": "用户A",
        "comment_0_timestamp": now - 3600,
        "comment_0_status": "active",
        "comment_1_id": 1002,
        "comment_1_content": "这是第二条评论。",
        "comment_1_author_id": 2002,
        "comment_1_author_name": "用户B",
        "comment_1_timestamp": now - 1800,
        "comment_1_status": "active",
        "total_count": 150,
        "has_more": True,
        "next_offset": 2,
        "request_id": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
        "rate_limit_remaining": 98,
        "rate_limit_reset": reset_time,
    }


def box3_statistics_mcp_getCommentList(
    limit: int,
    offset: int,
    token: str,
    userAgent: str
) -> Dict[str, Any]:
    """
    获取神岛平台用户的评论列表，需要Token和用户请求头。

    Args:
        limit (int): 限制返回的评论数量
        offset (int): 分页偏移量
        token (str): 认证Token，用于身份验证
        userAgent (str): 用户请求头，标识客户端信息

    Returns:
        Dict containing:
        - comments (List[Dict]): List of comment objects with id, content, author info, timestamp, and status
        - total_count (int): Total number of comments available on the platform
        - has_more (bool): Whether more comments are available beyond current page
        - next_offset (Optional[int]): Next offset for fetching more data, or None if no more
        - request_id (str): Unique identifier for the API request
        - rate_limit_remaining (int): Number of allowed requests left in current rate limit window
        - rate_limit_reset (int): Unix timestamp (seconds) when rate limit will reset

    Raises:
        ValueError: If limit or offset is negative, or if token/userAgent is empty
    """
    # Input validation
    if limit < 0:
        raise ValueError("limit must be non-negative")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if not token:
        raise ValueError("token is required")
    if not userAgent:
        raise ValueError("userAgent is required")

    # Call external API (simulated)
    api_data = call_external_api("box3-statistics-mcp-getCommentList")

    # Construct comments list from flattened API response
    comments = [
        {
            "id": api_data["comment_0_id"],
            "content": api_data["comment_0_content"],
            "author": {
                "id": api_data["comment_0_author_id"],
                "name": api_data["comment_0_author_name"]
            },
            "timestamp": api_data["comment_0_timestamp"],
            "status": api_data["comment_0_status"]
        },
        {
            "id": api_data["comment_1_id"],
            "content": api_data["comment_1_content"],
            "author": {
                "id": api_data["comment_1_author_id"],
                "name": api_data["comment_1_author_name"]
            },
            "timestamp": api_data["comment_1_timestamp"],
            "status": api_data["comment_1_status"]
        }
    ]

    # Apply limit to comments
    limited_comments = comments[:limit]

    # Determine next_offset and has_more
    next_offset = api_data["next_offset"] if api_data["has_more"] and api_data["next_offset"] != -1 else None
    has_more = api_data["has_more"] and bool(next_offset)

    # Build final result structure
    result = {
        "comments": limited_comments,
        "total_count": api_data["total_count"],
        "has_more": has_more,
        "next_offset": next_offset,
        "request_id": api_data["request_id"],
        "rate_limit_remaining": api_data["rate_limit_remaining"],
        "rate_limit_reset": api_data["rate_limit_reset"]
    }

    return result