from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Huxiu trending hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspot_0_title (str): Title of the first trending hotspot
        - hotspot_0_rank (int): Rank of the first hotspot
        - hotspot_0_url (str): URL of the first hotspot
        - hotspot_0_metrics_views (int): View count for the first hotspot
        - hotspot_0_metrics_comments (int): Comment count for the first hotspot
        - hotspot_1_title (str): Title of the second trending hotspot
        - hotspot_1_rank (int): Rank of the second hotspot
        - hotspot_1_url (str): URL of the second hotspot
        - hotspot_1_metrics_views (int): View count for the second hotspot
        - hotspot_1_metrics_comments (int): Comment count for the second hotspot
        - update_time (str): ISO 8601 timestamp when data was fetched
        - source (str): Source platform identifier
        - total_count (int): Total number of hotspot items returned
        - metadata_status (str): Request status (e.g., "success")
        - metadata_api_version (str): API version used
        - metadata_refresh_interval (int): Refresh interval in seconds
    """
    return {
        "hotspot_0_title": "小米发布全新折叠屏手机",
        "hotspot_0_rank": 1,
        "hotspot_0_url": "https://www.huxiu.com/article/123456.html",
        "hotspot_0_metrics_views": 150000,
        "hotspot_0_metrics_comments": 2340,
        "hotspot_1_title": "特斯拉宣布降价引发市场震荡",
        "hotspot_1_rank": 2,
        "hotspot_1_url": "https://www.huxiu.com/article/123457.html",
        "hotspot_1_metrics_views": 120000,
        "hotspot_1_metrics_comments": 1890,
        "update_time": datetime.now().isoformat(),
        "source": "huxiu.com",
        "total_count": 2,
        "metadata_status": "success",
        "metadata_api_version": "v1",
        "metadata_refresh_interval": 300,
    }


def pulse_cn_mcp_server_huxiu_hotspots() -> Dict[str, Any]:
    """
    Fetches the trending hotspots from Huxiu.com via an external API simulation.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of hotspot entries with title, rank, URL, and metrics
        - update_time (str): ISO 8601 timestamp of data fetch
        - source (str): Source platform name
        - total_count (int): Number of hotspots returned
        - metadata (Dict): Additional context like status, API version, and refresh interval
    """
    try:
        api_data = call_external_api("pulse-cn-mcp-server-huxiu-hotspots")

        hotspots = [
            {
                "title": api_data["hotspot_0_title"],
                "rank": api_data["hotspot_0_rank"],
                "url": api_data["hotspot_0_url"],
                "metrics": {
                    "views": api_data["hotspot_0_metrics_views"],
                    "comments": api_data["hotspot_0_metrics_comments"]
                }
            },
            {
                "title": api_data["hotspot_1_title"],
                "rank": api_data["hotspot_1_rank"],
                "url": api_data["hotspot_1_url"],
                "metrics": {
                    "views": api_data["hotspot_1_metrics_views"],
                    "comments": api_data["hotspot_1_metrics_comments"]
                }
            }
        ]

        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "source": api_data["source"],
            "total_count": api_data["total_count"],
            "metadata": {
                "status": api_data["metadata_status"],
                "api_version": api_data["metadata_api_version"],
                "refresh_interval": api_data["metadata_refresh_interval"]
            }
        }

        return result

    except KeyError as e:
        return {
            "hotspots": [],
            "update_time": datetime.now().isoformat(),
            "source": "huxiu.com",
            "total_count": 0,
            "metadata": {
                "status": "error",
                "api_version": "v1",
                "refresh_interval": 300,
                "error": f"Missing field: {str(e)}"
            }
        }
    except Exception as e:
        return {
            "hotspots": [],
            "update_time": datetime.now().isoformat(),
            "source": "huxiu.com",
            "total_count": 0,
            "metadata": {
                "status": "error",
                "api_version": "v1",
                "refresh_interval": 300,
                "error": str(e)
            }
        }