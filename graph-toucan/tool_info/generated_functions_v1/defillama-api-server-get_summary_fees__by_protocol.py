from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama protocol fees summary.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - data_0_date (int): Unix timestamp for first historical data point
        - data_0_total (float): Total value (e.g., dailyFees) for first data point
        - data_1_date (int): Unix timestamp for second historical data point
        - data_1_total (float): Total value (e.g., dailyFees) for second data point
        - protocol (str): Slug identifier of the protocol
        - dataType (str): Type of data returned (e.g., dailyFees, dailyRevenue)
        - totalValue (float): Sum of all values in the data array
        - startDate (int): Earliest Unix timestamp in the data series
        - endDate (int): Latest Unix timestamp in the data series
        - updated_at (int): Unix timestamp when data was last updated
        - chains_0 (str): First chain in breakdown
        - chains_1 (str): Second chain in breakdown
        - url (str): Source URL for the data
    """
    return {
        "data_0_date": 1672531200,
        "data_0_total": 125000.5,
        "data_1_date": 1672617600,
        "data_1_total": 132000.75,
        "protocol": "uniswap",
        "dataType": "dailyFees",
        "totalValue": 257001.25,
        "startDate": 1672531200,
        "endDate": 1672617600,
        "updated_at": 1672630000,
        "chains_0": "Ethereum",
        "chains_1": "Arbitrum",
        "url": "https://defillama.com/protocol/uniswap"
    }

def defillama_api_server_get_summary_fees_by_protocol(
    protocol: str, 
    dataType: Optional[str] = "dailyFees"
) -> Dict[str, Any]:
    """
    Get summary of protocol fees and revenue with historical data.
    
    Args:
        protocol (str): Protocol slug (required)
        dataType (str, optional): Desired data type, either 'dailyFees' or 'dailyRevenue'. Defaults to 'dailyFees'.
    
    Returns:
        Dict containing:
        - data (List[Dict]): List of historical data points with 'date' (Unix timestamp) and 'total' (numeric value)
        - protocol (str): Slug identifier of the protocol
        - dataType (str): Type of data returned
        - totalValue (float): Cumulative sum of all values in the data array
        - startDate (int): Earliest Unix timestamp in the data series
        - endDate (int): Latest Unix timestamp in the data series
        - metadata (Dict): Additional context including 'updated_at', 'chains', and 'url'
    
    Raises:
        ValueError: If protocol is not provided
    """
    if not protocol:
        raise ValueError("Parameter 'protocol' is required and cannot be empty.")
    
    if dataType not in ["dailyFees", "dailyRevenue"]:
        dataType = "dailyFees"  # default fallback
    
    # Call external API to get flattened data
    api_data = call_external_api("defillama-api-server-get_summary_fees__by_protocol")
    
    # Construct the data array from indexed fields
    data = [
        {"date": api_data["data_0_date"], "total": api_data["data_0_total"]},
        {"date": api_data["data_1_date"], "total": api_data["data_1_total"]}
    ]
    
    # Construct metadata
    metadata = {
        "updated_at": api_data["updated_at"],
        "chains": [api_data["chains_0"], api_data["chains_1"]],
        "url": api_data["url"]
    }
    
    # Build final result matching output schema
    result = {
        "data": data,
        "protocol": api_data["protocol"],
        "dataType": api_data["dataType"],
        "totalValue": api_data["totalValue"],
        "startDate": api_data["startDate"],
        "endDate": api_data["endDate"],
        "metadata": metadata
    }
    
    return result