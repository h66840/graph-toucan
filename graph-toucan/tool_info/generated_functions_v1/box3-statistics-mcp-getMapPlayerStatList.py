from typing import Dict, List, Any
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for map player statistics.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - player_0_playerId (str): Player ID of the first player
        - player_0_playCount (int): Number of times the first player played
        - player_0_totalPlayTime (int): Total play time in seconds for the first player
        - player_0_wins (int): Number of wins for the first player
        - player_0_kills (int): Total kills by the first player
        - player_0_deaths (int): Total deaths of the first player
        - player_0_kdRatio (float): Kill-death ratio of the first player
        - player_0_highestPerformance (int): Highest single-game performance score of the first player
        - player_1_playerId (str): Player ID of the second player
        - player_1_playCount (int): Number of times the second player played
        - player_1_totalPlayTime (int): Total play time in seconds for the second player
        - player_1_wins (int): Number of wins for the second player
        - player_1_kills (int): Total kills by the second player
        - player_1_deaths (int): Total deaths of the second player
        - player_1_kdRatio (float): Kill-death ratio of the second player
        - player_1_highestPerformance (int): Highest single-game performance score of the second player
        - totalPlayers (int): Total number of players matching the criteria
        - timeRange_startTime (str): Start time of the query range
        - timeRange_endTime (str): End time of the query range
        - mapInfo_mapId (str): ID of the map
        - mapInfo_mapName (str): Name of the map
        - mapInfo_mapType (str): Type/category of the map
        - pagination_currentPage (int): Current page number
        - pagination_pageSize (int): Number of items per page
        - pagination_hasMore (bool): Whether more pages exist
        - pagination_totalCount (int): Total number of items across all pages
        - requestMetadata_requestTime (str): Timestamp when the request was processed
        - requestMetadata_statusCode (int): HTTP status code of the response
        - requestMetadata_processingTimeMs (int): Processing time in milliseconds
    """
    return {
        "player_0_playerId": "player_12345",
        "player_0_playCount": 15,
        "player_0_totalPlayTime": 5400,
        "player_0_wins": 8,
        "player_0_kills": 67,
        "player_0_deaths": 45,
        "player_0_kdRatio": 1.49,
        "player_0_highestPerformance": 92,
        "player_1_playerId": "player_67890",
        "player_1_playCount": 23,
        "player_1_totalPlayTime": 8280,
        "player_1_wins": 14,
        "player_1_kills": 103,
        "player_1_deaths": 76,
        "player_1_kdRatio": 1.35,
        "player_1_highestPerformance": 98,
        "totalPlayers": 2,
        "timeRange_startTime": "2025-03-29",
        "timeRange_endTime": "2025-04-04",
        "mapInfo_mapId": "map_001",
        "mapInfo_mapName": "Dragon's Peak",
        "mapInfo_mapType": "Battle Royale",
        "pagination_currentPage": 1,
        "pagination_pageSize": 20,
        "pagination_hasMore": False,
        "pagination_totalCount": 2,
        "requestMetadata_requestTime": datetime.datetime.utcnow().isoformat(),
        "requestMetadata_statusCode": 200,
        "requestMetadata_processingTimeMs": 125
    }


def box3_statistics_mcp_getMapPlayerStatList(
    endTime: str,
    mapId: str,
    startTime: str,
    token: str,
    userAgent: str
) -> Dict[str, Any]:
    """
    获取神岛平台用户地图玩家统计，需Token和用户请求头和地图ID

    Parameters:
        endTime (str): 结束时间，例如：2025-04-04
        mapId (str): 地图ID
        startTime (str): 开始时间，例如：2025-03-29
        token (str): 认证Token
        userAgent (str): 用户请求头

    Returns:
        Dict containing:
        - playerStats (List[Dict]): 列表，包含每个玩家在指定地图上的统计信息
        - totalPlayers (int): 符合条件的总玩家数量
        - timeRange (Dict): 查询的时间范围
        - mapInfo (Dict): 地图基本信息
        - pagination (Dict): 分页信息
        - requestMetadata (Dict): 请求元数据
    """
    # Input validation
    if not all([endTime, mapId, startTime, token, userAgent]):
        raise ValueError("All parameters (endTime, mapId, startTime, token, userAgent) are required.")
    
    try:
        # Validate date format
        datetime.datetime.fromisoformat(endTime)
        datetime.datetime.fromisoformat(startTime)
    except ValueError as e:
        raise ValueError(f"Invalid date format: {e}")

    # Call external API (simulated)
    api_data = call_external_api("box3-statistics-mcp-getMapPlayerStatList")

    # Construct playerStats list from indexed fields
    player_stats = [
        {
            "playerId": api_data["player_0_playerId"],
            "playCount": api_data["player_0_playCount"],
            "totalPlayTime": api_data["player_0_totalPlayTime"],
            "wins": api_data["player_0_wins"],
            "kills": api_data["player_0_kills"],
            "deaths": api_data["player_0_deaths"],
            "kdRatio": api_data["player_0_kdRatio"],
            "highestPerformance": api_data["player_0_highestPerformance"]
        },
        {
            "playerId": api_data["player_1_playerId"],
            "playCount": api_data["player_1_playCount"],
            "totalPlayTime": api_data["player_1_totalPlayTime"],
            "wins": api_data["player_1_wins"],
            "kills": api_data["player_1_kills"],
            "deaths": api_data["player_1_deaths"],
            "kdRatio": api_data["player_1_kdRatio"],
            "highestPerformance": api_data["player_1_highestPerformance"]
        }
    ]

    # Construct result according to output schema
    result = {
        "playerStats": player_stats,
        "totalPlayers": api_data["totalPlayers"],
        "timeRange": {
            "startTime": api_data["timeRange_startTime"],
            "endTime": api_data["timeRange_endTime"]
        },
        "mapInfo": {
            "mapId": api_data["mapInfo_mapId"],
            "mapName": api_data["mapInfo_mapName"],
            "mapType": api_data["mapInfo_mapType"]
        },
        "pagination": {
            "currentPage": api_data["pagination_currentPage"],
            "pageSize": api_data["pagination_pageSize"],
            "hasMore": api_data["pagination_hasMore"],
            "totalCount": api_data["pagination_totalCount"]
        },
        "requestMetadata": {
            "requestTime": api_data["requestMetadata_requestTime"],
            "statusCode": api_data["requestMetadata_statusCode"],
            "processingTimeMs": api_data["requestMetadata_processingTimeMs"]
        }
    }

    return result