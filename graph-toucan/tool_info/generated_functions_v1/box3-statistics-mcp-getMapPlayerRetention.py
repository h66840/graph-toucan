from typing import Dict, List, Any
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for map player retention statistics.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - retention_0_date (str): First retention record date
        - retention_0_new_players (int): Number of new players on first date
        - retention_0_day1_rate (float): Day 1 retention rate for first date
        - retention_0_day7_rate (float): Day 7 retention rate for first date
        - retention_0_day30_rate (float): Day 30 retention rate for first date
        - retention_1_date (str): Second retention record date
        - retention_1_new_players (int): Number of new players on second date
        - retention_1_day1_rate (float): Day 1 retention rate for second date
        - retention_1_day7_rate (float): Day 7 retention rate for second date
        - retention_1_day30_rate (float): Day 30 retention rate for second date
        - time_range_start (str): Start date of the report
        - time_range_end (str): End date of the report
        - map_info_map_id (str): Map ID
        - map_info_name (str): Map name
        - map_info_creator (str): Map creator username
        - summary_metrics_avg_day1 (float): Average Day 1 retention rate
        - summary_metrics_avg_day7 (float): Average Day 7 retention rate
        - summary_metrics_avg_day30 (float): Average Day 30 retention rate
        - summary_metrics_total_new_players (int): Total new players across period
        - summary_metrics_trend (str): Overall trend direction ("up", "down", "stable")
        - request_metadata_query_timestamp (str): ISO format timestamp of query
        - request_metadata_data_complete (bool): Whether data is complete
    """
    start_date = "2025-03-29"
    end_date = "2025-04-04"
    now_iso = datetime.now().isoformat()

    return {
        "retention_0_date": start_date,
        "retention_0_new_players": 1250,
        "retention_0_day1_rate": round(random.uniform(0.35, 0.55), 3),
        "retention_0_day7_rate": round(random.uniform(0.15, 0.25), 3),
        "retention_0_day30_rate": round(random.uniform(0.05, 0.12), 3),
        "retention_1_date": "2025-03-30",
        "retention_1_new_players": 1320,
        "retention_1_day1_rate": round(random.uniform(0.35, 0.55), 3),
        "retention_1_day7_rate": round(random.uniform(0.15, 0.25), 3),
        "retention_1_day30_rate": round(random.uniform(0.05, 0.12), 3),
        "time_range_start": start_date,
        "time_range_end": end_date,
        "map_info_map_id": "map_12345",
        "map_info_name": "Mystery Island",
        "map_info_creator": "creator_user_789",
        "summary_metrics_avg_day1": round(random.uniform(0.40, 0.50), 3),
        "summary_metrics_avg_day7": round(random.uniform(0.18, 0.24), 3),
        "summary_metrics_avg_day30": round(random.uniform(0.06, 0.10), 3),
        "summary_metrics_total_new_players": 8750,
        "summary_metrics_trend": random.choice(["up", "down", "stable"]),
        "request_metadata_query_timestamp": now_iso,
        "request_metadata_data_complete": True,
    }


def box3_statistics_mcp_getMapPlayerRetention(
    endTime: str, mapId: str, startTime: str, token: str, userAgent: str
) -> Dict[str, Any]:
    """
    获取神岛平台用户地图玩家留存，需Token和用户请求头和地图ID

    Args:
        endTime (str): 结束时间，例如：2025-04-04
        mapId (str): 地图ID
        startTime (str): 开始时间，例如：2025-03-29
        token (str): 认证Token
        userAgent (str): 用户请求头

    Returns:
        Dict containing:
        - retentionData (List[Dict]): List of daily retention records with date and metrics
        - timeRange (Dict): Start and end dates of the report
        - mapInfo (Dict): Map information including ID, name, and creator
        - summaryMetrics (Dict): Aggregated statistics and trends
        - requestMetadata (Dict): Query timestamp and data completeness status

    Raises:
        ValueError: If required parameters are missing or invalid
    """
    # Input validation
    if not all([endTime, mapId, startTime, token, userAgent]):
        raise ValueError("All parameters (endTime, mapId, startTime, token, userAgent) are required")

    try:
        datetime.strptime(startTime, "%Y-%m-%d")
        datetime.strptime(endTime, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Invalid date format. Please use YYYY-MM-DD. Error: {str(e)}")

    if datetime.strptime(startTime, "%Y-%m-%d") > datetime.strptime(endTime, "%Y-%m-%d"):
        raise ValueError("startTime cannot be later than endTime")

    # Call external API to get flattened data
    api_data = call_external_api("box3-statistics-mcp-getMapPlayerRetention")

    # Construct retentionData list from indexed fields
    retention_data = [
        {
            "date": api_data["retention_0_date"],
            "new_players": api_data["retention_0_new_players"],
            "day1_retention_rate": api_data["retention_0_day1_rate"],
            "day7_retention_rate": api_data["retention_0_day7_rate"],
            "day30_retention_rate": api_data["retention_0_day30_rate"],
        },
        {
            "date": api_data["retention_1_date"],
            "new_players": api_data["retention_1_new_players"],
            "day1_retention_rate": api_data["retention_1_day1_rate"],
            "day7_retention_rate": api_data["retention_1_day7_rate"],
            "day30_retention_rate": api_data["retention_1_day30_rate"],
        },
    ]

    # Construct final result matching output schema
    result = {
        "retentionData": retention_data,
        "timeRange": {
            "start": api_data["time_range_start"],
            "end": api_data["time_range_end"],
        },
        "mapInfo": {
            "mapId": api_data["map_info_map_id"],
            "name": api_data["map_info_name"],
            "creator": api_data["map_info_creator"],
        },
        "summaryMetrics": {
            "average_day1_retention_rate": api_data["summary_metrics_avg_day1"],
            "average_day7_retention_rate": api_data["summary_metrics_avg_day7"],
            "average_day30_retention_rate": api_data["summary_metrics_avg_day30"],
            "total_new_players": api_data["summary_metrics_total_new_players"],
            "trend_direction": api_data["summary_metrics_trend"],
        },
        "requestMetadata": {
            "query_timestamp": api_data["request_metadata_query_timestamp"],
            "data_complete": api_data["request_metadata_data_complete"],
        },
    }

    return result