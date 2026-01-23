from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for The Paper news hotspots.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - hotspots_0_rank (int): Rank of the first trending news item
        - hotspots_0_title (str): Title of the first trending news item
        - hotspots_0_heat (int): Popularity score of the first item
        - hotspots_0_url (str): URL of the first news article
        - hotspots_0_category (str): Category of the first news item
        - hotspots_0_timestamp (str): ISO 8601 timestamp when first item was updated
        - hotspots_1_rank (int): Rank of the second trending news item
        - hotspots_1_title (str): Title of the second trending news item
        - hotspots_1_heat (int): Popularity score of the second item
        - hotspots_1_url (str): URL of the second news article
        - hotspots_1_category (str): Category of the second news item
        - hotspots_1_timestamp (str): ISO 8601 timestamp when second item was updated
        - update_time (str): ISO 8601 timestamp when the entire list was last updated
        - source (str): Name of the source platform
        - total_count (int): Total number of tracked hotspots
        - has_more (bool): Whether more items exist beyond the limit
    """
    return {
        "hotspots_0_rank": 1,
        "hotspots_0_title": "中国航天发布火星探测最新进展",
        "hotspots_0_heat": 987654,
        "hotspots_0_url": "https://www.thepaper.cn/news_detail_123456",
        "hotspots_0_category": "science",
        "hotspots_0_timestamp": "2025-04-05T08:30:00Z",
        "hotspots_1_rank": 2,
        "hotspots_1_title": "春季旅游市场迎来爆发式增长",
        "hotspots_1_heat": 876543,
        "hotspots_1_url": "https://www.thepaper.cn/news_detail_123457",
        "hotspots_1_category": "economy",
        "hotspots_1_timestamp": "2025-04-05T07:45:00Z",
        "update_time": "2025-04-05T09:00:00Z",
        "source": "The Paper",
        "total_count": 50,
        "has_more": True
    }

def pulse_cn_mcp_server_the_paper_news_hotspots(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    获取澎湃新闻热搜榜单，返回包含热点内容的实时数据。
    
    通过模拟API调用获取澎湃新闻的热搜数据，并根据limit参数限制返回数量。
    数据结构严格按照输出schema构建，包括热点列表、更新时间、来源等信息。
    
    Args:
        limit (Optional[int]): 显示的新闻数量限制，默认为None（返回所有可用项，最多为total_count）
    
    Returns:
        Dict[str, Any]: 包含以下键的字典：
            - hotspots (List[Dict]): 当前热搜新闻列表，每个条目包含rank, title, heat, url, category, timestamp
            - update_time (str): 数据最后更新时间（ISO 8601格式）
            - source (str): 数据来源标识
            - total_count (int): 当前追踪的热搜总数
            - has_more (bool): 是否存在超出返回列表的更多热搜
    
    Raises:
        ValueError: 如果limit为负数则抛出异常
    """
    if limit is not None and limit < 0:
        raise ValueError("limit must be non-negative")

    # 调用外部API获取扁平化数据
    api_data = call_external_api("pulse-cn-mcp-server-the-paper-news-hotspots")
    
    # 构建热搜列表（最多2个，根据API模拟数据）
    raw_hotspots = [
        {
            "rank": api_data["hotspots_0_rank"],
            "title": api_data["hotspots_0_title"],
            "heat": api_data["hotspots_0_heat"],
            "url": api_data["hotspots_0_url"],
            "category": api_data["hotspots_0_category"],
            "timestamp": api_data["hotspots_0_timestamp"]
        },
        {
            "rank": api_data["hotspots_1_rank"],
            "title": api_data["hotspots_1_title"],
            "heat": api_data["hotspots_1_heat"],
            "url": api_data["hotspots_1_url"],
            "category": api_data["hotspots_1_category"],
            "timestamp": api_data["hotspots_1_timestamp"]
        }
    ]
    
    # 根据limit参数过滤结果
    effective_limit = limit if limit is not None else len(raw_hotspots)
    hotspots = raw_hotspots[:effective_limit]
    
    # 构造最终返回结果
    result = {
        "hotspots": hotspots,
        "update_time": api_data["update_time"],
        "source": api_data["source"],
        "total_count": api_data["total_count"],
        "has_more": api_data["has_more"]
    }
    
    return result