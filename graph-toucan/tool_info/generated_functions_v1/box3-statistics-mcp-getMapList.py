from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for the map list retrieval tool.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - map_0_name (str): Name of the first map
        - map_0_id (int): ID of the first map
        - map_0_author (str): Author of the first map
        - map_0_created_time (int): Creation timestamp of the first map
        - map_0_play_count (int): Play count of the first map
        - map_0_description (str): Description of the first map
        - map_1_name (str): Name of the second map
        - map_1_id (int): ID of the second map
        - map_1_author (str): Author of the second map
        - map_1_created_time (int): Creation timestamp of the second map
        - map_1_play_count (int): Play count of the second map
        - map_1_description (str): Description of the second map
        - total_count (int): Total number of maps matching the query
        - has_more (bool): Whether more results exist beyond current page
        - response_offset (int): Current offset used in the response
        - response_limit (int): Number of items returned per page
        - response_keyword (str): Echoed keyword used in search
        - response_orderBy (int): Sorting method applied
        - metadata_timestamp (int): Server timestamp of the response
        - metadata_request_id (str): Unique request identifier
        - metadata_version (str): System version of the API
    """
    return {
        "map_0_name": "Mystic Island Adventure",
        "map_0_id": 1001,
        "map_0_author": "Alice",
        "map_0_created_time": 1672531200,
        "map_0_play_count": 1500,
        "map_0_description": "An adventurous journey through a mysterious island.",
        "map_1_name": "Desert Treasure Hunt",
        "map_1_id": 1002,
        "map_1_author": "Bob",
        "map_1_created_time": 1672617600,
        "map_1_play_count": 980,
        "map_1_description": "Search for hidden treasures in the vast desert.",
        "total_count": 45,
        "has_more": True,
        "response_offset": 0,
        "response_limit": 2,
        "response_keyword": "adventure",
        "response_orderBy": 0,
        "metadata_timestamp": 1672531200,
        "metadata_request_id": "req_abc123xyz",
        "metadata_version": "1.2.0"
    }

def box3_statistics_mcp_getMapList(keyword: str, limit: int, offset: int, orderBy: int) -> Dict[str, Any]:
    """
    获取神岛平台用户地图列表
    
    根据关键词、分页参数和排序方式查询用户地图列表，并返回地图详情、总数、分页信息等。
    
    Args:
        keyword (str): 搜索关键词，用于过滤地图名称或描述
        limit (int): 查询数量限制，最多返回100条
        offset (int): 分页偏移量
        orderBy (int): 排序方式：0表示官方推荐最热，1表示最新，2表示按关键词查找时使用
    
    Returns:
        Dict containing:
        - maps (List[Dict]): 地图对象列表，包含名称、ID、作者、创建时间、播放次数和描述
        - total_count (int): 符合查询条件的地图总数
        - has_more (bool): 是否还有更多结果
        - offset (int): 当前使用的偏移量
        - limit (int): 每页返回的数量
        - keyword (str): 使用的搜索关键词（回显）
        - orderBy (int): 使用的排序方式
        - metadata (Dict): 元数据信息，包括时间戳、请求ID和系统版本
    
    Raises:
        ValueError: 如果limit超过100或参数类型不正确
    """
    # Input validation
    if not isinstance(keyword, str):
        raise ValueError("keyword must be a string")
    if not isinstance(limit, int) or limit <= 0:
        raise ValueError("limit must be a positive integer")
    if limit > 100:
        raise ValueError("limit cannot exceed 100")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("offset must be a non-negative integer")
    if not isinstance(orderBy, int) or orderBy not in [0, 1, 2]:
        raise ValueError("orderBy must be 0 (hot), 1 (newest), or 2 (keyword-based)")

    # Call external API (simulated)
    api_data = call_external_api("box3-statistics-mcp-getMapList")

    # Construct maps list from flattened API response
    maps = [
        {
            "name": api_data["map_0_name"],
            "id": api_data["map_0_id"],
            "author": api_data["map_0_author"],
            "created_time": api_data["map_0_created_time"],
            "play_count": api_data["map_0_play_count"],
            "description": api_data["map_0_description"]
        },
        {
            "name": api_data["map_1_name"],
            "id": api_data["map_1_id"],
            "author": api_data["map_1_author"],
            "created_time": api_data["map_1_created_time"],
            "play_count": api_data["map_1_play_count"],
            "description": api_data["map_1_description"]
        }
    ]

    # Construct metadata
    metadata = {
        "timestamp": api_data["metadata_timestamp"],
        "request_id": api_data["metadata_request_id"],
        "version": api_data["metadata_version"]
    }

    # Build final result structure
    result = {
        "maps": maps,
        "total_count": api_data["total_count"],
        "has_more": api_data["has_more"],
        "offset": api_data["response_offset"],
        "limit": api_data["response_limit"],
        "keyword": api_data["response_keyword"],
        "orderBy": api_data["response_orderBy"],
        "metadata": metadata
    }

    return result