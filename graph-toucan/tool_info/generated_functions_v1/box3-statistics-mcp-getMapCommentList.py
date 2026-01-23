from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for map comment list.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - comment_0_commentId (str): First comment ID
        - comment_0_userId (str): First comment user ID
        - comment_0_username (str): First comment username
        - comment_0_content (str): First comment content
        - comment_0_createdAt (str): First comment creation time in ISO 8601
        - comment_0_likeCount (int): First comment like count
        - comment_0_replyCount (int): First comment reply count
        - comment_0_isHot (bool): Whether first comment is marked as hot
        - comment_1_commentId (str): Second comment ID
        - comment_1_userId (str): Second comment user ID
        - comment_1_username (str): Second comment username
        - comment_1_content (str): Second comment content
        - comment_1_createdAt (str): Second comment creation time in ISO 8601
        - comment_1_likeCount (int): Second comment like count
        - comment_1_replyCount (int): Second comment reply count
        - comment_1_isHot (bool): Whether second comment is marked as hot
        - totalCount (int): Total number of comments matching criteria
        - hasMore (bool): Whether there are more comments beyond current offset and limit
        - metadata_requestTime (str): ISO 8601 timestamp of request processing
        - metadata_orderByLabel (str): Label for the orderBy parameter (e.g., "热度排序")
        - metadata_contentTypeLabel (str): Label for the contentType (e.g., "地图")
    """
    return {
        "comment_0_commentId": "cmt_001",
        "comment_0_userId": "usr_1001",
        "comment_0_username": "user_john",
        "comment_0_content": "这个地图太棒了，细节非常到位！",
        "comment_0_createdAt": "2024-04-01T10:00:00Z",
        "comment_0_likeCount": 45,
        "comment_0_replyCount": 12,
        "comment_0_isHot": True,
        "comment_1_commentId": "cmt_002",
        "comment_1_userId": "usr_1002",
        "comment_1_username": "user_lisa",
        "comment_1_content": "模型加载有点卡，优化一下会更好。",
        "comment_1_createdAt": "2024-04-01T09:30:00Z",
        "comment_1_likeCount": 23,
        "comment_1_replyCount": 5,
        "comment_1_isHot": False,
        "totalCount": 150,
        "hasMore": True,
        "metadata_requestTime": datetime.now(timezone.utc).isoformat(),
        "metadata_orderByLabel": "热度排序",
        "metadata_contentTypeLabel": "地图"
    }


def box3_statistics_mcp_getMapCommentList(
    contentId: str,
    contentType: int,
    limit: int,
    offset: int,
    orderBy: int
) -> Dict[str, Any]:
    """
    获取神岛平台用户地图评论列表。

    根据提供的地图ID、内容类型、查询数量、偏移量和排序方式，返回用户评论列表及相关元数据。
    本函数模拟调用外部API并构造符合输出结构的响应数据。

    Args:
        contentId (str): 地图ID
        contentType (int): 评论分类，1表示地图，2表示模型
        limit (int): 查询数量，最多100条
        offset (int): 偏移量
        orderBy (int): 排序方式，1为创建时间倒序，4为热度排序（默认）

    Returns:
        Dict[str, Any]: 包含以下键的字典：
            - comments (List[Dict]): 评论列表，每条评论包含commentId, userId, username,
              content, createdAt, likeCount, replyCount, isHot
            - totalCount (int): 符合条件的评论总数
            - hasMore (bool): 是否还有更多评论
            - metadata (Dict): 元数据，包含requestTime, orderByLabel, contentTypeLabel

    Raises:
        ValueError: 当输入参数不符合要求时抛出异常
    """
    # 输入验证
    if not contentId:
        raise ValueError("contentId is required")
    if contentType not in [1, 2]:
        raise ValueError("contentType must be 1 (地图) or 2 (模型)")
    if not (1 <= limit <= 100):
        raise ValueError("limit must be between 1 and 100")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if orderBy not in [1, 4]:
        raise ValueError("orderBy must be 1 (创建时间倒序) or 4 (热度)")

    # 调用外部API获取扁平化数据
    api_data = call_external_api("box3-statistics-mcp-getMapCommentList")

    # 构建评论列表
    comments = [
        {
            "commentId": api_data["comment_0_commentId"],
            "userId": api_data["comment_0_userId"],
            "username": api_data["comment_0_username"],
            "content": api_data["comment_0_content"],
            "createdAt": api_data["comment_0_createdAt"],
            "likeCount": api_data["comment_0_likeCount"],
            "replyCount": api_data["comment_0_replyCount"],
            "isHot": api_data["comment_0_isHot"]
        },
        {
            "commentId": api_data["comment_1_commentId"],
            "userId": api_data["comment_1_userId"],
            "username": api_data["comment_1_username"],
            "content": api_data["comment_1_content"],
            "createdAt": api_data["comment_1_createdAt"],
            "likeCount": api_data["comment_1_likeCount"],
            "replyCount": api_data["comment_1_replyCount"],
            "isHot": api_data["comment_1_isHot"]
        }
    ]

    # 构建元数据
    metadata = {
        "requestTime": api_data["metadata_requestTime"],
        "orderByLabel": api_data["metadata_orderByLabel"],
        "contentTypeLabel": api_data["metadata_contentTypeLabel"]
    }

    # 构造最终结果
    result = {
        "comments": comments,
        "totalCount": api_data["totalCount"],
        "hasMore": api_data["hasMore"],
        "metadata": metadata
    }

    return result