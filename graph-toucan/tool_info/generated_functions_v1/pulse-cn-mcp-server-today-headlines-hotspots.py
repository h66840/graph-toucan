from typing import Dict, List, Any, Optional
import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for today's headlines hotspots.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - hotspot_0_rank (int): Rank of the first trending topic
        - hotspot_0_title (str): Title of the first trending topic
        - hotspot_0_url (str): URL link for the first trending topic
        - hotspot_0_query_count (str or int): Estimated search volume for the first topic
        - hotspot_0_source (str): Source of the first trending topic (e.g., 'Toutiao')
        - hotspot_0_timestamp (str): Time of data capture for the first topic
        - hotspot_1_rank (int): Rank of the second trending topic
        - hotspot_1_title (str): Title of the second trending topic
        - hotspot_1_url (str): URL link for the second trending topic
        - hotspot_1_query_count (str or int): Estimated search volume for the second topic
        - hotspot_1_source (str): Source of the second trending topic (e.g., 'Toutiao')
        - hotspot_1_timestamp (str): Time of data capture for the second topic
    """
    current_time = datetime.datetime.now().isoformat()
    return {
        "hotspot_0_rank": 1,
        "hotspot_0_title": "A major breakthrough in AI technology announced",
        "hotspot_0_url": "https://example.com/ai-breakthrough",
        "hotspot_0_query_count": "1.2M",
        "hotspot_0_source": "Toutiao",
        "hotspot_0_timestamp": current_time,
        "hotspot_1_rank": 2,
        "hotspot_1_title": "National holiday travel rush begins",
        "hotspot_1_url": "https://example.com/holiday-travel",
        "hotspot_1_query_count": "980K",
        "hotspot_1_source": "Toutiao",
        "hotspot_1_timestamp": current_time,
    }

def pulse_cn_mcp_server_today_headlines_hotspots(limit: Optional[int] = None) -> Dict[str, Any]:
    """
    获取今日头条热点热搜，返回包含热点内容的实时数据。通过API实时获取。
    
    Args:
        limit (Optional[int]): 显示的热点数量限制，默认为无限制（返回所有可用数据）
    
    Returns:
        Dict[str, Any]: 包含热点列表的字典，键为 'hotspots'，值为 List[Dict]，每个元素包含：
            - rank (int): 排名
            - title (str): 热点标题
            - url (str): 相关链接
            - query_count (str or int): 预估搜索量
            - source (str): 来源（如 'Toutiao'）
            - timestamp (str): 数据抓取时间
    
    Raises:
        ValueError: 如果 limit 小于 0
    """
    if limit is not None and (not isinstance(limit, int) or limit < 0):
        raise ValueError("limit must be a non-negative integer")

    # 调用外部API获取扁平化的热点数据
    api_data = call_external_api("pulse-cn-mcp-server-today-headlines-hotspots")

    # 构建热点列表
    hotspots = []
    max_items = min(limit or 2, 2)  # 最多支持2个热点（模拟API限制）

    for i in range(max_items):
        try:
            hotspot = {
                "rank": api_data[f"hotspot_{i}_rank"],
                "title": api_data[f"hotspot_{i}_title"],
                "url": api_data[f"hotspot_{i}_url"],
                "query_count": api_data[f"hotspot_{i}_query_count"],
                "source": api_data[f"hotspot_{i}_source"],
                "timestamp": api_data[f"hotspot_{i}_timestamp"]
            }
            hotspots.append(hotspot)
        except KeyError:
            # 如果某个索引的数据不存在，则跳过
            continue

    return {"hotspots": hotspots}