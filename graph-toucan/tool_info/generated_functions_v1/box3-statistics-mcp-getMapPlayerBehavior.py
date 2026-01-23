from typing import Dict, List, Any
from datetime import datetime, timedelta
import random
import string

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for map player behavior statistics.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - player_behavior_stats_total_sessions (int): Total number of player sessions
        - player_behavior_stats_avg_play_time_seconds (float): Average play time in seconds
        - player_behavior_stats_unique_players (int): Number of unique players
        - player_behavior_stats_most_active_hour (int): Most active hour (0-23)
        - player_behavior_stats_completion_rate (float): Map completion rate (0-1)
        - behavior_timeline_0_timestamp (str): Timestamp for first timeline entry
        - behavior_timeline_0_active_players (int): Active players at that time
        - behavior_timeline_0_session_count (int): Number of sessions at that time
        - behavior_timeline_0_average_duration_seconds (float): Average duration in seconds
        - top_interacted_elements_0_element_id (str): ID of top interacted element
        - top_interacted_elements_0_element_name (str): Name of top interacted element
        - top_interacted_elements_0_interaction_count (int): Number of interactions
        - top_interacted_elements_0_avg_time_spent_seconds (float): Average time spent on element
        - player_retention_day_1_retention_rate (float): Day 1 retention rate (0-1)
        - player_retention_day_3_retention_rate (float): Day 3 retention rate (0-1)
        - player_retention_day_7_retention_rate (float): Day 7 retention rate (0-1)
        - player_retention_churn_rate (float): Churn rate (0-1)
        - geographic_distribution_0_country (str): Country name
        - geographic_distribution_0_region (str): Region name
        - geographic_distribution_0_player_count (int): Number of players in region
        - geographic_distribution_0_total_play_time_seconds (int): Total play time in region
        - device_platforms_0_platform (str): Device platform (e.g., Windows, Android)
        - device_platforms_0_user_count (int): Number of users on platform
        - device_platforms_0_avg_session_length_seconds (float): Average session length
        - device_platforms_0_interaction_density (float): Interaction density score
        - error_encounters_total_error_events (int): Total number of error events
        - error_encounters_common_errors_0_error_type (str): Type of most common error
        - error_encounters_common_errors_0_frequency (int): Frequency of this error
        - error_encounters_common_errors_0_affected_players (int): Number of affected players
        - error_encounters_high_friction_zones_0_zone_id (str): ID of high friction zone
        - error_encounters_high_friction_zones_0_zone_name (str): Name of high friction zone
        - error_encounters_high_friction_zones_0_issue_type (str): Type of issue in zone
        - metadata_request_id (str): Unique request identifier
        - metadata_generated_at (str): ISO timestamp when data was generated
        - metadata_time_range_start (str): Start of time range (ISO format)
        - metadata_time_range_end (str): End of time range (ISO format)
        - metadata_map_id (str): Map ID for which data was retrieved
        - metadata_data_coverage_status (str): Status of data coverage (e.g., complete, partial)
    """
    # Generate deterministic request ID based on tool name
    request_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    now = datetime.utcnow().isoformat() + 'Z'
    
    return {
        "player_behavior_stats_total_sessions": random.randint(500, 5000),
        "player_behavior_stats_avg_play_time_seconds": round(random.uniform(300, 1800), 2),
        "player_behavior_stats_unique_players": random.randint(200, 2000),
        "player_behavior_stats_most_active_hour": random.randint(0, 23),
        "player_behavior_stats_completion_rate": round(random.uniform(0.1, 0.9), 3),
        "behavior_timeline_0_timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
        "behavior_timeline_0_active_players": random.randint(50, 500),
        "behavior_timeline_0_session_count": random.randint(100, 1000),
        "behavior_timeline_0_average_duration_seconds": round(random.uniform(200, 1200), 2),
        "top_interacted_elements_0_element_id": f"elem_{random.randint(1000, 9999)}",
        "top_interacted_elements_0_element_name": f"Interactive Object {random.randint(1, 10)}",
        "top_interacted_elements_0_interaction_count": random.randint(100, 5000),
        "top_interacted_elements_0_avg_time_spent_seconds": round(random.uniform(10, 300), 2),
        "player_retention_day_1_retention_rate": round(random.uniform(0.1, 0.5), 3),
        "player_retention_day_3_retention_rate": round(random.uniform(0.05, 0.3), 3),
        "player_retention_day_7_retention_rate": round(random.uniform(0.02, 0.2), 3),
        "player_retention_churn_rate": round(random.uniform(0.3, 0.8), 3),
        "geographic_distribution_0_country": "China",
        "geographic_distribution_0_region": "Shanghai",
        "geographic_distribution_0_player_count": random.randint(100, 1000),
        "geographic_distribution_0_total_play_time_seconds": random.randint(10000, 1000000),
        "device_platforms_0_platform": random.choice(["Windows", "Android", "iOS"]),
        "device_platforms_0_user_count": random.randint(50, 500),
        "device_platforms_0_avg_session_length_seconds": round(random.uniform(300, 1500), 2),
        "device_platforms_0_interaction_density": round(random.uniform(1.0, 10.0), 2),
        "error_encounters_total_error_events": random.randint(0, 100),
        "error_encounters_common_errors_0_error_type": random.choice(["Timeout", "Crash", "Freeze", "ConnectionLost"]),
        "error_encounters_common_errors_0_frequency": random.randint(1, 50),
        "error_encounters_common_errors_0_affected_players": random.randint(1, 30),
        "error_encounters_high_friction_zones_0_zone_id": f"zone_{random.randint(100, 999)}",
        "error_encounters_high_friction_zones_0_zone_name": f"Difficult Area {random.randint(1, 5)}",
        "error_encounters_high_friction_zones_0_issue_type": random.choice(["NavigationBlock", "PerformanceDrop", "InteractionFailure"]),
        "metadata_request_id": request_id,
        "metadata_generated_at": now,
        "metadata_time_range_start": "2025-03-29T00:00:00Z",
        "metadata_time_range_end": "2025-04-04T23:59:59Z",
        "metadata_map_id": "map_12345",
        "metadata_data_coverage_status": random.choice(["complete", "partial"])
    }

def box3_statistics_mcp_getMapPlayerBehavior(
    endTime: str,
    mapId: str,
    startTime: str,
    token: str,
    userAgent: str
) -> Dict[str, Any]:
    """
    获取神岛平台用户地图玩家行为，需Token和用户请求头和地图ID
    
    该函数查询指定时间段内特定地图的玩家行为统计数据，包括玩家行为聚合指标、
    时间序列活动模式、交互热点元素、玩家留存率、地理分布、设备平台分布、
    错误遭遇情况以及响应元数据。
    
    Parameters:
        endTime (str): 结束时间，格式为YYYY-MM-DD，例如：2025-04-04
        mapId (str): 地图ID，标识要查询的地图
        startTime (str): 开始时间，格式为YYYY-MM-DD，例如：2025-03-29
        token (str): 认证Token，用于身份验证
        userAgent (str): 用户请求头，用于识别客户端
    
    Returns:
        Dict containing the following keys:
        - player_behavior_stats (Dict): 包含玩家行为聚合统计信息
        - behavior_timeline (List[Dict]): 时间序列数据，显示每日或每小时玩家活动模式
        - top_interacted_elements (List[Dict]): 玩家交互最多的地图元素列表
        - player_retention (Dict): 玩家返回地图的留存率指标
        - geographic_distribution (List[Dict]): 按地理区域划分的玩家活动分布
        - device_platforms (List[Dict]): 跨设备类型的玩家行为分布
        - error_encounters (Dict): 玩家遇到的错误或障碍摘要
        - metadata (Dict): 关于响应本身的信息
    
    Raises:
        ValueError: 当输入参数格式不正确或缺失必要参数时抛出
    """
    # Input validation
    if not endTime:
        raise ValueError("endTime is required")
    if not mapId:
        raise ValueError("mapId is required")
    if not startTime:
        raise ValueError("startTime is required")
    if not token:
        raise ValueError("token is required")
    if not userAgent:
        raise ValueError("userAgent is required")
    
    # Validate date format
    try:
        start_dt = datetime.strptime(startTime, "%Y-%m-%d")
        end_dt = datetime.strptime(endTime, "%Y-%m-%d")
        if start_dt > end_dt:
            raise ValueError("startTime must be earlier than or equal to endTime")
    except ValueError as e:
        if "time data" in str(e):
            raise ValueError("startTime and endTime must be in YYYY-MM-DD format")
        else:
            raise e
    
    # Call external API to get flattened data
    api_data = call_external_api("box3-statistics-mcp-getMapPlayerBehavior")
    
    # Construct nested output structure from flattened API data
    result = {
        "player_behavior_stats": {
            "total_sessions": api_data["player_behavior_stats_total_sessions"],
            "avg_play_time_seconds": api_data["player_behavior_stats_avg_play_time_seconds"],
            "unique_players": api_data["player_behavior_stats_unique_players"],
            "most_active_hour": api_data["player_behavior_stats_most_active_hour"],
            "completion_rate": api_data["player_behavior_stats_completion_rate"]
        },
        "behavior_timeline": [
            {
                "timestamp": api_data["behavior_timeline_0_timestamp"],
                "active_players": api_data["behavior_timeline_0_active_players"],
                "session_count": api_data["behavior_timeline_0_session_count"],
                "average_duration_seconds": api_data["behavior_timeline_0_average_duration_seconds"]
            }
        ],
        "top_interacted_elements": [
            {
                "element_id": api_data["top_interacted_elements_0_element_id"],
                "element_name": api_data["top_interacted_elements_0_element_name"],
                "interaction_count": api_data["top_interacted_elements_0_interaction_count"],
                "avg_time_spent_seconds": api_data["top_interacted_elements_0_avg_time_spent_seconds"]
            }
        ],
        "player_retention": {
            "day_1_retention_rate": api_data["player_retention_day_1_retention_rate"],
            "day_3_retention_rate": api_data["player_retention_day_3_retention_rate"],
            "day_7_retention_rate": api_data["player_retention_day_7_retention_rate"],
            "churn_rate": api_data["player_retention_churn_rate"]
        },
        "geographic_distribution": [
            {
                "country": api_data["geographic_distribution_0_country"],
                "region": api_data["geographic_distribution_0_region"],
                "player_count": api_data["geographic_distribution_0_player_count"],
                "total_play_time_seconds": api_data["geographic_distribution_0_total_play_time_seconds"]
            }
        ],
        "device_platforms": [
            {
                "platform": api_data["device_platforms_0_platform"],
                "user_count": api_data["device_platforms_0_user_count"],
                "avg_session_length_seconds": api_data["device_platforms_0_avg_session_length_seconds"],
                "interaction_density": api_data["device_platforms_0_interaction_density"]
            }
        ],
        "error_encounters": {
            "total_error_events": api_data["error_encounters_total_error_events"],
            "common_errors": [
                {
                    "error_type": api_data["error_encounters_common_errors_0_error_type"],
                    "frequency": api_data["error_encounters_common_errors_0_frequency"],
                    "affected_players": api_data["error_encounters_common_errors_0_affected_players"]
                }
            ],
            "high_friction_zones": [
                {
                    "zone_id": api_data["error_encounters_high_friction_zones_0_zone_id"],
                    "zone_name": api_data["error_encounters_high_friction_zones_0_zone_name"],
                    "issue_type": api_data["error_encounters_high_friction_zones_0_issue_type"]
                }
            ]
        },
        "metadata": {
            "request_id": api_data["metadata_request_id"],
            "generated_at": api_data["metadata_generated_at"],
            "time_range": {
                "start": api_data["metadata_time_range_start"],
                "end": api_data["metadata_time_range_end"]
            },
            "map_id": api_data["metadata_map_id"],
            "data_coverage_status": api_data["metadata_data_coverage_status"]
        }
    }
    
    return result