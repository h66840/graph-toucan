from typing import Dict, List, Any
from datetime import datetime, timezone

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Weibo hotspots.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - hotspot_0_rank (int): Rank of the first trending topic
        - hotspot_0_title (str): Title of the first trending topic
        - hotspot_0_heat (int): Heat value of the first trending topic
        - hotspot_1_rank (int): Rank of the second trending topic
        - hotspot_1_title (str): Title of the second trending topic
        - hotspot_1_heat (int): Heat value of the second trending topic
        - update_time (str): ISO 8601 timestamp when data was fetched
        - source (str): Source of the data, e.g., 'weibo.com'
        - total_count (int): Total number of hot topics returned (here, 2)
    """
    return {
        "hotspot_0_rank": 1,
        "hotspot_0_title": "China National Day Celebration",
        "hotspot_0_heat": 9876543,
        "hotspot_1_rank": 2,
        "hotspot_1_title": "New Panda Born in Zoo",
        "hotspot_1_heat": 8765432,
        "update_time": "2024-05-20T12:34:56Z",
        "source": "weibo.com",
        "total_count": 2
    }

def pulse_cn_mcp_server_get_weibo_hotspots() -> Dict[str, Any]:
    """
    Fetches the latest Weibo trending topics (hotspots) by simulating an API call.
    
    This function retrieves real-time Weibo hot topic data including rank, topic title,
    and heat value. It constructs the response from flattened external API data
    into the required nested structure.

    Returns:
        Dict containing:
        - hotspots (List[Dict]): List of current Weibo hot topics with rank, title, and heat.
        - update_time (str): ISO 8601 timestamp indicating when data was updated.
        - source (str): Attribution of the data source.
        - total_count (int): Number of hot topics in the list.
    
    Example:
        {
            "hotspots": [
                {"rank": 1, "title": "Topic A", "heat": 1000000},
                {"rank": 2, "title": "Topic B", "heat": 900000}
            ],
            "update_time": "2024-05-20T12:34:56Z",
            "source": "weibo.com",
            "total_count": 2
        }
    """
    try:
        # Call the simulated external API
        api_data = call_external_api("pulse-cn-mcp-server-get-weibo-hotspots")

        # Construct the hotspots list from indexed fields
        hotspots = [
            {
                "rank": api_data["hotspot_0_rank"],
                "title": api_data["hotspot_0_title"],
                "heat": api_data["hotspot_0_heat"]
            },
            {
                "rank": api_data["hotspot_1_rank"],
                "title": api_data["hotspot_1_title"],
                "heat": api_data["hotspot_1_heat"]
            }
        ]

        # Build final result matching output schema
        result = {
            "hotspots": hotspots,
            "update_time": api_data["update_time"],
            "source": api_data["source"],
            "total_count": api_data["total_count"]
        }

        return result

    except KeyError as e:
        # Handle missing expected fields
        raise RuntimeError(f"Missing required field in API response: {str(e)}") from e
    except Exception as e:
        # Handle any other unforeseen errors
        raise RuntimeError(f"Failed to retrieve Weibo hotspots: {str(e)}") from e