from typing import Dict, List, Any
from datetime import datetime, timezone
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching 36Kr 24-hour hotspots data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - hotspots_0_title (str): Title of the first trending item
        - hotspots_0_rank (int): Rank of the first trending item
        - hotspots_0_heat_score (float): Heat score of the first trending item
        - hotspots_0_url (str): URL of the first trending item
        - hotspots_1_title (str): Title of the second trending item
        - hotspots_1_rank (int): Rank of the second trending item
        - hotspots_1_heat_score (float): Heat score of the second trending item
        - hotspots_1_url (str): URL of the second trending item
        - update_time (str): ISO 8601 timestamp when data was last updated
        - source (str): Source platform name
        - total_count (int): Total number of hotspot entries returned
        - metadata_refresh_interval_minutes (int): Refresh interval in minutes
    """
    # Generate realistic mock data
    base_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    
    return {
        "hotspots_0_title": "AI大模型商业化加速，多家企业公布最新进展",
        "hotspots_0_rank": 1,
        "hotspots_0_heat_score": 9876.5,
        "hotspots_0_url": "https://36kr.com/hotspot/12345",
        "hotspots_1_title": "新能源汽车市场竞争加剧，新势力车企发布销量数据",
        "hotspots_1_rank": 2,
        "hotspots_1_heat_score": 8765.4,
        "hotspots_1_url": "https://36kr.com/hotspot/12346",
        "update_time": base_time,
        "source": "36Kr",
        "total_count": 2,
        "metadata_refresh_interval_minutes": 30
    }


def pulse_cn_mcp_server_36_krypton_24_hour_hotspots() -> Dict[str, Any]:
    """
    获取36氪24小时热搜榜单，返回包含热点内容的实时数据。
    
    This function retrieves trending items from 36Kr's 24-hour hot榜 by simulating
    an API call and transforming flat response data into structured nested output.
    
    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of trending items with title, rank, heat_score, and URL
        - update_time (str): ISO 8601 timestamp of last update
        - source (str): Source platform name ('36Kr')
        - total_count (int): Number of hotspot entries returned
        - metadata (Dict): Additional info like refresh interval
        
    Example:
        {
            "hotspots": [
                {
                    "title": "AI大模型商业化加速...",
                    "rank": 1,
                    "heat_score": 9876.5,
                    "url": "https://36kr.com/hotspot/12345"
                },
                ...
            ],
            "update_time": "2024-05-20T12:34:56Z",
            "source": "36Kr",
            "total_count": 2,
            "metadata": {
                "refresh_interval_minutes": 30
            }
        }
    """
    try:
        # Fetch simulated external data
        api_data = call_external_api("pulse-cn-mcp-server-36-krypton-24-hour-hotspots")
        
        # Construct hotspots list from indexed fields
        hotspots = [
            {
                "title": api_data["hotspots_0_title"],
                "rank": api_data["hotspots_0_rank"],
                "heat_score": api_data["hotspots_0_heat_score"],
                "url": api_data["hotspots_0_url"]
            },
            {
                "title": api_data["hotspots_1_title"],
                "rank": api_data["hotspots_1_rank"],
                "heat_score": api_data["hotspots_1_heat_score"],
                "url": api_data["hotspots_1_url"]
            }
        ]
        
        # Build final result structure
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "source": api_data["source"],
            "total_count": api_data["total_count"],
            "metadata": {
                "refresh_interval_minutes": api_data["metadata_refresh_interval_minutes"]
            }
        }
        
        return result
        
    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve or process 36Kr hotspots data: {str(e)}") from e