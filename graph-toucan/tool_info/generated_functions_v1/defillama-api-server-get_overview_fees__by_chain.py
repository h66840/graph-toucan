from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama fees overview by chain.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - protocol_0_name (str): Name of the first protocol
        - protocol_0_slug (str): Slug of the first protocol
        - protocol_0_category (str): Category of the first protocol
        - protocol_0_dailyFees (float): Daily fees for the first protocol
        - protocol_0_dailyRevenue (float): Daily revenue for the first protocol
        - protocol_1_name (str): Name of the second protocol
        - protocol_1_slug (str): Slug of the second protocol
        - protocol_1_category (str): Category of the second protocol
        - protocol_1_dailyFees (float): Daily fees for the second protocol
        - protocol_1_dailyRevenue (float): Daily revenue for the second protocol
        - total_data_chart_0_timestamp (int): First timestamp in total data chart
        - total_data_chart_0_value (float): Value at first timestamp in total data chart
        - total_data_chart_1_timestamp (int): Second timestamp in total data chart
        - total_data_chart_1_value (float): Value at second timestamp in total data chart
        - total_data_chart_breakdown_protocol_0_slug (str): Slug for breakdown of first protocol
        - total_data_chart_breakdown_protocol_0_0_timestamp (int): First timestamp for breakdown of first protocol
        - total_data_chart_breakdown_protocol_0_0_value (float): First value for breakdown of first protocol
        - total_data_chart_breakdown_protocol_0_1_timestamp (int): Second timestamp for breakdown of first protocol
        - total_data_chart_breakdown_protocol_0_1_value (float): Second value for breakdown of first protocol
        - total_data_chart_breakdown_protocol_1_slug (str): Slug for breakdown of second protocol
        - total_data_chart_breakdown_protocol_1_0_timestamp (int): First timestamp for breakdown of second protocol
        - total_data_chart_breakdown_protocol_1_0_value (float): First value for breakdown of second protocol
        - total_data_chart_breakdown_protocol_1_1_timestamp (int): Second timestamp for breakdown of second protocol
        - total_data_chart_breakdown_protocol_1_1_value (float): Second value for breakdown of second protocol
        - chain (str): Name of the chain
        - data_type (str): Type of data returned (e.g., dailyFees)
        - all_chains_0 (str): First supported chain
        - all_chains_1 (str): Second supported chain
        - timestamp (int): Unix timestamp when response was generated
        - meta_api_version (str): API version
        - meta_next_update (int): Unix timestamp for next update
        - meta_warnings (str): Any warnings from the service
    """
    return {
        "protocol_0_name": "Uniswap",
        "protocol_0_slug": "uniswap",
        "protocol_0_category": "Dexes",
        "protocol_0_dailyFees": 2500000.0,
        "protocol_0_dailyRevenue": 500000.0,
        "protocol_1_name": "SushiSwap",
        "protocol_1_slug": "sushiswap",
        "protocol_1_category": "Dexes",
        "protocol_1_dailyFees": 800000.0,
        "protocol_1_dailyRevenue": 160000.0,
        "total_data_chart_0_timestamp": 1672531200,
        "total_data_chart_0_value": 3300000.0,
        "total_data_chart_1_timestamp": 1672617600,
        "total_data_chart_1_value": 3700000.0,
        "total_data_chart_breakdown_protocol_0_slug": "uniswap",
        "total_data_chart_breakdown_protocol_0_0_timestamp": 1672531200,
        "total_data_chart_breakdown_protocol_0_0_value": 2500000.0,
        "total_data_chart_breakdown_protocol_0_1_timestamp": 1672617600,
        "total_data_chart_breakdown_protocol_0_1_value": 2700000.0,
        "total_data_chart_breakdown_protocol_1_slug": "sushiswap",
        "total_data_chart_breakdown_protocol_1_0_timestamp": 1672531200,
        "total_data_chart_breakdown_protocol_1_0_value": 800000.0,
        "total_data_chart_breakdown_protocol_1_1_timestamp": 1672617600,
        "total_data_chart_breakdown_protocol_1_1_value": 1000000.0,
        "chain": "Ethereum",
        "data_type": "dailyFees",
        "all_chains_0": "Ethereum",
        "all_chains_1": "Binance Smart Chain",
        "timestamp": 1672704000,
        "meta_api_version": "1.0",
        "meta_next_update": 1672707600,
        "meta_warnings": "Data may be preliminary for recent dates"
    }

def defillama_api_server_get_overview_fees_by_chain(
    chain: str,
    dataType: Optional[str] = None,
    excludeTotalDataChart: Optional[bool] = None,
    excludeTotalDataChartBreakdown: Optional[bool] = None
) -> Dict[str, Any]:
    """
    List all protocols along with summaries of their fees and revenue and dataType history data by chain.
    
    Args:
        chain (str): Chain name, list of all supported chains can be found under allChains attribute in /overview/fees response
        dataType (str, optional): Desired data type, dailyFees by default.
        excludeTotalDataChart (bool, optional): True to exclude aggregated chart from response
        excludeTotalDataChartBreakdown (bool, optional): True to exclude broken down chart from response
    
    Returns:
        Dict containing:
        - protocols (List[Dict]): List of protocol objects containing fee and revenue summaries
        - total_data_chart (List[List[int]]): Aggregated historical data points for the requested dataType
        - total_data_chart_breakdown (Dict): Breakdown of the total data chart by individual protocol
        - chain (str): Name of the chain for which data was fetched
        - data_type (str): The type of data returned
        - all_chains (List[str]): List of all supported chains available in the API
        - timestamp (int): Unix timestamp indicating when the response was generated
        - meta (Dict): Additional metadata such as API version, next_update, and any warnings
    """
    # Input validation
    if not chain:
        raise ValueError("Parameter 'chain' is required and cannot be empty")
    
    # Set default values
    if dataType is None:
        dataType = "dailyFees"
    
    # Call external API to get flat data
    api_data = call_external_api("defillama_api_server_get_overview_fees__by_chain")
    
    # Construct protocols list
    protocols = [
        {
            "name": api_data["protocol_0_name"],
            "slug": api_data["protocol_0_slug"],
            "category": api_data["protocol_0_category"],
            "dailyFees": api_data["protocol_0_dailyFees"],
            "dailyRevenue": api_data["protocol_0_dailyRevenue"]
        },
        {
            "name": api_data["protocol_1_name"],
            "slug": api_data["protocol_1_slug"],
            "category": api_data["protocol_1_category"],
            "dailyFees": api_data["protocol_1_dailyFees"],
            "dailyRevenue": api_data["protocol_1_dailyRevenue"]
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
            api_data["total_data_chart_breakdown_protocol_0_slug"]: [
                [api_data["total_data_chart_breakdown_protocol_0_0_timestamp"], api_data["total_data_chart_breakdown_protocol_0_0_value"]],
                [api_data["total_data_chart_breakdown_protocol_0_1_timestamp"], api_data["total_data_chart_breakdown_protocol_0_1_value"]]
            ],
            api_data["total_data_chart_breakdown_protocol_1_slug"]: [
                [api_data["total_data_chart_breakdown_protocol_1_0_timestamp"], api_data["total_data_chart_breakdown_protocol_1_0_value"]],
                [api_data["total_data_chart_breakdown_protocol_1_1_timestamp"], api_data["total_data_chart_breakdown_protocol_1_1_value"]]
            ]
        }
    
    # Construct all_chains list
    all_chains = [
        api_data["all_chains_0"],
        api_data["all_chains_1"]
    ]
    
    # Construct meta
    meta = {
        "api_version": api_data["meta_api_version"],
        "next_update": api_data["meta_next_update"],
        "warnings": api_data["meta_warnings"]
    }
    
    # Return final response
    return {
        "protocols": protocols,
        "total_data_chart": total_data_chart,
        "total_data_chart_breakdown": total_data_chart_breakdown,
        "chain": api_data["chain"],
        "data_type": api_data["data_type"],
        "all_chains": all_chains,
        "timestamp": api_data["timestamp"],
        "meta": meta
    }