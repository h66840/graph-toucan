from typing import Dict, List, Any
from datetime import datetime, timezone, timedelta
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for map release information.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - map_release_info_0_release_id (str): First release version unique identifier
        - map_release_info_0_version (str): First map version number
        - map_release_info_0_released_at (str): First release time in ISO 8601 format
        - map_release_info_0_status (str): First release status ('active' or 'deprecated')
        - map_release_info_0_region (str): First release region or node
        - map_release_info_0_changelog (str): First release changelog or update notes
        - map_release_info_0_author (str): First release author username
        - map_release_info_1_release_id (str): Second release version unique identifier
        - map_release_info_1_version (str): Second map version number
        - map_release_info_1_released_at (str): Second release time in ISO 8601 format
        - map_release_info_1_status (str): Second release status ('active' or 'deprecated')
        - map_release_info_1_region (str): Second release region or node
        - map_release_info_1_changelog (str): Second release changelog or update notes
        - map_release_info_1_author (str): Second release author username
        - total_count (int): Total number of matching map release records
        - has_more (bool): Whether more results exist beyond current offset and limit
        - metadata_request_id (str): Unique ID for the current request
        - metadata_timestamp (str): Response generation time in ISO 8601 format
        - metadata_duration_ms (int): Processing duration in milliseconds
    """
    # Generate deterministic but realistic values based on tool name
    random.seed(tool_name.__hash__() % (2**32))

    def random_version() -> str:
        return f"{random.randint(1, 10)}.{random.randint(0, 9)}.{random.randint(0, 99)}"

    def random_iso_time() -> str:
        base = datetime.now(timezone.utc)
        offset = random.randint(-30, 0)
        dt = base.replace(minute=random.randint(0, 59), second=random.randint(0, 59)) + timedelta(days=offset)
        return dt.isoformat()

    def random_string(prefix: str, length: int = 8) -> str:
        return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    return {
        "map_release_info_0_release_id": random_string("rel", 12),
        "map_release_info_0_version": random_version(),
        "map_release_info_0_released_at": random_iso_time(),
        "map_release_info_0_status": random.choice(["active", "deprecated"]),
        "map_release_info_0_region": random.choice(["cn-north-1", "us-west-1", "eu-central-1"]),
        "map_release_info_0_changelog": f"Updated terrain data and fixed POI inaccuracies.",
        "map_release_info_0_author": random_string("user", 6),

        "map_release_info_1_release_id": random_string("rel", 12),
        "map_release_info_1_version": random_version(),
        "map_release_info_1_released_at": random_iso_time(),
        "map_release_info_1_status": random.choice(["active", "deprecated"]),
        "map_release_info_1_region": random.choice(["cn-east-2", "ap-southeast-1", "us-east-1"]),
        "map_release_info_1_changelog": f"Added new landmarks and improved routing logic.",
        "map_release_info_1_author": random_string("user", 6),

        "total_count": random.randint(50, 200),
        "has_more": random.choice([True, False]),
        "metadata_request_id": random_string("req", 16),
        "metadata_timestamp": datetime.now(timezone.utc).isoformat(),
        "metadata_duration_ms": random.randint(10, 200)
    }


def box3_statistics_mcp_getMapReleaseInfo(contentId: str, limit: int, offset: int) -> Dict[str, Any]:
    """
    获取神岛平台用户地图发布信息。

    该函数模拟查询指定地图ID的发布记录，返回分页结果，包括发布版本、时间、状态、区域、更新说明、发布人等信息。
    使用模拟的外部API调用获取数据，并根据输入参数构造符合输出结构的结果。

    Args:
        contentId (str): 地图ID，用于标识查询的地图资源
        limit (int): 查询数量限制，最多返回100条记录
        offset (int): 分页偏移量，用于跳过前面的记录

    Returns:
        Dict[str, Any]: 包含以下字段的字典：
            - map_release_info (List[Dict]): 地图发布信息列表，每条记录包含：
                - release_id (str): 发布版本唯一标识
                - version (str): 地图版本号
                - released_at (str): 发布时间（ISO 8601格式）
                - status (str): 发布状态（如 'active', 'deprecated'）
                - region (str): 发布区域或节点
                - changelog (str): 更新说明
                - author (str): 发布人用户名
            - total_count (int): 符合条件的地图发布记录总数
            - has_more (bool): 是否还有更多结果未返回
            - metadata (Dict): 附加元信息，包含：
                - request_id (str): 当前请求唯一ID
                - timestamp (str): 响应生成时间（ISO 8601格式）
                - duration_ms (int): 处理耗时（毫秒）

    Raises:
        ValueError: 当 limit 超过 100 或小于 1，或 offset 小于 0 时抛出
        TypeError: 当参数类型不正确时抛出
    """
    # Input validation
    if not isinstance(contentId, str) or not contentId.strip():
        raise TypeError("contentId must be a non-empty string")
    if not isinstance(limit, int):
        raise TypeError("limit must be an integer")
    if not isinstance(offset, int):
        raise TypeError("offset must be an integer")
    if limit < 1 or limit > 100:
        raise ValueError("limit must be between 1 and 100")
    if offset < 0:
        raise ValueError("offset must be non-negative")

    # Call external API (simulated)
    raw_data = call_external_api("box3-statistics-mcp-getMapReleaseInfo")

    # Construct map_release_info list from indexed fields
    map_release_info = [
        {
            "release_id": raw_data["map_release_info_0_release_id"],
            "version": raw_data["map_release_info_0_version"],
            "released_at": raw_data["map_release_info_0_released_at"],
            "status": raw_data["map_release_info_0_status"],
            "region": raw_data["map_release_info_0_region"],
            "changelog": raw_data["map_release_info_0_changelog"],
            "author": raw_data["map_release_info_0_author"]
        },
        {
            "release_id": raw_data["map_release_info_1_release_id"],
            "version": raw_data["map_release_info_1_version"],
            "released_at": raw_data["map_release_info_1_released_at"],
            "status": raw_data["map_release_info_1_status"],
            "region": raw_data["map_release_info_1_region"],
            "changelog": raw_data["map_release_info_1_changelog"],
            "author": raw_data["map_release_info_1_author"]
        }
    ]

    # Apply limit and offset logic (simulate pagination)
    start_idx = offset
    end_idx = offset + limit
    paginated_release_info = map_release_info * ((end_idx // 2) + 1)  # Repeat data to simulate larger dataset
    paginated_release_info = paginated_release_info[start_idx:end_idx]

    # Construct final result
    result = {
        "map_release_info": paginated_release_info,
        "total_count": raw_data["total_count"],
        "has_more": raw_data["has_more"],
        "metadata": {
            "request_id": raw_data["metadata_request_id"],
            "timestamp": raw_data["metadata_timestamp"],
            "duration_ms": raw_data["metadata_duration_ms"]
        }
    }

    return result