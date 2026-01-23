from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama overview fees.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - protocol_0_name (str): Name of the first protocol
        - protocol_0_slug (str): Slug of the first protocol
        - protocol_0_category (str): Category of the first protocol
        - protocol_0_chains (str): Comma-separated chains for the first protocol
        - protocol_0_dailyFees (float): Daily fees for the first protocol
        - protocol_0_dailyRevenue (float): Daily revenue for the first protocol
        - protocol_0_historicalData (str): JSON string of historical data for the first protocol
        - protocol_1_name (str): Name of the second protocol
        - protocol_1_slug (str): Slug of the second protocol
        - protocol_1_category (str): Category of the second protocol
        - protocol_1_chains (str): Comma-separated chains for the second protocol
        - protocol_1_dailyFees (float): Daily fees for the second protocol
        - protocol_1_dailyRevenue (float): Daily revenue for the second protocol
        - protocol_1_historicalData (str): JSON string of historical data for the second protocol
        - total_fees (float): Total aggregated fees across all protocols
        - total_revenue (float): Total aggregated revenue across all protocols
        - timestamp (int): Unix timestamp of data generation
        - metadata_dataType (str): Data type used in the request
        - metadata_excludeTotalDataChart (bool): Whether aggregated chart was excluded
        - metadata_excludeTotalDataChartBreakdown (bool): Whether breakdown chart was excluded
    """
    return {
        "protocol_0_name": "Uniswap",
        "protocol_0_slug": "uniswap",
        "protocol_0_category": "Dexes",
        "protocol_0_chains": "Ethereum,Arbitrum",
        "protocol_0_dailyFees": 2500000.0,
        "protocol_0_dailyRevenue": 500000.0,
        "protocol_0_historicalData": '[{"date": 1672531200, "dailyFees": 2400000}, {"date": 1672617600, "dailyFees": 2500000}]',
        "protocol_1_name": "Aave",
        "protocol_1_slug": "aave",
        "protocol_1_category": "Lending",
        "protocol_1_chains": "Ethereum,Polygon",
        "protocol_1_dailyFees": 1800000.0,
        "protocol_1_dailyRevenue": 360000.0,
        "protocol_1_historicalData": '[{"date": 1672531200, "dailyFees": 1750000}, {"date": 1672617600, "dailyFees": 1800000}]',
        "total_fees": 4300000.0,
        "total_revenue": 860000.0,
        "timestamp": 1672704000,
        "metadata_dataType": "dailyFees",
        "metadata_excludeTotalDataChart": False,
        "metadata_excludeTotalDataChartBreakdown": False
    }

def defillama_api_server_get_overview_fees(
    dataType: Optional[str] = "dailyFees",
    excludeTotalDataChart: Optional[bool] = False,
    excludeTotalDataChartBreakdown: Optional[bool] = False
) -> Dict[str, Any]:
    """
    List all protocols along with summaries of their fees and revenue and dataType history data.

    Args:
        dataType (Optional[str]): Desired data type, dailyFees by default.
        excludeTotalDataChart (Optional[bool]): True to exclude aggregated chart from response.
        excludeTotalDataChartBreakdown (Optional[bool]): True to exclude broken down chart from response.

    Returns:
        Dict containing:
        - protocols (List[Dict]): List of protocol objects with fields like name, slug, category, chains,
          dailyFees, dailyRevenue, and historicalData.
        - total_fees (float): Total aggregated fees across all protocols.
        - total_revenue (float): Total aggregated revenue across all protocols.
        - timestamp (int): Unix timestamp indicating when the data was generated.
        - metadata (Dict): Additional context including applied filters, dataType used, and source info.

    Raises:
        ValueError: If dataType is not a valid string.
    """
    # Input validation
    if dataType is not None and not isinstance(dataType, str):
        raise ValueError("dataType must be a string or None")
    if not isinstance(excludeTotalDataChart, bool):
        raise ValueError("excludeTotalDataChart must be a boolean")
    if not isinstance(excludeTotalDataChartBreakdown, bool):
        raise ValueError("excludeTotalDataChartBreakdown must be a boolean")

    # Call external API (simulated)
    raw_data = call_external_api("defillama-api-server-get_overview_fees")

    # Construct protocols list from flattened fields
    protocols = [
        {
            "name": raw_data["protocol_0_name"],
            "slug": raw_data["protocol_0_slug"],
            "category": raw_data["protocol_0_category"],
            "chains": raw_data["protocol_0_chains"].split(","),
            "dailyFees": raw_data["protocol_0_dailyFees"],
            "dailyRevenue": raw_data["protocol_0_dailyRevenue"],
            "historicalData": raw_data["protocol_0_historicalData"]
        },
        {
            "name": raw_data["protocol_1_name"],
            "slug": raw_data["protocol_1_slug"],
            "category": raw_data["protocol_1_category"],
            "chains": raw_data["protocol_1_chains"].split(","),
            "dailyFees": raw_data["protocol_1_dailyFees"],
            "dailyRevenue": raw_data["protocol_1_dailyRevenue"],
            "historicalData": raw_data["protocol_1_historicalData"]
        }
    ]

    # Build metadata
    metadata = {
        "dataType": dataType or "dailyFees",
        "excludeTotalDataChart": excludeTotalDataChart,
        "excludeTotalDataChartBreakdown": excludeTotalDataChartBreakdown
    }

    # Construct final result
    result = {
        "protocols": protocols,
        "total_fees": raw_data["total_fees"],
        "total_revenue": raw_data["total_revenue"],
        "timestamp": raw_data["timestamp"],
        "metadata": metadata
    }

    return result