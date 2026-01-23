from typing import Dict, List, Any
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bilibili daily hotspots.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hotspots_0_rank (int): Rank of the first trending item
        - hotspots_0_title (str): Title of the first trending video
        - hotspots_0_video_url (str): URL of the first video
        - hotspots_0_play_count (int): Play count of the first video
        - hotspots_0_danmu_count (int): Danmu (comment) count of the first video
        - hotspots_0_author (str): Author name of the first video
        - hotspots_0_upload_time (str): Upload time of the first video in ISO format
        - hotspots_0_cover_image_url (str): Cover image URL of the first video
        - hotspots_1_rank (int): Rank of the second trending item
        - hotspots_1_title (str): Title of the second trending video
        - hotspots_1_video_url (str): URL of the second video
        - hotspots_1_play_count (int): Play count of the second video
        - hotspots_1_danmu_count (int): Danmu (comment) count of the second video
        - hotspots_1_author (str): Author name of the second video
        - hotspots_1_upload_time (str): Upload time of the second video in ISO format
        - hotspots_1_cover_image_url (str): Cover image URL of the second video
        - update_time (str): ISO 8601 timestamp when data was fetched
        - total_count (int): Total number of items in the daily ranking list
        - metadata_source_platform (str): Source platform name (e.g., 'Bilibili')
        - metadata_list_type (str): Type of list (e.g., 'daily_hot')
        - metadata_request_status (str): Status of the request (e.g., 'success')
    """
    return {
        "hotspots_0_rank": 1,
        "hotspots_0_title": "【2024年度神曲】全网爆火的洗脑神曲合集！听完根本停不下来！",
        "hotspots_0_video_url": "https://www.bilibili.com/video/BV1Aa4y1p7Jz",
        "hotspots_0_play_count": 8234567,
        "hotspots_0_danmu_count": 124500,
        "hotspots_0_author": "音乐雷达MusicRadar",
        "hotspots_0_upload_time": "2024-03-15T10:30:00Z",
        "hotspots_0_cover_image_url": "https://i0.hdslb.com/bfs/archive/abc123.jpg",
        "hotspots_1_rank": 2,
        "hotspots_1_title": "【硬核科技】小米SU7 vs 特斯拉Model 3 全面对比测评",
        "hotspots_1_video_url": "https://www.bilibili.com/video/BV1Xa4y1p7Km",
        "hotspots_1_play_count": 6987321,
        "hotspots_1_danmu_count": 98200,
        "hotspots_1_author": "科技美学",
        "hotspots_1_upload_time": "2024-03-14T18:45:00Z",
        "hotspots_1_cover_image_url": "https://i0.hdslb.com/bfs/archive/def456.jpg",
        "update_time": "2024-03-16T08:00:00Z",
        "total_count": 100,
        "metadata_source_platform": "Bilibili",
        "metadata_list_type": "daily_hot",
        "metadata_request_status": "success"
    }


def pulse_cn_mcp_server_bilibili_daily_hotspots() -> Dict[str, Any]:
    """
    Fetches Bilibili's daily leaderboard data containing trending video information.

    This function simulates retrieving real-time hotspot data from Bilibili's API.
    It returns a structured response with trending items, update timestamp,
    total count, and metadata about the list.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending videos with details like rank, title,
          video URL, play count, danmu count, author, upload time, and cover image.
        - update_time (str): ISO 8601 timestamp indicating when the data was fetched.
        - total_count (int): Total number of entries in the daily ranking (typically 100).
        - metadata (Dict): Additional context including source platform, list type,
          and request status.

    Example:
        {
            "hotspots": [
                {
                    "rank": 1,
                    "title": "【2024年度神曲】全网爆火的洗脑神曲合集！...",
                    "video_url": "https://www.bilibili.com/video/BV1Aa4y1p7Jz",
                    "play_count": 8234567,
                    "danmu_count": 124500,
                    "author": "音乐雷达MusicRadar",
                    "upload_time": "2024-03-15T10:30:00Z",
                    "cover_image_url": "https://i0.hdslb.com/bfs/archive/abc123.jpg"
                },
                ...
            ],
            "update_time": "2024-03-16T08:00:00Z",
            "total_count": 100,
            "metadata": {
                "source_platform": "Bilibili",
                "list_type": "daily_hot",
                "request_status": "success"
            }
        }
    """
    try:
        # Call external API to get flattened data
        api_data = call_external_api("pulse-cn-mcp-server-bilibili-daily-hotspots")

        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "rank": api_data["hotspots_0_rank"],
                "title": api_data["hotspots_0_title"],
                "video_url": api_data["hotspots_0_video_url"],
                "play_count": api_data["hotspots_0_play_count"],
                "danmu_count": api_data["hotspots_0_danmu_count"],
                "author": api_data["hotspots_0_author"],
                "upload_time": api_data["hotspots_0_upload_time"],
                "cover_image_url": api_data["hotspots_0_cover_image_url"]
            },
            {
                "rank": api_data["hotspots_1_rank"],
                "title": api_data["hotspots_1_title"],
                "video_url": api_data["hotspots_1_video_url"],
                "play_count": api_data["hotspots_1_play_count"],
                "danmu_count": api_data["hotspots_1_danmu_count"],
                "author": api_data["hotspots_1_author"],
                "upload_time": api_data["hotspots_1_upload_time"],
                "cover_image_url": api_data["hotspots_1_cover_image_url"]
            }
        ]

        # Construct final result matching output schema
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "total_count": api_data["total_count"],
            "metadata": {
                "source_platform": api_data["metadata_source_platform"],
                "list_type": api_data["metadata_list_type"],
                "request_status": api_data["metadata_request_status"]
            }
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to process Bilibili daily hotspots data: {str(e)}") from e