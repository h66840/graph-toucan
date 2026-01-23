from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for '什么值得买' rankings.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - item_0_title (str): Title of the first ranked item
        - item_0_product_name (str): Product name of the first item
        - item_0_link (str): URL link to the first item
        - item_0_price (float): Price of the first item in CNY
        - item_0_rating (float): Rating of the first item (e.g., out of 5)
        - item_0_summary (str): Summary or description of the first item
        - item_1_title (str): Title of the second ranked item
        - item_1_product_name (str): Product name of the second item
        - item_1_link (str): URL link to the second item
        - item_1_price (float): Price of the second item in CNY
        - item_1_rating (float): Rating of the second item (e.g., out of 5)
        - item_1_summary (str): Summary or description of the second item
        - total_count (int): Total number of items returned
        - time_range (str): Time range for the ranking: 'daily', 'weekly', or 'monthly'
        - rank_type (str): Type of ranking: e.g., 'hot', 'discount', 'recommendation'
        - fetched_at (str): Timestamp when data was fetched, in ISO 8601 format
        - metadata_source_url (str): Source URL of the ranking list
        - metadata_next_update (str): Expected next update time in ISO 8601 format
    """
    return {
        "item_0_title": "限时秒杀！Apple iPhone 15 Pro 最低仅需6999元",
        "item_0_product_name": "Apple iPhone 15 Pro",
        "item_0_link": "https://www.smzdm.com/p/abc123",
        "item_0_price": 6999.0,
        "item_0_rating": 4.8,
        "item_0_summary": "高性能旗舰手机，A17芯片，钛金属边框，摄影能力大幅提升。",
        "item_1_title": "京东家电补贴，小米空调立减800元",
        "item_1_product_name": "小米空调 1.5匹 变频",
        "item_1_link": "https://www.smzdm.com/p/def456",
        "item_1_price": 2199.0,
        "item_1_rating": 4.6,
        "item_1_summary": "节能省电，智能控制，适合卧室使用，现享受政府补贴。",
        "total_count": 2,
        "time_range": "daily",
        "rank_type": "discount",
        "fetched_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "metadata_source_url": "https://www.smzdm.com/hot/",
        "metadata_next_update": (datetime.utcnow().replace(minute=0, second=0, microsecond=0) + 
                                 timedelta(hours=1)).strftime("%Y-%m-%dT%H:00:00Z")
    }


def trends_hub_get_smzdm_rank(unit: Optional[str] = None) -> Dict[str, Any]:
    """
    获取什么值得买热门榜单数据，包括商品推荐、优惠信息、购物攻略等内容。

    Parameters:
        unit (Optional[str]): 时间单位或榜单类型过滤参数（如 'daily', 'weekly'），可选。

    Returns:
        Dict with the following structure:
        - items (List[Dict]): List of ranked content items, each containing:
            - title (str): Item title
            - product_name (str): Name of the product
            - link (str): URL to the item
            - price (float): Price in CNY
            - rating (float): User rating
            - summary (str): Brief description or summary
        - total_count (int): Number of items returned
        - time_range (str): Time range of the ranking ('daily', 'weekly', 'monthly')
        - rank_type (str): Type of ranking ('hot', 'discount', 'recommendation')
        - fetched_at (str): Fetch timestamp in ISO 8601 format
        - metadata (Dict): Additional metadata including:
            - source_url (str): Original source URL
            - next_update (str): Estimated next update time
    """
    # Validate input
    valid_units = {'daily', 'weekly', 'monthly', None}
    if unit not in valid_units:
        raise ValueError(f"Invalid unit: {unit}. Must be one of {valid_units}")

    try:
        # Fetch simulated external data
        raw_data = call_external_api("trends-hub-get-smzdm-rank")

        # Construct items list from indexed fields
        items = [
            {
                "title": raw_data["item_0_title"],
                "product_name": raw_data["item_0_product_name"],
                "link": raw_data["item_0_link"],
                "price": raw_data["item_0_price"],
                "rating": raw_data["item_0_rating"],
                "summary": raw_data["item_0_summary"]
            },
            {
                "title": raw_data["item_1_title"],
                "product_name": raw_data["item_1_product_name"],
                "link": raw_data["item_1_link"],
                "price": raw_data["item_1_price"],
                "rating": raw_data["item_1_rating"],
                "summary": raw_data["item_1_summary"]
            }
        ]

        # Construct metadata
        metadata = {
            "source_url": raw_data["metadata_source_url"],
            "next_update": raw_data["metadata_next_update"]
        }

        # Build final result matching output schema
        result = {
            "items": items,
            "total_count": raw_data["total_count"],
            "time_range": raw_data["time_range"],
            "rank_type": raw_data["rank_type"],
            "fetched_at": raw_data["fetched_at"],
            "metadata": metadata
        }

        return result

    except KeyError as e:
        raise RuntimeError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to process SMZDM rank data: {e}")