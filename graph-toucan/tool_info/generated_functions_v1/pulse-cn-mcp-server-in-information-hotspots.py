from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for IT news hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspots_0_title (str): Title of the first trending IT news item
        - hotspots_0_rank (int): Rank of the first item in the list
        - hotspots_0_popularity_score (float): Popularity score of the first item
        - hotspots_0_source (str): Source publication or website of the first item
        - hotspots_0_timestamp (str): ISO 8601 timestamp when the first item was published
        - hotspots_0_url (str): URL link to the first news item
        - hotspots_1_title (str): Title of the second trending IT news item
        - hotspots_1_rank (int): Rank of the second item in the list
        - hotspots_1_popularity_score (float): Popularity score of the second item
        - hotspots_1_source (str): Source publication or website of the second item
        - hotspots_1_timestamp (str): ISO 8601 timestamp when the second item was published
        - hotspots_1_url (str): URL link to the second news item
        - update_time (str): ISO 8601 timestamp indicating when the data was last updated
        - total_count (int): Total number of hotspot entries returned
        - region (str): Geographic region for which the hotspots are relevant (e.g., "CN")
        - metadata_data_source (str): Name of the data source providing the information
        - metadata_api_version (str): Version of the API used to fetch the data
        - metadata_refresh_interval_seconds (int): Interval in seconds at which data is refreshed
    """
    return {
        "hotspots_0_title": "AI 大模型竞争白热化：通义千问发布新版本",
        "hotspots_0_rank": 1,
        "hotspots_0_popularity_score": 9876.5,
        "hotspots_0_source": "TechNode",
        "hotspots_0_timestamp": "2024-04-05T08:30:00Z",
        "hotspots_0_url": "https://technode.com/ai-qwen-update",

        "hotspots_1_title": "华为发布全新鸿蒙系统，支持多设备无缝协同",
        "hotspots_1_rank": 2,
        "hotspots_1_popularity_score": 8765.4,
        "hotspots_1_source": "PingWest",
        "hotspots_1_timestamp": "2024-04-05T07:15:00Z",
        "hotspots_1_url": "https://pingwest.com/harmonyos-launch",

        "update_time": "2024-04-05T09:00:00Z",
        "total_count": 2,
        "region": "CN",
        "metadata_data_source": "PulseCN MCP Server",
        "metadata_api_version": "v1.2.3",
        "metadata_refresh_interval_seconds": 300,
    }


def pulse_cn_mcp_server_in_information_hotspots() -> Dict[str, Any]:
    """
    获取IT资讯热搜榜单，返回包含热点内容的实时数据。

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending IT news items with title, rank, popularity score,
          source, timestamp, and URL
        - update_time (str): ISO 8601 timestamp indicating when the data was last updated
        - total_count (int): Total number of hotspot entries returned
        - region (str): Geographic region for which the hotspots are relevant (e.g., "CN")
        - metadata (Dict): Additional contextual information including data source, API version,
          and refresh interval
    """
    try:
        # Fetch simulated API data
        api_data = call_external_api("pulse-cn-mcp-server-in-information-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "title": api_data["hotspots_0_title"],
                "rank": api_data["hotspots_0_rank"],
                "popularity_score": api_data["hotspots_0_popularity_score"],
                "source": api_data["hotspots_0_source"],
                "timestamp": api_data["hotspots_0_timestamp"],
                "url": api_data["hotspots_0_url"],
            },
            {
                "title": api_data["hotspots_1_title"],
                "rank": api_data["hotspots_1_rank"],
                "popularity_score": api_data["hotspots_1_popularity_score"],
                "source": api_data["hotspots_1_source"],
                "timestamp": api_data["hotspots_1_timestamp"],
                "url": api_data["hotspots_1_url"],
            },
        ]

        # Construct metadata
        metadata = {
            "data_source": api_data["metadata_data_source"],
            "api_version": api_data["metadata_api_version"],
            "refresh_interval_seconds": api_data["metadata_refresh_interval_seconds"],
        }

        # Build final result
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "total_count": api_data["total_count"],
            "region": api_data["region"],
            "metadata": metadata,
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing expected field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve or process IT news hotspots: {str(e)}") from e