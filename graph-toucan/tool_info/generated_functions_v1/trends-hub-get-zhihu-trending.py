from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching Zhihu trending data from external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - trending_item_0_title (str): Title of the first trending Zhihu question
        - trending_item_0_description (str): Description of the first trending item
        - trending_item_0_cover (str): URL of the cover image for the first item
        - trending_item_0_created (int): Unix timestamp of creation time for first item
        - trending_item_0_popularity (int): Popularity score (e.g., view count or vote count)
        - trending_item_0_link (str): Direct link to the first trending question
        - trending_item_1_title (str): Title of the second trending Zhihu question
        - trending_item_1_description (str): Description of the second trending item
        - trending_item_1_cover (str): URL of the cover image for the second item
        - trending_item_1_created (int): Unix timestamp of creation time for second item
        - trending_item_1_popularity (int): Popularity score for second item
        - trending_item_1_link (str): Direct link to the second trending question
    """
    current_timestamp = int(datetime.datetime.now().timestamp())
    return {
        "trending_item_0_title": "如何评价中国航天员首次出舱活动？",
        "trending_item_0_description": "中国航天员在空间站成功完成首次出舱任务，引发广泛关注。",
        "trending_item_0_cover": "https://example.com/images/astronaut.jpg",
        "trending_item_0_created": current_timestamp - 3600,
        "trending_item_0_popularity": 125000,
        "trending_item_0_link": "https://www.zhihu.com/question/123456789",

        "trending_item_1_title": "为什么年轻人越来越不敢结婚？",
        "trending_item_1_description": "社会压力、经济负担和观念变化让结婚变得复杂。",
        "trending_item_1_cover": "https://example.com/images/marriage.jpg",
        "trending_item_1_created": current_timestamp - 7200,
        "trending_item_1_popularity": 98000,
        "trending_item_1_link": "https://www.zhihu.com/question/987654321"
    }


def trends_hub_get_zhihu_trending(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    获取知乎热榜，包含时事热点、社会话题、科技动态、娱乐八卦等多领域的热门问答和讨论的中文资讯。

    Args:
        limit (Optional[int]): 返回的热门条目数量上限，默认返回全部可用条目（最多2条模拟数据）

    Returns:
        Dict[str, Any]: 包含 'trending_items' 键的字典，其值为热门问题列表，每个问题包含：
            - title (str): 问题标题
            - description (str): 问题描述
            - cover (str): 封面图片链接
            - created (int): 创建时间戳（Unix时间）
            - popularity (int): 热度值（如浏览量或赞同数）
            - link (str): 问题链接
    """
    # 调用外部API获取扁平化的数据
    api_data = call_external_api("trends-hub-get-zhihu-trending")

    # 构建 trending_items 列表
    trending_items: List[Dict[str, Any]] = []

    # 添加第一个项目（如果存在）
    if "trending_item_0_title" in api_data:
        item_0 = {
            "title": api_data["trending_item_0_title"],
            "description": api_data["trending_item_0_description"],
            "cover": api_data["trending_item_0_cover"],
            "created": api_data["trending_item_0_created"],
            "popularity": api_data["trending_item_0_popularity"],
            "link": api_data["trending_item_0_link"]
        }
        trending_items.append(item_0)

    # 添加第二个项目（如果存在）
    if "trending_item_1_title" in api_data:
        item_1 = {
            "title": api_data["trending_item_1_title"],
            "description": api_data["trending_item_1_description"],
            "cover": api_data["trending_item_1_cover"],
            "created": api_data["trending_item_1_created"],
            "popularity": api_data["trending_item_1_popularity"],
            "link": api_data["trending_item_1_link"]
        }
        trending_items.append(item_1)

    # 应用 limit 参数限制返回数量
    if limit is not None and limit > 0:
        trending_items = trending_items[:limit]

    return {
        "trending_items": trending_items
    }