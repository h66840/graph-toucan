from typing import Dict, List, Any
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching cryptocurrency announcements from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - code (str): Response status code, e.g., "200"
        - msg (str): Human-readable message, e.g., "Success"
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
    current_time_ms = int(time.time() * 1000)
    announcement_types = [
        "latest_news", "coin_listings", "trading_competitions_promotions",
        "maintenance_system_updates", "symbol_delisting"
    ]
    sample_titles = [
        "New Trading Pair Launched",
        "System Maintenance Scheduled",
        "BTC/USDT Delisting Notice",
        "Win Up to $10,000 in Our Trading Contest",
        "Platform Upgrade Announcement"
    ]
    sample_descs = [
        "We are excited to announce the launch of new trading pairs including ETH/USDC and SOL/USDT.",
        "Scheduled maintenance will occur on June 15th from 02:00 to 04:00 UTC.",
        "The BTC/USDT trading pair will be delisted due to low trading volume.",
        "Join our trading competition and win amazing prizes worth over $10,000.",
        "Our platform will undergo a major upgrade to improve performance and security."
    ]

    selected_type = random.choice(announcement_types)
    return {
        "code": "200",
        "msg": "Success",
        "requestTime": current_time_ms,
        "data_0_annId": f"ann{random.randint(10000, 99999)}",
        "data_0_annDesc": random.choice(sample_descs),
        "data_0_annTitle": random.choice(sample_titles),
        "data_0_annType": selected_type,
        "data_0_annSubType": "general",
        "data_0_language": "en",
        "data_0_annUrl": f"https://example.com/announcements/ann{random.randint(10000, 99999)}",
        "data_0_cTime": current_time_ms - random.randint(0, 86400000 * 30),  # Within last month
        "data_1_annId": f"ann{random.randint(10000, 99999)}",
        "data_1_annDesc": random.choice(sample_descs),
        "data_1_annTitle": random.choice(sample_titles),
        "data_1_annType": selected_type,
        "data_1_annSubType": "general",
        "data_1_language": "en",
        "data_1_annUrl": f"https://example.com/announcements/ann{random.randint(10000, 99999)}",
        "data_1_cTime": current_time_ms - random.randint(0, 86400000 * 30),
    }


def coin_price_fetcher_getAnnoucements(anType: str) -> Dict[str, Any]:
    """
    Search for cryptocurrency announcements within one month.
    
    Args:
        anType (str): Type of announcement to filter by. Valid values:
                      'latest_news', 'coin_listings', 'trading_competitions_promotions',
                      'maintenance_system_updates', 'symbol_delisting', or empty string for all.
    
    Returns:
        Dict containing:
        - code (str): Response status code
        - msg (str): Human-readable message
        - requestTime (int): Timestamp in milliseconds when request was processed
        - data (List[Dict]): List of announcement objects with fields:
            'annId', 'annDesc', 'annTitle', 'annType', 'annSubType',
            'language', 'annUrl', 'cTime'
    
    Raises:
        ValueError: If anType is None or not a string
    """
    if anType is None:
        raise ValueError("anType must be a string")
    if not isinstance(anType, str):
        raise ValueError("anType must be a string")

    # Fetch data from simulated external API
    api_data = call_external_api("coin-price-fetcher-getAnnoucements")

    # Construct the first announcement object
    announcement_0 = {
        "annId": api_data["data_0_annId"],
        "annDesc": api_data["data_0_annDesc"],
        "annTitle": api_data["data_0_annTitle"],
        "annType": api_data["data_0_annType"],
        "annSubType": api_data["data_0_annSubType"],
        "language": api_data["data_0_language"],
        "annUrl": api_data["data_0_annUrl"],
        "cTime": api_data["data_0_cTime"]
    }

    # Construct the second announcement object
    announcement_1 = {
        "annId": api_data["data_1_annId"],
        "annDesc": api_data["data_1_annDesc"],
        "annTitle": api_data["data_1_annTitle"],
        "annType": api_data["data_1_annType"],
        "annSubType": api_data["data_1_annSubType"],
        "language": api_data["data_1_language"],
        "annUrl": api_data["data_1_annUrl"],
        "cTime": api_data["data_1_cTime"]
    }

    # Create data list
    raw_data = [announcement_0, announcement_1]

    # Filter by announcement type if specified
    if anType.strip():
        filtered_data = [ann for ann in raw_data if ann["annType"] == anType]
    else:
        filtered_data = raw_data

    # Construct final result
    result = {
        "code": api_data["code"],
        "msg": api_data["msg"],
        "requestTime": api_data["requestTime"],
        "data": filtered_data
    }

    return result