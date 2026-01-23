from typing import Dict, List, Any, Optional
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Tencent News trending.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - news_0_title (str): Title of the first trending news item
        - news_0_source (str): Source of the first trending news item
        - news_0_category (str): Category of the first trending news item
        - news_0_timestamp (str): ISO 8601 timestamp of the first news item
        - news_0_summary (str): Summary of the first trending news item
        - news_0_url (str): URL of the first trending news item
        - news_0_relevance_score (float): Relevance score of the first news item
        - news_1_title (str): Title of the second trending news item
        - news_1_source (str): Source of the second trending news item
        - news_1_category (str): Category of the second trending news item
        - news_1_timestamp (str): ISO 8601 timestamp of the second news item
        - news_1_summary (str): Summary of the second trending news item
        - news_1_url (str): URL of the second trending news item
        - news_1_relevance_score (float): Relevance score of the second news item
        - total_count (int): Total number of trending news items returned
        - update_time (str): ISO 8601 timestamp indicating when the trends data was last updated
        - category_0 (str): First category covered in the trends
        - category_1 (str): Second category covered in the trends
        - category_2 (str): Third category covered in the trends
        - has_more (bool): Whether more trending items are available beyond current page
        - metadata_source_platform (str): Source platform name
        - metadata_api_version (str): API version used
        - metadata_request_status (str): Status of the request
    """
    return {
        "news_0_title": "中国成功发射遥感卫星三十号",
        "news_0_source": "新华社",
        "news_0_category": "domestic",
        "news_0_timestamp": "2023-10-05T08:30:00Z",
        "news_0_summary": "我国在酒泉卫星发射中心成功发射遥感卫星三十号，用于科学实验和国土资源普查。",
        "news_0_url": "https://news.qq.com/radar/12345",
        "news_0_relevance_score": 0.98,
        "news_1_title": "国际油价大幅波动引发市场关注",
        "news_1_source": "央视财经",
        "news_1_category": "finance",
        "news_1_timestamp": "2023-10-05T07:15:00Z",
        "news_1_summary": "受地缘政治影响，国际原油价格本周出现显著波动，专家分析后续走势。",
        "news_1_url": "https://news.qq.com/finance/67890",
        "news_1_relevance_score": 0.92,
        "total_count": 2,
        "update_time": datetime.now(timezone.utc).isoformat(),
        "category_0": "domestic",
        "category_1": "finance",
        "category_2": "international",
        "has_more": True,
        "metadata_source_platform": "Tencent News",
        "metadata_api_version": "v1.2.0",
        "metadata_request_status": "success"
    }


def trends_hub_get_tencent_news_trending(page_size: Optional[int] = 20) -> Dict[str, Any]:
    """
    获取腾讯新闻热点榜，包含国内外时事、社会热点、财经资讯、娱乐动态及体育赛事的综合性中文新闻资讯。

    Args:
        page_size (Optional[int]): 每页返回的新闻数量，默认为20

    Returns:
        Dict containing:
        - news_trends (List[Dict]): List of trending news items with title, source, category,
          timestamp, summary, URL, and relevance score
        - total_count (int): Total number of trending news items returned
        - update_time (str): ISO 8601 timestamp indicating when the data was last updated
        - categories_covered (List[str]): List of news categories included
        - has_more (bool): Whether more items are available beyond current page
        - metadata (Dict): Additional metadata including source platform, API version, and status
    """
    # Validate input
    if page_size is not None and (not isinstance(page_size, int) or page_size <= 0):
        raise ValueError("page_size must be a positive integer")

    # Fetch data from external API (simulated)
    raw_data = call_external_api("trends-hub-get-tencent-news-trending")

    # Construct news trends list from indexed fields
    news_trends: List[Dict[str, Any]] = [
        {
            "title": raw_data["news_0_title"],
            "source": raw_data["news_0_source"],
            "category": raw_data["news_0_category"],
            "timestamp": raw_data["news_0_timestamp"],
            "summary": raw_data["news_0_summary"],
            "url": raw_data["news_0_url"],
            "relevance_score": raw_data["news_0_relevance_score"]
        },
        {
            "title": raw_data["news_1_title"],
            "source": raw_data["news_1_source"],
            "category": raw_data["news_1_category"],
            "timestamp": raw_data["news_1_timestamp"],
            "summary": raw_data["news_1_summary"],
            "url": raw_data["news_1_url"],
            "relevance_score": raw_data["news_1_relevance_score"]
        }
    ]

    # Extract categories covered (non-empty values only)
    categories_covered: List[str] = []
    for i in range(3):
        cat = raw_data.get(f"category_{i}")
        if cat:
            categories_covered.append(cat)

    # Construct final result matching output schema
    result = {
        "news_trends": news_trends,
        "total_count": raw_data["total_count"],
        "update_time": raw_data["update_time"],
        "categories_covered": categories_covered,
        "has_more": raw_data["has_more"],
        "metadata": {
            "source_platform": raw_data["metadata_source_platform"],
            "api_version": raw_data["metadata_api_version"],
            "request_status": raw_data["metadata_request_status"]
        }
    }

    return result