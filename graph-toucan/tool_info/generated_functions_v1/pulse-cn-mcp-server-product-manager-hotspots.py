from typing import Dict, List, Any
from datetime import datetime, timezone
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the '人人都是产品经理' hotspots.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - hotspots_0_title (str): Title of the first trending topic
        - hotspots_0_rank (int): Rank of the first trending topic
        - hotspots_0_popularity (int): Popularity score (热度) of the first topic
        - hotspots_0_timestamp (str): ISO 8601 timestamp for the first topic
        - hotspots_1_title (str): Title of the second trending topic
        - hotspots_1_rank (int): Rank of the second trending topic
        - hotspots_1_popularity (int): Popularity score (热度) of the second topic
        - hotspots_1_timestamp (str): ISO 8601 timestamp for the second topic
        - update_time (str): ISO 8601 timestamp when data was last updated
        - source (str): Source platform name
        - total_count (int): Total number of hot topics returned
        - metadata_status (str): Status of the API request
        - metadata_api_version (str): Version of the API
        - metadata_next_update_in_seconds (int): Seconds until next update
    """
    def random_title():
        subjects = ["产品经理", "用户增长", "产品设计", "数据分析", "AI产品", "用户体验", "需求文档", "产品迭代"]
        actions = ["如何做好", "实战分享", "避坑指南", "深度解析", "入门必读", "高效方法论"]
        return f"{random.choice(actions)} {random.choice(subjects)}"

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    past_time = (datetime.now(timezone.utc) - datetime.timedelta(minutes=5)).isoformat().replace("+00:00", "Z")

    return {
        "hotspots_0_title": random_title(),
        "hotspots_0_rank": 1,
        "hotspots_0_popularity": random.randint(8000, 10000),
        "hotspots_0_timestamp": now,
        "hotspots_1_title": random_title(),
        "hotspots_1_rank": 2,
        "hotspots_1_popularity": random.randint(6000, 8000),
        "hotspots_1_timestamp": past_time,
        "update_time": now,
        "source": "人人都是产品经理",
        "total_count": 2,
        "metadata_status": "success",
        "metadata_api_version": "1.0",
        "metadata_next_update_in_seconds": 300
    }

def pulse_cn_mcp_server_product_manager_hotspots() -> Dict[str, Any]:
    """
    获取人人都是产品经理热搜榜单，返回包含热点内容的实时数据。

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending topics with title, rank,热度, and timestamp
        - update_time (str): ISO 8601 timestamp indicating when the data was last updated
        - source (str): Source platform name
        - total_count (int): Total number of hot topics returned
        - metadata (Dict): Additional info like status, api_version, next_update_in_seconds
    """
    try:
        # Fetch simulated external API data
        api_data = call_external_api("pulse-cn-mcp-server-product-manager-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "title": api_data["hotspots_0_title"],
                "rank": api_data["hotspots_0_rank"],
                "热度": api_data["hotspots_0_popularity"],
                "timestamp": api_data["hotspots_0_timestamp"]
            },
            {
                "title": api_data["hotspots_1_title"],
                "rank": api_data["hotspots_1_rank"],
                "热度": api_data["hotspots_1_popularity"],
                "timestamp": api_data["hotspots_1_timestamp"]
            }
        ]

        # Construct metadata
        metadata = {
            "status": api_data["metadata_status"],
            "api_version": api_data["metadata_api_version"],
            "next_update_in_seconds": api_data["metadata_next_update_in_seconds"]
        }

        # Build final result
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "source": api_data["source"],
            "total_count": api_data["total_count"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise ValueError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve or process hotspots data: {str(e)}") from e