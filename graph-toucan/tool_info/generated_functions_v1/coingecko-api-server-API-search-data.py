from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CoinGecko search functionality.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - coin_0_id (str): First coin ID
        - coin_0_name (str): First coin name
        - coin_0_api_symbol (str): First coin API symbol
        - coin_0_symbol (str): First coin symbol
        - coin_0_market_cap_rank (int): First coin market cap rank
        - coin_0_thumb (str): First coin thumbnail URL
        - coin_0_large (str): First coin large image URL
        - coin_1_id (str): Second coin ID
        - coin_1_name (str): Second coin name
        - coin_1_api_symbol (str): Second coin API symbol
        - coin_1_symbol (str): Second coin symbol
        - coin_1_market_cap_rank (int): Second coin market cap rank
        - coin_1_thumb (str): Second coin thumbnail URL
        - coin_1_large (str): Second coin large image URL
        - exchange_0_id (str): First exchange ID
        - exchange_0_name (str): First exchange name
        - exchange_0_market_type (str): First exchange market type
        - exchange_0_thumb (str): First exchange thumbnail URL
        - exchange_0_large (str): First exchange large image URL
        - exchange_1_id (str): Second exchange ID
        - exchange_1_name (str): Second exchange name
        - exchange_1_market_type (str): Second exchange market type
        - exchange_1_thumb (str): Second exchange thumbnail URL
        - exchange_1_large (str): Second exchange large image URL
        - ico_0 (str): First ICO name
        - ico_1 (str): Second ICO name
        - category_0_id (str): First category ID
        - category_0_name (str): First category name
        - category_1_id (str): Second category ID
        - category_1_name (str): Second category name
        - nft_0_id (str): First NFT collection ID
        - nft_0_name (str): First NFT collection name
        - nft_0_symbol (str): First NFT collection symbol
        - nft_0_thumb (str): First NFT collection thumbnail URL
        - nft_1_id (str): Second NFT collection ID
        - nft_1_name (str): Second NFT collection name
        - nft_1_symbol (str): Second NFT collection symbol
        - nft_1_thumb (str): Second NFT collection thumbnail URL
    """
    return {
        "coin_0_id": "bitcoin",
        "coin_0_name": "Bitcoin",
        "coin_0_api_symbol": "btc",
        "coin_0_symbol": "BTC",
        "coin_0_market_cap_rank": 1,
        "coin_0_thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png",
        "coin_0_large": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        "coin_1_id": "ethereum",
        "coin_1_name": "Ethereum",
        "coin_1_api_symbol": "eth",
        "coin_1_symbol": "ETH",
        "coin_1_market_cap_rank": 2,
        "coin_1_thumb": "https://assets.coingecko.com/coins/images/279/thumb/ethereum.png",
        "coin_1_large": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
        "exchange_0_id": "binance",
        "exchange_0_name": "Binance",
        "exchange_0_market_type": "centralized",
        "exchange_0_thumb": "https://assets.coingecko.com/markets/images/53/thumb/binance.jpg",
        "exchange_0_large": "https://assets.coingecko.com/markets/images/53/large/binance.jpg",
        "exchange_1_id": "coinbase_exchange",
        "exchange_1_name": "Coinbase Exchange",
        "exchange_1_market_type": "centralized",
        "exchange_1_thumb": "https://assets.coingecko.com/markets/images/81/thumb/coinbase.png",
        "exchange_1_large": "https://assets.coingecko.com/markets/images/81/large/coinbase.png",
        "ico_0": "Ethereum",
        "ico_1": "Cardano",
        "category_0_id": "blockchain",
        "category_0_name": "Blockchain",
        "category_1_id": "smart-contracts",
        "category_1_name": "Smart Contracts",
        "nft_0_id": "cryptopunks",
        "nft_0_name": "CryptoPunks",
        "nft_0_symbol": "PUNK",
        "nft_0_thumb": "https://assets.coingecko.com/nft_collections/images/1/thumb/cryptopunks.jpg",
        "nft_1_id": "bored-ape-yacht-club",
        "nft_1_name": "Bored Ape Yacht Club",
        "nft_1_symbol": "BAYC",
        "nft_1_thumb": "https://assets.coingecko.com/nft_collections/images/2/thumb/bored-ape.jpg"
    }

def coingecko_api_server_API_search_data(query: str) -> Dict[str, Any]:
    """
    Search for coins, exchanges, ICOs, categories, and NFTs based on a query string.
    
    Args:
        query (str): The search query string (required)
    
    Returns:
        Dict containing search results with the following structure:
        - coins (List[Dict]): List of coin search results with 'id', 'name', 'api_symbol', 
          'symbol', 'market_cap_rank', 'thumb', and 'large' fields
        - exchanges (List[Dict]): List of exchange search results with 'id', 'name', 
          'market_type', 'thumb', and 'large' fields
        - icos (List[str]): List of initial coin offering (ICO) names matching the search query
        - categories (List[Dict]): List of category results with 'id' and 'name' fields
        - nfts (List[Dict]): List of NFT collection results with 'id', 'name', 'symbol', 
          'thumb', and potentially other metadata fields
    
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query:
        raise ValueError("Query parameter is required")
    if not isinstance(query, str):
        raise ValueError("Query must be a string")
    
    # Fetch simulated external API data
    api_data = call_external_api("coingecko-api-server-API-search-data")
    
    # Construct coins list
    coins = [
        {
            "id": api_data["coin_0_id"],
            "name": api_data["coin_0_name"],
            "api_symbol": api_data["coin_0_api_symbol"],
            "symbol": api_data["coin_0_symbol"],
            "market_cap_rank": api_data["coin_0_market_cap_rank"],
            "thumb": api_data["coin_0_thumb"],
            "large": api_data["coin_0_large"]
        },
        {
            "id": api_data["coin_1_id"],
            "name": api_data["coin_1_name"],
            "api_symbol": api_data["coin_1_api_symbol"],
            "symbol": api_data["coin_1_symbol"],
            "market_cap_rank": api_data["coin_1_market_cap_rank"],
            "thumb": api_data["coin_1_thumb"],
            "large": api_data["coin_1_large"]
        }
    ]
    
    # Construct exchanges list
    exchanges = [
        {
            "id": api_data["exchange_0_id"],
            "name": api_data["exchange_0_name"],
            "market_type": api_data["exchange_0_market_type"],
            "thumb": api_data["exchange_0_thumb"],
            "large": api_data["exchange_0_large"]
        },
        {
            "id": api_data["exchange_1_id"],
            "name": api_data["exchange_1_name"],
            "market_type": api_data["exchange_1_market_type"],
            "thumb": api_data["exchange_1_thumb"],
            "large": api_data["exchange_1_large"]
        }
    ]
    
    # Construct icos list
    icos = [
        api_data["ico_0"],
        api_data["ico_1"]
    ]
    
    # Construct categories list
    categories = [
        {
            "id": api_data["category_0_id"],
            "name": api_data["category_0_name"]
        },
        {
            "id": api_data["category_1_id"],
            "name": api_data["category_1_name"]
        }
    ]
    
    # Construct nfts list
    nfts = [
        {
            "id": api_data["nft_0_id"],
            "name": api_data["nft_0_name"],
            "symbol": api_data["nft_0_symbol"],
            "thumb": api_data["nft_0_thumb"]
        },
        {
            "id": api_data["nft_1_id"],
            "name": api_data["nft_1_name"],
            "symbol": api_data["nft_1_symbol"],
            "thumb": api_data["nft_1_thumb"]
        }
    ]
    
    return {
        "coins": coins,
        "exchanges": exchanges,
        "icos": icos,
        "categories": categories,
        "nfts": nfts
    }