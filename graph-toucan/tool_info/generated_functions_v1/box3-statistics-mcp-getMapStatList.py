from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for map statistics.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_0_map_id (str): ID of the first map
        - data_0_map_name (str): Name of the first map
        - data_0_user_count (int): Number of users on the first map
        - data_0_session_count (int): Number of sessions on the first map
        - data_0_total_duration (int): Total time spent on the first map in seconds
        - data_1_map_id (str): ID of the second map
        - data_1_map_name (str): Name of the second map
        - data_1_user_count (int): Number of users on the second map
        - data_1_session_count (int): Number of sessions on the second map
        - data_1_total_duration (int): Total time spent on the second map in seconds
        - totalCount (int): Total number of map statistic records
        - success (bool): Whether the request was successful
        - message (str): Result message
        - metadata_time_range_start (str): Start of applied time range
        - metadata_time_range_end (str): End of applied time range
        - metadata_timestamp (str): Server timestamp in ISO format
        - metadata_has_next_page (bool): Whether more pages exist
        - metadata_has_prev_page (bool): Whether previous page exists
    """
    return {
        "data_0_map_id": "map_001",
        "data_0_map_name": "Central Island",
        "data_0_user_count": 150,
        "data_0_session_count": 320,
        "data_0_total_duration": 45600,
        "data_1_map_id": "map_002",
        "data_1_map_name": "Northern Forest",
        "data_1_user_count": 98,
        "data_1_session_count": 210,
        "data_1_total_duration": 31200,
        "totalCount": 2,
        "success": True,
        "message": "Success",
        "metadata_time_range_start": "2025-03-29",
        "metadata_time_range_end": "2025-04-04",
        "metadata_timestamp": "2025-04-05T10:00:00Z",
        "metadata_has_next_page": False,
        "metadata_has_prev_page": False
    }

def box3_statistics_mcp_getMapStatList(
    endTime: str,
    startTime: str,
    token: str,
    userAgent: str
) -> Dict[str, Any]:
    """
    获取神岛平台用户地图统计列表，需Token和用户请求头

    Args:
        endTime (str): 结束时间，例如：2025-04-04
        startTime (str): 开始时间，例如：2025-03-29
        token (str): 认证Token
        userAgent (str): 用户请求头

    Returns:
        Dict containing:
        - data (List[Dict]): List of map statistics entries, each containing details about user activity on a specific map
        - totalCount (int): Total number of map statistic records returned in the response
        - success (bool): Indicates whether the request was processed successfully
        - message (str): Human-readable message describing the result, e.g., 'Success' or error details
        - metadata (Dict): Additional contextual information such as applied time range, server timestamp, and pagination status
    """
    # Input validation
    if not endTime:
        return {
            "data": [],
            "totalCount": 0,
            "success": False,
            "message": "endTime is required",
            "metadata": {
                "time_range": {"start": startTime, "end": endTime},
                "timestamp": "1970-01-01T00:00:00Z",
                "has_next_page": False,
                "has_prev_page": False
            }
        }
    
    if not startTime:
        return {
            "data": [],
            "totalCount": 0,
            "success": False,
            "message": "startTime is required",
            "metadata": {
                "time_range": {"start": startTime, "end": endTime},
                "timestamp": "1970-01-01T00:00:00Z",
                "has_next_page": False,
                "has_prev_page": False
            }
        }
    
    if not token:
        return {
            "data": [],
            "totalCount": 0,
            "success": False,
            "message": "token is required",
            "metadata": {
                "time_range": {"start": startTime, "end": endTime},
                "timestamp": "1970-01-01T00:00:00Z",
                "has_next_page": False,
                "has_prev_page": False
            }
        }
    
    if not userAgent:
        return {
            "data": [],
            "totalCount": 0,
            "success": False,
            "message": "userAgent is required",
            "metadata": {
                "time_range": {"start": startTime, "end": endTime},
                "timestamp": "1970-01-01T00:00:00Z",
                "has_next_page": False,
                "has_prev_page": False
            }
        }

    # Call external API (simulated)
    api_data = call_external_api("box3-statistics-mcp-getMapStatList")

    # Construct data list from flattened fields
    data = [
        {
            "map_id": api_data["data_0_map_id"],
            "map_name": api_data["data_0_map_name"],
            "user_count": api_data["data_0_user_count"],
            "session_count": api_data["data_0_session_count"],
            "total_duration": api_data["data_0_total_duration"]
        },
        {
            "map_id": api_data["data_1_map_id"],
            "map_name": api_data["data_1_map_name"],
            "user_count": api_data["data_1_user_count"],
            "session_count": api_data["data_1_session_count"],
            "total_duration": api_data["data_1_total_duration"]
        }
    ]

    # Construct metadata
    metadata = {
        "time_range": {
            "start": api_data["metadata_time_range_start"],
            "end": api_data["metadata_time_range_end"]
        },
        "timestamp": api_data["metadata_timestamp"],
        "has_next_page": api_data["metadata_has_next_page"],
        "has_prev_page": api_data["metadata_has_prev_page"]
    }

    # Construct final result
    result = {
        "data": data,
        "totalCount": api_data["totalCount"],
        "success": api_data["success"],
        "message": api_data["message"],
        "metadata": metadata
    }

    return result