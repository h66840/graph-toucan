from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Zhihu real-time hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspot_0_title (str): Title of the first trending topic
        - hotspot_0_rank (int): Rank of the first trending topic
        - hotspot_0_heat (int): Heat score of the first trending topic
        - hotspot_0_url (str): URL of the first trending topic
        - hotspot_1_title (str): Title of the second trending topic
        - hotspot_1_rank (int): Rank of the second trending topic
        - hotspot_1_heat (int): Heat score of the second trending topic
        - hotspot_1_url (str): URL of the second trending topic
        - update_time (str): Timestamp when data was last updated in ISO 8601 format
        - source (str): Source platform name
        - total_count (int): Total number of trending items returned
        - metadata_status (str): Status of the API request
        - metadata_version (str): API version
        - metadata_refresh_interval (int): Refresh interval in seconds
    """
    return {
        "hotspot_0_title": "如何评价2024年第一季度中国GDP增长?",
        "hotspot_0_rank": 1,
        "hotspot_0_heat": 987654,
        "hotspot_0_url": "https://www.zhihu.com/hot/1",
        "hotspot_1_title": "为什么年轻人越来越不敢结婚？",
        "hotspot_1_rank": 2,
        "hotspot_1_heat": 876543,
        "hotspot_1_url": "https://www.zhihu.com/hot/2",
        "update_time": "2024-05-20T12:34:56Z",
        "source": "Zhihu",
        "total_count": 2,
        "metadata_status": "success",
        "metadata_version": "1.0.0",
        "metadata_refresh_interval": 300,
    }


def pulse_cn_mcp_server_zhihu_realtime_hotspots() -> Dict[str, Any]:
    """
    Fetches real-time trending topics from Zhihu via external API simulation.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of real-time trending topics on Zhihu,
          each with title, rank, heat, and URL
        - update_time (str): Timestamp of last update in ISO 8601 format
        - source (str): Source platform name ('Zhihu')
        - total_count (int): Number of trending items returned
        - metadata (Dict): Additional API response info like status, version, refresh interval

    Raises:
        KeyError: If expected fields are missing from API response
        ValueError: If data validation fails
    """
    try:
        api_data = call_external_api("pulse-cn-mcp-server-zhihu-realtime-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "title": api_data["hotspot_0_title"],
                "rank": api_data["hotspot_0_rank"],
                "heat": api_data["hotspot_0_heat"],
                "url": api_data["hotspot_0_url"],
            },
            {
                "title": api_data["hotspot_1_title"],
                "rank": api_data["hotspot_1_rank"],
                "heat": api_data["hotspot_1_heat"],
                "url": api_data["hotspot_1_url"],
            },
        ]

        # Construct metadata
        metadata = {
            "status": api_data["metadata_status"],
            "version": api_data["metadata_version"],
            "refresh_interval": api_data["metadata_refresh_interval"],
        }

        # Final result structure
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "source": api_data["source"],
            "total_count": api_data["total_count"],
            "metadata": metadata,
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing required field in API response: {e}")
    except Exception as e:
        raise ValueError(f"Failed to process Zhihu real-time hotspots data: {e}")