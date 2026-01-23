from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DEXs overview by chain.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - dexs_0_name (str): Name of the first DEX
        - dexs_0_slug (str): Slug of the first DEX
        - dexs_0_logo (str): Logo URL of the first DEX
        - dexs_0_total_volume (float): Total volume of the first DEX
        - dexs_0_volume_change_7d (float): 7-day volume change percentage for the first DEX
        - dexs_1_name (str): Name of the second DEX
        - dexs_1_slug (str): Slug of the second DEX
        - dexs_1_logo (str): Logo URL of the second DEX
        - dexs_1_total_volume (float): Total volume of the second DEX
        - dexs_1_volume_change_7d (float): 7-day volume change percentage for the second DEX
        - total_volume (float): Total trading volume across all DEXs on the chain
        - volume_change_7d (float): Percentage change in total volume vs 7 days ago
        - top_dex_by_volume_name (str): Name of the top DEX by volume
        - top_dex_by_volume_volume (float): Volume of the top DEX
        - top_dex_by_volume_share (float): Share of total volume (as decimal)
        - all_chains_0 (str): First supported chain
        - all_chains_1 (str): Second supported chain
        - chart_data_0_timestamp (int): First chart data timestamp
        - chart_data_0_volume (float): Volume at first timestamp
        - chart_data_1_timestamp (int): Second chart data timestamp
        - chart_data_1_volume (float): Volume at second timestamp
        - chart_data_breakdown_0_timestamp (int): First breakdown timestamp
        - chart_data_breakdown_0_dex_a (float): Volume for DEX A at first timestamp
        - chart_data_breakdown_0_dex_b (float): Volume for DEX B at first timestamp
        - chart_data_breakdown_1_timestamp (int): Second breakdown timestamp
        - chart_data_breakdown_1_dex_a (float): Volume for DEX A at second timestamp
        - chart_data_breakdown_1_dex_b (float): Volume for DEX B at second timestamp
        - metadata_updated_at (int): Unix timestamp when data was last updated
        - metadata_chain_status (str): Status of the chain (e.g., "active")
        - metadata_data_source (str): Source of the data
    """
    return {
        "dexs_0_name": "Uniswap",
        "dexs_0_slug": "uniswap",
        "dexs_0_logo": "https://example.com/uniswap.png",
        "dexs_0_total_volume": 1250000000.0,
        "dexs_0_volume_change_7d": 12.5,
        "dexs_1_name": "SushiSwap",
        "dexs_1_slug": "sushiswap",
        "dexs_1_logo": "https://example.com/sushiswap.png",
        "dexs_1_total_volume": 320000000.0,
        "dexs_1_volume_change_7d": -5.3,
        "total_volume": 1570000000.0,
        "volume_change_7d": 8.2,
        "top_dex_by_volume_name": "Uniswap",
        "top_dex_by_volume_volume": 1250000000.0,
        "top_dex_by_volume_share": 0.796,
        "all_chains_0": "Ethereum",
        "all_chains_1": "Arbitrum",
        "chart_data_0_timestamp": 1698768000,
        "chart_data_0_volume": 75000000.0,
        "chart_data_1_timestamp": 1698854400,
        "chart_data_1_volume": 82000000.0,
        "chart_data_breakdown_0_timestamp": 1698768000,
        "chart_data_breakdown_0_dex_a": 50000000.0,
        "chart_data_breakdown_0_dex_b": 25000000.0,
        "chart_data_breakdown_1_timestamp": 1698854400,
        "chart_data_breakdown_1_dex_a": 55000000.0,
        "chart_data_breakdown_1_dex_b": 27000000.0,
        "metadata_updated_at": 1698923400,
        "metadata_chain_status": "active",
        "metadata_data_source": "defillama"
    }

def defillama_api_server_get_overview_dexs_by_chain(
    chain: str,
    excludeTotalDataChart: Optional[bool] = False,
    excludeTotalDataChartBreakdown: Optional[bool] = False
) -> Dict[str, Any]:
    """
    List all DEXs along with summaries of their volumes and historical data filtered by chain.

    Args:
        chain (str): Chain name (e.g., "Ethereum"). List of supported chains available in response.
        excludeTotalDataChart (bool, optional): If True, excludes aggregated chart data.
        excludeTotalDataChartBreakdown (bool, optional): If True, excludes broken down chart data.

    Returns:
        Dict containing:
        - dexs (List[Dict]): List of DEX entries with metadata and volume metrics
        - total_volume (float): Total trading volume across all DEXs on the chain
        - volume_change_7d (float): Percentage change in total volume compared to 7 days ago
        - top_dex_by_volume (Dict): Info about top DEX by volume (name, volume, share)
        - all_chains (List[str]): List of all supported chains
        - chart_data (List[List]): Time-series data as [timestamp, volume] pairs (if not excluded)
        - chart_data_breakdown (List[Dict]): Breakdown of volume per DEX over time (if not excluded)
        - metadata (Dict): Additional context like update time, chain status, data source

    Raises:
        ValueError: If chain is not provided or empty
    """
    if not chain or not chain.strip():
        raise ValueError("Chain parameter is required and cannot be empty")

    # Fetch simulated external API data
    api_data = call_external_api("defillama-api-server-get_overview_dexs__by_chain")

    # Construct DEXs list
    dexs = [
        {
            "name": api_data["dexs_0_name"],
            "slug": api_data["dexs_0_slug"],
            "logo": api_data["dexs_0_logo"],
            "total_volume": api_data["dexs_0_total_volume"],
            "volume_change_7d": api_data["dexs_0_volume_change_7d"]
        },
        {
            "name": api_data["dexs_1_name"],
            "slug": api_data["dexs_1_slug"],
            "logo": api_data["dexs_1_logo"],
            "total_volume": api_data["dexs_1_total_volume"],
            "volume_change_7d": api_data["dexs_1_volume_change_7d"]
        }
    ]

    # Construct top DEX info
    top_dex_by_volume = {
        "name": api_data["top_dex_by_volume_name"],
        "volume": api_data["top_dex_by_volume_volume"],
        "share": api_data["top_dex_by_volume_share"]
    }

    # Construct all chains list
    all_chains = [api_data["all_chains_0"], api_data["all_chains_1"]]

    # Conditionally include chart data
    chart_data = []
    if not excludeTotalDataChart:
        chart_data = [
            [api_data["chart_data_0_timestamp"], api_data["chart_data_0_volume"]],
            [api_data["chart_data_1_timestamp"], api_data["chart_data_1_volume"]]
        ]

    # Conditionally include chart breakdown
    chart_data_breakdown = []
    if not excludeTotalDataChartBreakdown:
        chart_data_breakdown = [
            {
                "timestamp": api_data["chart_data_breakdown_0_timestamp"],
                "dex_a": api_data["chart_data_breakdown_0_dex_a"],
                "dex_b": api_data["chart_data_breakdown_0_dex_b"]
            },
            {
                "timestamp": api_data["chart_data_breakdown_1_timestamp"],
                "dex_a": api_data["chart_data_breakdown_1_dex_a"],
                "dex_b": api_data["chart_data_breakdown_1_dex_b"]
            }
        ]

    # Construct metadata
    metadata = {
        "updated_at": api_data["metadata_updated_at"],
        "chain_status": api_data["metadata_chain_status"],
        "data_source": api_data["metadata_data_source"]
    }

    # Assemble final response
    result = {
        "dexs": dexs,
        "total_volume": api_data["total_volume"],
        "volume_change_7d": api_data["volume_change_7d"],
        "top_dex_by_volume": top_dex_by_volume,
        "all_chains": all_chains,
        "metadata": metadata
    }

    if chart_data:
        result["chart_data"] = chart_data

    if chart_data_breakdown:
        result["chart_data_breakdown"] = chart_data_breakdown

    return result