from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for insect tribe hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspots_0_rank (int): Rank of the first trending topic
        - hotspots_0_topic (str): Name of the first trending topic
        - hotspots_0_popularity (int): Popularity score of the first topic
        - hotspots_0_timestamp (str): ISO timestamp for the first topic
        - hotspots_1_rank (int): Rank of the second trending topic
        - hotspots_1_topic (str): Name of the second trending topic
        - hotspots_1_popularity (int): Popularity score of the second topic
        - hotspots_1_timestamp (str): ISO timestamp for the second topic
        - last_updated (str): ISO 8601 timestamp when data was last refreshed
        - total_count (int): Total number of hotspot entries returned
        - source (str): Identifier for the data source
        - metadata_api_version (str): Version of the API
        - metadata_region (str): Geographic region of the data
        - metadata_update_frequency (str): How often data is updated
    """
    return {
        "hotspots_0_rank": 1,
        "hotspots_0_topic": "Ant Colony Expansion Tactics",
        "hotspots_0_popularity": 9876,
        "hotspots_0_timestamp": "2023-10-05T08:00:00Z",
        "hotspots_1_rank": 2,
        "hotspots_1_topic": "Bee Hive Communication Breakthrough",
        "hotspots_1_popularity": 8765,
        "hotspots_1_timestamp": "2023-10-05T07:30:00Z",
        "last_updated": "2023-10-05T08:15:00Z",
        "total_count": 2,
        "source": "insect-tribe-pulse-api",
        "metadata_api_version": "v1.2",
        "metadata_region": "CN",
        "metadata_update_frequency": "realtime"
    }


def pulse_cn_mcp_server_insect_hotspots() -> Dict[str, Any]:
    """
    获取虫族部落热搜榜单，返回包含热点内容的实时数据。

    This function retrieves real-time trending topics related to insect tribes
    by querying an external API simulation. It processes the flat response
    into a structured format with nested objects and lists as defined in the schema.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending topics with rank, name, popularity, and timestamp
        - last_updated (str): ISO 8601 timestamp of last refresh
        - total_count (int): Number of hotspot entries
        - source (str): Data source identifier
        - metadata (Dict): Additional context including API version, region, and update frequency
    """
    try:
        # Call external API to get flat data
        api_data = call_external_api("pulse-cn-mcp-server-insect-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "rank": api_data["hotspots_0_rank"],
                "topic": api_data["hotspots_0_topic"],
                "popularity": api_data["hotspots_0_popularity"],
                "timestamp": api_data["hotspots_0_timestamp"]
            },
            {
                "rank": api_data["hotspots_1_rank"],
                "topic": api_data["hotspots_1_topic"],
                "popularity": api_data["hotspots_1_popularity"],
                "timestamp": api_data["hotspots_1_timestamp"]
            }
        ]

        # Construct metadata dictionary
        metadata = {
            "api_version": api_data["metadata_api_version"],
            "region": api_data["metadata_region"],
            "update_frequency": api_data["metadata_update_frequency"]
        }

        # Build final result structure
        result = {
            "hotspots": hotspots,
            "last_updated": api_data["last_updated"],
            "total_count": api_data["total_count"],
            "source": api_data["source"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise ValueError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve or process insect hotspots data: {str(e)}") from e