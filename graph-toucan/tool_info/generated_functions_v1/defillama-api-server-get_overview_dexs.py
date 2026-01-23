from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DEX overview.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - dex_0_name (str): Name of the first DEX
        - dex_0_slug (str): Slug of the first DEX
        - dex_0_chains (str): Comma-separated chains for the first DEX
        - dex_0_volume_24h (float): 24-hour volume for the first DEX
        - dex_0_volume_7d (float): 7-day volume for the first DEX
        - dex_0_total_volume (float): Total volume for the first DEX
        - dex_0_change_1d (float): 1-day volume change percentage for the first DEX
        - dex_0_change_7d (float): 7-day volume change percentage for the first DEX
        - dex_0_url (str): URL of the first DEX
        - dex_1_name (str): Name of the second DEX
        - dex_1_slug (str): Slug of the second DEX
        - dex_1_chains (str): Comma-separated chains for the second DEX
        - dex_1_volume_24h (float): 24-hour volume for the second DEX
        - dex_1_volume_7d (float): 7-day volume for the second DEX
        - dex_1_total_volume (float): Total volume for the second DEX
        - dex_1_change_1d (float): 1-day volume change percentage for the second DEX
        - dex_1_change_7d (float): 7-day volume change percentage for the second DEX
        - dex_1_url (str): URL of the second DEX
        - total_data_chart_0_timestamp (int): First timestamp in aggregated chart
        - total_data_chart_0_value (float): Volume value at first timestamp
        - total_data_chart_1_timestamp (int): Second timestamp in aggregated chart
        - total_data_chart_1_value (float): Volume value at second timestamp
        - total_data_chart_breakdown_uniswap_0_timestamp (int): First timestamp for Uniswap breakdown
        - total_data_chart_breakdown_uniswap_0_value (float): Volume value for Uniswap at first timestamp
        - total_data_chart_breakdown_uniswap_1_timestamp (int): Second timestamp for Uniswap breakdown
        - total_data_chart_breakdown_uniswap_1_value (float): Volume value for Uniswap at second timestamp
        - total_data_chart_breakdown_sushiswap_0_timestamp (int): First timestamp for Sushiswap breakdown
        - total_data_chart_breakdown_sushiswap_0_value (float): Volume value for Sushiswap at first timestamp
        - total_data_chart_breakdown_sushiswap_1_timestamp (int): Second timestamp for Sushiswap breakdown
        - total_data_chart_breakdown_sushiswap_1_value (float): Volume value for Sushiswap at second timestamp
        - meta_total_dexs (int): Total number of DEXs returned
        - meta_updated_at (int): Unix timestamp when data was last updated
        - meta_warning (str): Warning message if any
    """
    return {
        "dex_0_name": "Uniswap",
        "dex_0_slug": "uniswap",
        "dex_0_chains": "Ethereum,Optimism,Arbitrum",
        "dex_0_volume_24h": 125000000.0,
        "dex_0_volume_7d": 875000000.0,
        "dex_0_total_volume": 25000000000.0,
        "dex_0_change_1d": 12.5,
        "dex_0_change_7d": -3.2,
        "dex_0_url": "https://uniswap.org",
        "dex_1_name": "SushiSwap",
        "dex_1_slug": "sushiswap",
        "dex_1_chains": "Ethereum,BSC",
        "dex_1_volume_24h": 45000000.0,
        "dex_1_volume_7d": 315000000.0,
        "dex_1_total_volume": 8500000000.0,
        "dex_1_change_1d": -5.1,
        "dex_1_change_7d": 8.7,
        "dex_1_url": "https://sushi.com",
        "total_data_chart_0_timestamp": 1672531200,
        "total_data_chart_0_value": 170000000.0,
        "total_data_chart_1_timestamp": 1672617600,
        "total_data_chart_1_value": 185000000.0,
        "total_data_chart_breakdown_uniswap_0_timestamp": 1672531200,
        "total_data_chart_breakdown_uniswap_0_value": 120000000.0,
        "total_data_chart_breakdown_uniswap_1_timestamp": 1672617600,
        "total_data_chart_breakdown_uniswap_1_value": 125000000.0,
        "total_data_chart_breakdown_sushiswap_0_timestamp": 1672531200,
        "total_data_chart_breakdown_sushiswap_0_value": 40000000.0,
        "total_data_chart_breakdown_sushiswap_1_timestamp": 1672617600,
        "total_data_chart_breakdown_sushiswap_1_value": 45000000.0,
        "meta_total_dexs": 2,
        "meta_updated_at": 1672623400,
        "meta_warning": "Data may be delayed by up to 1 hour"
    }

def defillama_api_server_get_overview_dexs(excludeTotalDataChart: Optional[bool] = False, 
                                          excludeTotalDataChartBreakdown: Optional[bool] = False) -> Dict[str, Any]:
    """
    List all DEXs along with summaries of their volumes and historical data.

    Args:
        excludeTotalDataChart (bool, optional): If True, excludes aggregated chart from response. Defaults to False.
        excludeTotalDataChartBreakdown (bool, optional): If True, excludes broken down chart from response. Defaults to False.

    Returns:
        Dict containing:
        - dexs (List[Dict]): List of DEX entries with metadata and volume summaries.
        - total_data_chart (List[List[int]]): Aggregated historical volume data as [timestamp, value] pairs.
        - total_data_chart_breakdown (Dict): Breakdown of historical volume by DEX, mapping names to time-series data.
        - meta (Dict): Metadata about the response including update timestamps and warnings.
    
    Raises:
        ValueError: If input parameters are of incorrect type.
    """
    # Input validation
    if excludeTotalDataChart is not None and not isinstance(excludeTotalDataChart, bool):
        raise ValueError("excludeTotalDataChart must be a boolean or None")
    if excludeTotalDataChartBreakdown is not None and not isinstance(excludeTotalDataChartBreakdown, bool):
        raise ValueError("excludeTotalDataChartBreakdown must be a boolean or None")

    # Fetch data from external API (simulated)
    api_data = call_external_api("defillama-api-server-get_overview_dexs")

    # Construct DEXs list
    dexs = [
        {
            "name": api_data["dex_0_name"],
            "slug": api_data["dex_0_slug"],
            "chains": api_data["dex_0_chains"].split(","),
            "volume_24h": api_data["dex_0_volume_24h"],
            "volume_7d": api_data["dex_0_volume_7d"],
            "total_volume": api_data["dex_0_total_volume"],
            "change_1d": api_data["dex_0_change_1d"],
            "change_7d": api_data["dex_0_change_7d"],
            "url": api_data["dex_0_url"]
        },
        {
            "name": api_data["dex_1_name"],
            "slug": api_data["dex_1_slug"],
            "chains": api_data["dex_1_chains"].split(","),
            "volume_24h": api_data["dex_1_volume_24h"],
            "volume_7d": api_data["dex_1_volume_7d"],
            "total_volume": api_data["dex_1_total_volume"],
            "change_1d": api_data["dex_1_change_1d"],
            "change_7d": api_data["dex_1_change_7d"],
            "url": api_data["dex_1_url"]
        }
    ]

    # Construct total_data_chart
    total_data_chart = []
    if not excludeTotalDataChart:
        total_data_chart = [
            [api_data["total_data_chart_0_timestamp"], api_data["total_data_chart_0_value"]],
            [api_data["total_data_chart_1_timestamp"], api_data["total_data_chart_1_value"]]
        ]

    # Construct total_data_chart_breakdown
    total_data_chart_breakdown = {}
    if not excludeTotalDataChartBreakdown:
        total_data_chart_breakdown = {
            "uniswap": [
                [api_data["total_data_chart_breakdown_uniswap_0_timestamp"], api_data["total_data_chart_breakdown_uniswap_0_value"]],
                [api_data["total_data_chart_breakdown_uniswap_1_timestamp"], api_data["total_data_chart_breakdown_uniswap_1_value"]]
            ],
            "sushiswap": [
                [api_data["total_data_chart_breakdown_sushiswap_0_timestamp"], api_data["total_data_chart_breakdown_sushiswap_0_value"]],
                [api_data["total_data_chart_breakdown_sushiswap_1_timestamp"], api_data["total_data_chart_breakdown_sushiswap_1_value"]]
            ]
        }

    # Construct meta
    meta = {
        "total_dexs": api_data["meta_total_dexs"],
        "updated_at": api_data["meta_updated_at"],
        "warning": api_data["meta_warning"]
    }

    # Return final response
    return {
        "dexs": dexs,
        "total_data_chart": total_data_chart,
        "total_data_chart_breakdown": total_data_chart_breakdown,
        "meta": meta
    }