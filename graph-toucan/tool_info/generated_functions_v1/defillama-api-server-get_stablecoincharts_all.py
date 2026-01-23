from typing import Dict, List, Any, Optional
import random
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for stablecoin charts.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - data_0_date (int): Unix timestamp for first time-series entry
        - data_0_totalCirculating (float): Total circulating market cap at first date
        - data_1_date (int): Unix timestamp for second time-series entry
        - data_1_totalCirculating (float): Total circulating market cap at second date
        - metadata_generated_at (int): Unix timestamp when response was generated
        - metadata_stablecoin_count (int): Number of stablecoins included in calculation
        - metadata_source_url (str): Reference API endpoint or data source URL
    """
    current_time = int(time.time())
    return {
        "data_0_date": current_time - 86400,  # 24 hours ago
        "data_0_totalCirculating": 125.5e9 + random.uniform(-5e9, 5e9),  # ~$125.5B with noise
        "data_1_date": current_time,  # now
        "data_1_totalCirculating": 126.0e9 + random.uniform(-5e9, 5e9),  # ~$126B with noise
        "metadata_generated_at": current_time,
        "metadata_stablecoin_count": 25,
        "metadata_source_url": "https://api.llama.fi/stablecoinCharts/all"
    }


def defillama_api_server_get_stablecoincharts_all(stablecoin: Optional[int] = None) -> Dict[str, Any]:
    """
    Get historical market cap sum of all stablecoins.

    This function retrieves time-series data representing the total circulating
    market cap of all stablecoins over time. It returns a list of data points
    with timestamps and values, along with metadata about the response.

    Args:
        stablecoin (Optional[int]): Stablecoin ID to filter by (optional).
            If provided, may influence results (though this is simulated).

    Returns:
        Dict containing:
        - data (List[Dict]): List of time-series entries with 'date' (Unix timestamp)
          and 'totalCirculating' (float, total market cap in USD)
        - metadata (Dict): Additional context including:
          - generated_at (int): Unix timestamp of response generation
          - stablecoin_count (int): Number of stablecoins included
          - source_url (str): Reference data source

    Note:
        In a real implementation, this would call an external API.
        Here, we simulate the response using call_external_api helper.
    """
    # Validate input
    if stablecoin is not None and (not isinstance(stablecoin, int) or stablecoin < 0):
        raise ValueError("Stablecoin ID must be a non-negative integer if provided.")

    # Fetch simulated external data
    api_data = call_external_api("defillama-api-server-get_stablecoincharts_all")

    # Construct the data list from flattened fields
    data = [
        {
            "date": api_data["data_0_date"],
            "totalCirculating": api_data["data_0_totalCirculating"]
        },
        {
            "date": api_data["data_1_date"],
            "totalCirculating": api_data["data_1_totalCirculating"]
        }
    ]

    # Construct metadata
    metadata = {
        "generated_at": api_data["metadata_generated_at"],
        "stablecoin_count": api_data["metadata_stablecoin_count"],
        "source_url": api_data["metadata_source_url"]
    }

    # Return final structured response
    return {
        "data": data,
        "metadata": metadata
    }