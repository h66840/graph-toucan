from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Zhihu Daily hotspots.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - hotspot_0_title (str): Title of the first trending topic
        - hotspot_0_rank (int): Rank of the first trending topic
        - hotspot_0_heat (int): Popularity score (heat) of the first topic
        - hotspot_0_url (str): URL link to the first topic
        - hotspot_1_title (str): Title of the second trending topic
        - hotspot_1_rank (int): Rank of the second trending topic
        - hotspot_1_heat (int): Popularity score (heat) of the second topic
        - hotspot_1_url (str): URL link to the second topic
        - update_time (str): Timestamp when data was last updated, in ISO 8601 format
        - total_count (int): Total number of hotspots returned
        - source (str): Source platform name, e.g., 'Zhihu Daily'
        - has_more (bool): Whether more hotspots are available beyond current list
        - metadata_api_version (str): Version of the API used
        - metadata_status (str): Request status (e.g., 'success')
        - metadata_freshness (str): Indicator of data freshness (e.g., 'fresh')
    """
    return {
        "hotspot_0_title": "年轻人为何越来越不敢结婚？",
        "hotspot_0_rank": 1,
        "hotspot_0_heat": 987654,
        "hotspot_0_url": "https://www.zhihu.com/hot/1",
        "hotspot_1_title": "AI 是否会取代人类程序员？",
        "hotspot_1_rank": 2,
        "hotspot_1_heat": 876543,
        "hotspot_1_url": "https://www.zhihu.com/hot/2",
        "update_time": datetime.now(timezone.utc).isoformat(),
        "total_count": 2,
        "source": "Zhihu Daily",
        "has_more": True,
        "metadata_api_version": "v1.2.3",
        "metadata_status": "success",
        "metadata_freshness": "fresh"
    }


def pulse_cn_mcp_server_zhihu_daily_hotspots() -> Dict[str, Any]:
    """
    Fetches and returns the Zhihu Daily trending topics list with detailed information.

    This function simulates retrieving real-time Zhihu Daily hotspots through an external API.
    It processes flat scalar data from the API into a structured nested format as per schema.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending topics with title, rank, heat, and URL
        - update_time (str): ISO 8601 timestamp of last update
        - total_count (int): Number of hotspots in current response
        - source (str): Origin platform name
        - has_more (bool): Indicates if additional pages exist
        - metadata (Dict): Additional context like API version, status, and freshness
    """
    try:
        # Call external API to get flattened data
        api_data = call_external_api("pulse-cn-mcp-server-zhihu-daily-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "title": api_data["hotspot_0_title"],
                "rank": api_data["hotspot_0_rank"],
                "heat": api_data["hotspot_0_heat"],
                "url": api_data["hotspot_0_url"]
            },
            {
                "title": api_data["hotspot_1_title"],
                "rank": api_data["hotspot_1_rank"],
                "heat": api_data["hotspot_1_heat"],
                "url": api_data["hotspot_1_url"]
            }
        ]

        # Construct metadata dictionary
        metadata = {
            "api_version": api_data["metadata_api_version"],
            "status": api_data["metadata_status"],
            "freshness": api_data["metadata_freshness"]
        }

        # Assemble final result matching output schema
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "total_count": api_data["total_count"],
            "source": api_data["source"],
            "has_more": api_data["has_more"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise ValueError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to process Zhihu Daily hotspots data: {str(e)}") from e