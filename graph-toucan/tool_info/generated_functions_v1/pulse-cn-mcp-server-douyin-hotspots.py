from typing import Dict, List, Any
from datetime import datetime, timezone


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Douyin hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspots_0_rank (int): Rank of the first trending topic
        - hotspots_0_keyword (str): Keyword of the first trending topic
        - hotspots_0_url (str): URL of the first trending topic
        - hotspots_0_heat (int): Heat score of the first trending topic
        - hotspots_0_is_trending_up (bool): Whether the first topic is trending up
        - hotspots_0_category (str): Category of the first trending topic
        - hotspots_1_rank (int): Rank of the second trending topic
        - hotspots_1_keyword (str): Keyword of the second trending topic
        - hotspots_1_url (str): URL of the second trending topic
        - hotspots_1_heat (int): Heat score of the second trending topic
        - hotspots_1_is_trending_up (bool): Whether the second topic is trending up
        - hotspots_1_category (str): Category of the second trending topic
        - update_time (str): ISO 8601 timestamp when data was updated
        - total_count (int): Total number of hotspot entries returned
        - source (str): Data source identifier
    """
    return {
        "hotspots_0_rank": 1,
        "hotspots_0_keyword": "Celebrity Dance Challenge",
        "hotspots_0_url": "https://www.douyin.com/hotspot/1001",
        "hotspots_0_heat": 12500000,
        "hotspots_0_is_trending_up": True,
        "hotspots_0_category": "Entertainment",
        "hotspots_1_rank": 2,
        "hotspots_1_keyword": "New Year Food Recipes",
        "hotspots_1_url": "https://www.douyin.com/hotspot/1002",
        "hotspots_1_heat": 9800000,
        "hotspots_1_is_trending_up": False,
        "hotspots_1_category": "Lifestyle",
        "update_time": "2024-05-20T12:34:56Z",
        "total_count": 2,
        "source": "douyin-api"
    }


def pulse_cn_mcp_server_douyin_hotspots() -> Dict[str, Any]:
    """
    Fetches real-time Douyin trending topics data via external API simulation.

    This function retrieves hotspot data including rank, keyword, URL, heat,
    trend direction, and category for each trending topic. It constructs
    a properly structured response from flattened API data.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending topics with detailed metadata
        - update_time (str): ISO 8601 timestamp of last update
        - total_count (int): Number of hotspot entries returned
        - source (str): Identifier for the data source

        Each hotspot dict includes:
        - rank (int): Ranking position (1-based)
        - keyword (str): Trending phrase or title
        - url (str): Direct link to content
        - heat (int): Popularity metric (e.g., view count)
        - is_trending_up (bool): Whether topic is gaining momentum
        - category (str): Topic classification (e.g., 'Entertainment', 'News')
    """
    try:
        # Call external API to get flattened data
        api_data = call_external_api("pulse-cn-mcp-server-douyin-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "rank": api_data["hotspots_0_rank"],
                "keyword": api_data["hotspots_0_keyword"],
                "url": api_data["hotspots_0_url"],
                "heat": api_data["hotspots_0_heat"],
                "is_trending_up": api_data["hotspots_0_is_trending_up"],
                "category": api_data["hotspots_0_category"]
            },
            {
                "rank": api_data["hotspots_1_rank"],
                "keyword": api_data["hotspots_1_keyword"],
                "url": api_data["hotspots_1_url"],
                "heat": api_data["hotspots_1_heat"],
                "is_trending_up": api_data["hotspots_1_is_trending_up"],
                "category": api_data["hotspots_1_category"]
            }
        ]

        # Build final result structure matching output schema
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "total_count": api_data["total_count"],
            "source": api_data["source"]
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to process Douyin hotspots data: {str(e)}") from e