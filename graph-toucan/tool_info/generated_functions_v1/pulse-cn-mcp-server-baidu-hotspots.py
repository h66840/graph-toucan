from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Baidu hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspots_0_rank (int): Rank of the first trending topic
        - hotspots_0_keyword (str): Search term or headline of the first topic
        - hotspots_0_url (str): Direct link to the Baidu search results for the first topic
        - hotspots_0_heat_score (int): Popularity score of the first topic
        - hotspots_0_formatted_query (str): Display-ready version of the first keyword
        - hotspots_0_description (str): Summary or context for the first topic
        - hotspots_0_is_promoted (bool): Whether the first entry is sponsored
        - hotspots_1_rank (int): Rank of the second trending topic
        - hotspots_1_keyword (str): Search term or headline of the second topic
        - hotspots_1_url (str): Direct link to the Baidu search results for the second topic
        - hotspots_1_heat_score (int): Popularity score of the second topic
        - hotspots_1_formatted_query (str): Display-ready version of the second keyword
        - hotspots_1_description (str): Summary or context for the second topic
        - hotspots_1_is_promoted (bool): Whether the second entry is sponsored
        - update_time (str): ISO 8601 timestamp when data was fetched
        - source (str): Name of the source platform
        - total_count (int): Total number of hotspots returned
        - refresh_interval (int): Suggested interval in seconds before next refresh
    """
    return {
        "hotspots_0_rank": 1,
        "hotspots_0_keyword": "北京天气",
        "hotspots_0_url": "https://www.baidu.com/s?wd=北京天气",
        "hotspots_0_heat_score": 987654,
        "hotspots_0_formatted_query": "北京天气预报",
        "hotspots_0_description": "今日北京气温骤降，伴有强风",
        "hotspots_0_is_promoted": False,
        "hotspots_1_rank": 2,
        "hotspots_1_keyword": "中国女足",
        "hotspots_1_url": "https://www.baidu.com/s?wd=中国女足",
        "hotspots_1_heat_score": 876543,
        "hotspots_1_formatted_query": "中国女足最新比赛",
        "hotspots_1_description": "女足亚洲杯半决赛即将开赛",
        "hotspots_1_is_promoted": True,
        "update_time": datetime.now(timezone.utc).isoformat(),
        "source": "Baidu",
        "total_count": 2,
        "refresh_interval": 300
    }


def pulse_cn_mcp_server_baidu_hotspots() -> Dict[str, Any]:
    """
    获取百度热搜榜单，返回包含热点内容的实时数据。

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending search entries with rank, keyword, URL, heat score,
          formatted query, description, and promotion status
        - update_time (str): ISO 8601 timestamp indicating when the data was last updated
        - source (str): Name of the source platform ("Baidu")
        - total_count (int): Total number of hotspots in the result set
        - refresh_interval (int): Suggested refresh interval in seconds

    Each hotspot dict contains:
        - rank (int): Position on the heatmap (starting from 1)
        - keyword (str): Actual search term or headline
        - url (str): Direct link to Baidu search results
        - heat_score (int): Numeric popularity indicator
        - formatted_query (str): Cleaned or display-ready version of keyword
        - description (str): Brief summary about the topic
        - is_promoted (bool): Whether the entry is sponsored/boosted
    """
    try:
        # Fetch simulated external data
        api_data = call_external_api("pulse-cn-mcp-server-baidu-hotspots")

        # Construct hotspots list from indexed fields
        hotspots: List[Dict[str, Any]] = [
            {
                "rank": api_data["hotspots_0_rank"],
                "keyword": api_data["hotspots_0_keyword"],
                "url": api_data["hotspots_0_url"],
                "heat_score": api_data["hotspots_0_heat_score"],
                "formatted_query": api_data["hotspots_0_formatted_query"],
                "description": api_data["hotspots_0_description"],
                "is_promoted": api_data["hotspots_0_is_promoted"]
            },
            {
                "rank": api_data["hotspots_1_rank"],
                "keyword": api_data["hotspots_1_keyword"],
                "url": api_data["hotspots_1_url"],
                "heat_score": api_data["hotspots_1_heat_score"],
                "formatted_query": api_data["hotspots_1_formatted_query"],
                "description": api_data["hotspots_1_description"],
                "is_promoted": api_data["hotspots_1_is_promoted"]
            }
        ]

        # Build final result structure
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "source": api_data["source"],
            "total_count": api_data["total_count"],
            "refresh_interval": api_data["refresh_interval"]
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve or process Baidu hotspots: {str(e)}") from e