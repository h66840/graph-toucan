from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DEX summary.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - total_volume (float): Total trading volume across all historical data
        - daily_volume_0_date (str): First daily volume entry date in YYYY-MM-DD
        - daily_volume_0_volume (float): First daily volume amount
        - daily_volume_1_date (str): Second daily volume entry date in YYYY-MM-DD
        - daily_volume_1_volume (float): Second daily volume amount
        - protocol_slug (str): Identifier slug of the DEX protocol
        - protocol_name (str): Human-readable name of the protocol
        - chain_breakdown_ethereum (float): Volume on Ethereum chain
        - chain_breakdown_bsc (float): Volume on Binance Smart Chain
        - category (str): Category of the protocol
        - success (bool): Whether the request was successful
        - error (str): Error message if any, otherwise empty string
        - last_updated (str): Timestamp when data was last updated (ISO 8601)
        - metadata_source_url (str): Source URL for the data
        - metadata_api_version (str): API version used
        - metadata_time_range_start (str): Start of time range (YYYY-MM-DD)
        - metadata_time_range_end (str): End of time range (YYYY-MM-DD)
    """
    today = datetime.now()
    return {
        "total_volume": 1250000000.5,
        "daily_volume_0_date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "daily_volume_0_volume": 45000000.0,
        "daily_volume_1_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        "daily_volume_1_volume": 42000000.0,
        "protocol_slug": "uniswap",
        "protocol_name": "Uniswap",
        "chain_breakdown_ethereum": 1000000000.0,
        "chain_breakdown_bsc": 250000000.5,
        "category": "Dexes",
        "success": True,
        "error": "",
        "last_updated": (today - timedelta(hours=1)).isoformat(),
        "metadata_source_url": "https://api.llama.fi/overview/dexs",
        "metadata_api_version": "1.0",
        "metadata_time_range_start": "2020-01-01",
        "metadata_time_range_end": today.strftime("%Y-%m-%d"),
    }


def defillama_api_server_get_summary_dexs_by_protocol(
    protocol: str,
    excludeTotalDataChart: Optional[bool] = False,
    excludeTotalDataChartBreakdown: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Get summary of dex volume with historical data for a specific protocol.

    Args:
        protocol (str): Protocol slug (required)
        excludeTotalDataChart (bool, optional): If True, excludes aggregated chart data
        excludeTotalDataChartBreakdown (bool, optional): If True, excludes broken down chart data

    Returns:
        Dict containing:
        - total_volume (float): Total trading volume across all historical data
        - daily_volumes (List[Dict]): List of daily volume entries with date and volume
        - protocol_slug (str): Identifier slug of the DEX protocol
        - protocol_name (str): Human-readable name of the protocol
        - chain_breakdown (Dict): Volume breakdown by blockchain network
        - category (str): Category of the protocol
        - success (bool): Whether the request was successful
        - error (str): Error message if request failed, otherwise None
        - last_updated (str): Timestamp when data was last updated (ISO 8601)
        - metadata (Dict): Additional contextual information

    Raises:
        ValueError: If protocol is not provided
    """
    if not protocol:
        return {
            "total_volume": 0.0,
            "daily_volumes": [],
            "protocol_slug": "",
            "protocol_name": "",
            "chain_breakdown": {},
            "category": "",
            "success": False,
            "error": "Protocol slug is required",
            "last_updated": datetime.now().isoformat(),
            "metadata": {
                "source_url": "",
                "api_version": "",
                "time_range": {"start": "", "end": ""}
            }
        }

    # Fetch simulated external API data
    api_data = call_external_api("defillama-api-server-get_summary_dexs__by_protocol")

    # Construct daily volumes list
    daily_volumes = [
        {
            "date": api_data["daily_volume_0_date"],
            "volume": api_data["daily_volume_0_volume"]
        },
        {
            "date": api_data["daily_volume_1_date"],
            "volume": api_data["daily_volume_1_volume"]
        }
    ]

    # Construct chain breakdown
    chain_breakdown = {}
    if not excludeTotalDataChartBreakdown:
        chain_breakdown = {
            "ethereum": api_data["chain_breakdown_ethereum"],
            "bsc": api_data["chain_breakdown_bsc"]
        }

    # Construct metadata
    metadata = {
        "source_url": api_data["metadata_source_url"],
        "api_version": api_data["metadata_api_version"],
        "time_range": {
            "start": api_data["metadata_time_range_start"],
            "end": api_data["metadata_time_range_end"]
        }
    }

    # Build result
    result = {
        "total_volume": api_data["total_volume"],
        "daily_volumes": daily_volumes,
        "protocol_slug": api_data["protocol_slug"],
        "protocol_name": api_data["protocol_name"],
        "chain_breakdown": chain_breakdown,
        "category": api_data["category"],
        "success": api_data["success"],
        "error": api_data["error"] if api_data["error"] else None,
        "last_updated": api_data["last_updated"],
        "metadata": metadata
    }

    # Exclude total data chart if requested
    if excludeTotalDataChart:
        result["daily_volumes"] = []

    return result