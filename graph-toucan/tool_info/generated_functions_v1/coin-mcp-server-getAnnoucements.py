from typing import Dict, List, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cryptocurrency announcements.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - code (str): Response status code, e.g., "00000"
        - msg (str): Message describing the result, e.g., "success"
        - requestTime (int): Timestamp in milliseconds when request was processed
        - data_0_annId (str): First announcement ID
        - data_0_annDesc (str): First announcement description
        - data_0_annTitle (str): First announcement title
        - data_0_annType (str): First announcement type
        - data_0_annSubType (str): First announcement subtype
        - data_0_language (str): First announcement language
        - data_0_annUrl (str): First announcement URL
        - data_0_cTime (int): First announcement creation time (timestamp)
        - data_1_annId (str): Second announcement ID
        - data_1_annDesc (str): Second announcement description
        - data_1_annTitle (str): Second announcement title
        - data_1_annType (str): Second announcement type
        - data_1_annSubType (str): Second announcement subtype
        - data_1_language (str): Second announcement language
        - data_1_annUrl (str): Second announcement URL
        - data_1_cTime (int): Second announcement creation time (timestamp)
    """
    now_ms = int(time.time() * 1000)
    announcement_types = [
        "latest_news",
        "coin_listings",
        "trading_competitions_promotions",
        "maintenance_system_updates",
        "symbol_delisting"
    ]
    sample_titles = [
        "New Trading Pair Launched",
        "System Maintenance Scheduled",
        "Bitcoin ETF Approved",
        "Token Delisting Notice",
        "Trading Competition Begins"
    ]
    sample_descs = [
        "We are excited to announce the launch of new trading pairs including BTC/USDT and ETH/USDT.",
        "Planned maintenance will occur on Sunday at 2 AM UTC. Trading will be paused temporarily.",
        "Regulatory approval has been granted for a new Bitcoin ETF product.",
        "The following tokens will be delisted due to low trading volume.",
        "Join our monthly trading competition for a chance to win $10,000 in prizes."
    ]

    return {
        "code": "00000",
        "msg": "success",
        "requestTime": now_ms,
        "data_0_annId": f"ann{random.randint(10000, 99999)}",
        "data_0_annDesc": random.choice(sample_descs),
        "data_0_annTitle": random.choice(sample_titles),
        "data_0_annType": random.choice(announcement_types),
        "data_0_annSubType": "general",
        "data_0_language": "en",
        "data_0_annUrl": f"https://example.com/announcements/ann{random.randint(10000, 99999)}",
        "data_0_cTime": now_ms - random.randint(0, 2592000000),  # within last month
        "data_1_annId": f"ann{random.randint(10000, 99999)}",
        "data_1_annDesc": random.choice(sample_descs),
        "data_1_annTitle": random.choice(sample_titles),
        "data_1_annType": random.choice(announcement_types),
        "data_1_annSubType": "urgent",
        "data_1_language": "en",
        "data_1_annUrl": f"https://example.com/announcements/ann{random.randint(10000, 99999)}",
        "data_1_cTime": now_ms - random.randint(0, 2592000000),  # within last month
    }


def coin_mcp_server_getAnnoucements(anType: str) -> Dict[str, Any]:
    """
    Search for cryptocurrency announcements within one month.

    Args:
        anType (str): Type of announcement to filter by. Valid values:
                      'latest_news', 'coin_listings', 'trading_competitions_promotions',
                      'maintenance_system_updates', 'symbol_delisting', or empty string for all.

    Returns:
        Dict containing:
        - code (str): Response status code
        - msg (str): Result message
        - requestTime (int): Timestamp in milliseconds
        - data (List[Dict]): List of announcement objects with keys:
            'annId', 'annDesc', 'annTitle', 'annType', 'annSubType',
            'language', 'annUrl', 'cTime'
    """
    # Input validation
    valid_types = [
        "latest_news",
        "coin_listings",
        "trading_competitions_promotions",
        "maintenance_system_updates",
        "symbol_delisting",
        ""
    ]
    if anType not in valid_types:
        return {
            "code": "99999",
            "msg": f"Invalid announcement type: {anType}. Must be one of {valid_types}",
            "requestTime": int(time.time() * 1000),
            "data": []
        }

    # Fetch data from simulated external API
    api_data = call_external_api("coin-mcp-server-getAnnoucements")

    # Construct data list from flattened API response
    data = [
        {
            "annId": api_data["data_0_annId"],
            "annDesc": api_data["data_0_annDesc"],
            "annTitle": api_data["data_0_annTitle"],
            "annType": api_data["data_0_annType"],
            "annSubType": api_data["data_0_annSubType"],
            "language": api_data["data_0_language"],
            "annUrl": api_data["data_0_annUrl"],
            "cTime": api_data["data_0_cTime"]
        },
        {
            "annId": api_data["data_1_annId"],
            "annDesc": api_data["data_1_annDesc"],
            "annTitle": api_data["data_1_annTitle"],
            "annType": api_data["data_1_annType"],
            "annSubType": api_data["data_1_annSubType"],
            "language": api_data["data_1_language"],
            "annUrl": api_data["data_1_annUrl"],
            "cTime": api_data["data_1_cTime"]
        }
    ]

    # Filter by announcement type if specified
    if anType:
        filtered_data = [ann for ann in data if ann["annType"] == anType]
        data = filtered_data

    # Return final structured response
    return {
        "code": api_data["code"],
        "msg": api_data["msg"],
        "requestTime": api_data["requestTime"],
        "data": data
    }