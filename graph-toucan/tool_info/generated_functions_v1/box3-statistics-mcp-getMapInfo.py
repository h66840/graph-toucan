from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching map information from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - mapName (str): Display name or title of the map
        - creatorId (str): Unique identifier of the user who created the map
        - creationTime (str): ISO 8601 timestamp indicating when the map was created
        - lastAccessedTime (str): ISO 8601 timestamp indicating the most recent access to the map
        - accessCount (int): Total number of times the map has been accessed or viewed
        - mapStatus (str): Current status of the map (e.g., active, archived, deleted)
        - version (str): Version identifier of the map data or configuration
        - isPublic (bool): Whether the map is publicly accessible
        - allowedUsers_0 (str): First allowed user ID
        - allowedUsers_1 (str): Second allowed user ID
        - allowedRoles_0 (str): First allowed role
        - allowedRoles_1 (str): Second allowed role
        - regionCoverage_0 (str): First geographic region covered
        - regionCoverage_1 (str): Second geographic region covered
        - tags_0 (str): First tag describing the map
        - tags_1 (str): Second tag describing the map
        - success (bool): Indicates whether the request was successful
        - error (str): Error message if the request failed; absent or null on success
    """
    # Generate realistic mock data based on mapId (tool_name is ignored here)
    now = datetime.utcnow()
    creation_time = now - timedelta(days=random.randint(1, 365))
    last_accessed = creation_time + timedelta(hours=random.randint(1, 1000))

    return {
        "mapName": f"Map_{random.randint(1000, 9999)}",
        "creatorId": f"usr_{random.randint(10000, 99999)}",
        "creationTime": creation_time.isoformat() + "Z",
        "lastAccessedTime": last_accessed.isoformat() + "Z",
        "accessCount": random.randint(0, 10000),
        "mapStatus": random.choice(["active", "archived"]),
        "version": f"v{random.randint(1, 10)}.{random.randint(0, 9)}",
        "isPublic": random.choice([True, False]),
        "allowedUsers_0": f"usr_{random.randint(10000, 99999)}",
        "allowedUsers_1": f"usr_{random.randint(10000, 99999)}",
        "allowedRoles_0": random.choice(["viewer", "editor", "admin"]),
        "allowedRoles_1": random.choice(["viewer", "editor", "admin"]),
        "regionCoverage_0": random.choice(["North America", "Europe", "Asia", "South America", "Africa", "Oceania"]),
        "regionCoverage_1": random.choice(["Northeast", "Southeast", "Northwest", "Southwest", "Central"]),
        "tags_0": random.choice(["transportation", "urban", "rural", "topography", "climate", "demographics"]),
        "tags_1": random.choice(["2023", "confidential", "public", "experimental", "historical"]),
        "success": True,
        "error": None
    }


def box3_statistics_mcp_getMapInfo(mapId: str) -> Dict[str, Any]:
    """
    获取神岛平台用户地图详情

    该函数通过调用外部API获取指定地图ID的详细信息，包括地图名称、创建者、访问统计、权限等。

    Args:
        mapId (str): 地图ID，用于标识要查询的地图资源

    Returns:
        Dict[str, Any]: 包含地图详细信息的字典，结构如下：
            - mapDetails (Dict): 包含地图的完整详细信息
            - accessCount (int): 地图被访问的总次数
            - creatorId (str): 地图创建者的唯一标识符
            - creationTime (str): 地图创建时间（ISO 8601格式）
            - lastAccessedTime (str): 地图最后被访问的时间（ISO 8601格式）
            - mapName (str): 地图显示名称
            - mapStatus (str): 地图当前状态（如：active, archived, deleted）
            - permissions (Dict): 地图访问权限配置
                - isPublic (bool): 是否公开
                - allowedUsers (List[str]): 允许访问的用户列表
                - allowedRoles (List[str]): 允许访问的角色列表
            - regionCoverage (List[str]): 地图覆盖的地理区域列表
            - tags (List[str]): 地图的标签列表
            - version (str): 地图版本标识
            - success (bool): 请求是否成功
            - error (str, optional): 错误信息（如果请求失败）

    Raises:
        ValueError: 当mapId为空或无效时抛出异常
    """
    # Input validation
    if not mapId or not isinstance(mapId, str) or len(mapId.strip()) == 0:
        return {
            "success": False,
            "error": "Invalid mapId: must be a non-empty string",
            "accessCount": 0,
            "creatorId": "",
            "creationTime": "",
            "lastAccessedTime": "",
            "mapName": "",
            "mapStatus": "",
            "version": "",
            "mapDetails": {},
            "permissions": {},
            "regionCoverage": [],
            "tags": []
        }

    try:
        # Call external API to get flat data
        api_data = call_external_api("box3-statistics-mcp-getMapInfo")

        # Extract and construct nested structures
        permissions = {
            "isPublic": api_data["isPublic"],
            "allowedUsers": [
                api_data["allowedUsers_0"],
                api_data["allowedUsers_1"]
            ],
            "allowedRoles": [
                api_data["allowedRoles_0"],
                api_data["allowedRoles_1"]
            ]
        }

        regionCoverage = [
            api_data["regionCoverage_0"],
            api_data["regionCoverage_1"]
        ]

        tags = [
            api_data["tags_0"],
            api_data["tags_1"]
        ]

        mapDetails = {
            "mapName": api_data["mapName"],
            "creatorId": api_data["creatorId"],
            "creationTime": api_data["creationTime"],
            "lastAccessedTime": api_data["lastAccessedTime"],
            "accessCount": api_data["accessCount"],
            "mapStatus": api_data["mapStatus"],
            "version": api_data["version"],
            "permissions": permissions,
            "regionCoverage": regionCoverage,
            "tags": tags
        }

        # Construct final result
        result = {
            "mapDetails": mapDetails,
            "accessCount": api_data["accessCount"],
            "creatorId": api_data["creatorId"],
            "creationTime": api_data["creationTime"],
            "lastAccessedTime": api_data["lastAccessedTime"],
            "mapName": api_data["mapName"],
            "mapStatus": api_data["mapStatus"],
            "permissions": permissions,
            "regionCoverage": regionCoverage,
            "tags": tags,
            "version": api_data["version"],
            "success": api_data["success"]
        }

        # Add error field only if present
        if api_data.get("error") is not None:
            result["error"] = api_data["error"]

        return result

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to retrieve map info: {str(e)}",
            "accessCount": 0,
            "creatorId": "",
            "creationTime": "",
            "lastAccessedTime": "",
            "mapName": "",
            "mapStatus": "",
            "version": "",
            "mapDetails": {},
            "permissions": {},
            "regionCoverage": [],
            "tags": []
        }