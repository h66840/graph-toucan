from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for DefiLlama historical chain TVL.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - tvl_data_0_date (int): Unix timestamp for first TVL data point
        - tvl_data_0_totalLiquidityUSD (float): Total liquidity in USD for first data point
        - tvl_data_1_date (int): Unix timestamp for second TVL data point
        - tvl_data_1_totalLiquidityUSD (float): Total liquidity in USD for second data point
        - chains_0 (str): Name of first blockchain
        - chains_1 (str): Name of second blockchain
        - metadata_generatedAt (int): Unix timestamp when data was generated
        - metadata_description (str): Description of data scope
        - metadata_source (str): Source of the data
    """
    return {
        "tvl_data_0_date": 1672531200,
        "tvl_data_0_totalLiquidityUSD": 50000000000.0,
        "tvl_data_1_date": 1672617600,
        "tvl_data_1_totalLiquidityUSD": 51000000000.0,
        "chains_0": "Ethereum",
        "chains_1": "Binance Smart Chain",
        "metadata_generatedAt": 1672704000,
        "metadata_description": "Historical TVL excluding liquid staking and double counted TVL",
        "metadata_source": "DefiLlama"
    }

def defillama_api_server_get_v2_historicalChainTvl() -> Dict[str, Any]:
    """
    Get historical TVL (excludes liquid staking and double counted tvl) of DeFi on all chains.

    Returns:
        Dict containing:
        - tvl_data (List[Dict]): List of time-series entries with 'date' and 'totalLiquidityUSD'
        - chains (List[str]): List of blockchain names
        - metadata (Dict): Additional context including generatedAt, description, and source
    """
    try:
        api_data = call_external_api("defillama-api-server-get_v2_historicalChainTvl")
        
        # Construct tvl_data list from indexed fields
        tvl_data = [
            {
                "date": api_data["tvl_data_0_date"],
                "totalLiquidityUSD": api_data["tvl_data_0_totalLiquidityUSD"]
            },
            {
                "date": api_data["tvl_data_1_date"],
                "totalLiquidityUSD": api_data["tvl_data_1_totalLiquidityUSD"]
            }
        ]
        
        # Construct chains list from indexed fields
        chains = [
            api_data["chains_0"],
            api_data["chains_1"]
        ]
        
        # Construct metadata dictionary
        metadata = {
            "generatedAt": api_data["metadata_generatedAt"],
            "description": api_data["metadata_description"],
            "source": api_data["metadata_source"]
        }
        
        return {
            "tvl_data": tvl_data,
            "chains": chains,
            "metadata": metadata
        }
        
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to process historical chain TVL data: {str(e)}")