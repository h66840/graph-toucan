from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for trending search on CoinGecko.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - coin_0_name (str): First trending coin name
        - coin_0_symbol (str): First trending coin symbol
        - coin_0_price (float): First trending coin price in USD
        - coin_0_market_cap (float): First trending coin market cap in USD
        - coin_0_price_change_percentage_24h (float): First coin 24h price change percentage
        - coin_0_image_url (str): First trending coin image URL
        - coin_0_sparkline (str): First trending coin sparkline (comma-separated prices)
        - coin_0_market_cap_rank (int): First trending coin market cap rank
        - coin_1_name (str): Second trending coin name
        - coin_1_symbol (str): Second trending coin symbol
        - coin_1_price (float): Second trending coin price in USD
        - coin_1_market_cap (float): Second trending coin market cap in USD
        - coin_1_price_change_percentage_24h (float): Second coin 24h price change percentage
        - coin_1_image_url (str): Second trending coin image URL
        - coin_1_sparkline (str): Second trending coin sparkline (comma-separated prices)
        - coin_1_market_cap_rank (int): Second trending coin market cap rank
        - category_0_name (str): First trending category name
        - category_0_coin_count (int): Number of coins in first trending category
        - category_0_market_cap (float): Market cap of first trending category in USD
        - category_0_volume (float): Volume of first trending category in USD
        - category_0_24h_change_usd (float): 24h change in USD for first category
        - category_0_24h_change_btc (float): 24h change in BTC for first category
        - category_0_sparkline_url (str): Sparkline URL for first trending category
        - category_1_name (str): Second trending category name
        - category_1_coin_count (int): Number of coins in second trending category
        - category_1_market_cap (float): Market cap of second trending category in USD
        - category_1_volume (float): Volume of second trending category in USD
        - category_1_24h_change_usd (float): 24h change in USD for second category
        - category_1_24h_change_btc (float): 24h change in BTC for second category
        - category_1_sparkline_url (str): Sparkline URL for second trending category
        - nft_0_name (str): First trending NFT collection name
        - nft_0_symbol (str): First trending NFT collection symbol
        - nft_0_floor_price (float): Floor price of first NFT collection
        - nft_0_volume_24h (float): 24h volume of first NFT collection in native currency
        - nft_0_average_sale_price (float): Average sale price of first NFT collection
        - nft_0_price_change_percentage (float): Price change percentage of first NFT collection
        - nft_0_native_currency (str): Native currency of first NFT collection
        - nft_0_thumbnail (str): Thumbnail image URL of first NFT collection
        - nft_1_name (str): Second trending NFT collection name
        - nft_1_symbol (str): Second trending NFT collection symbol
        - nft_1_floor_price (float): Floor price of second NFT collection
        - nft_1_volume_24h (float): 24h volume of second NFT collection in native currency
        - nft_1_average_sale_price (float): Average sale price of second NFT collection
        - nft_1_price_change_percentage (float): Price change percentage of second NFT collection
        - nft_1_native_currency (str): Native currency of second NFT collection
        - nft_1_thumbnail (str): Thumbnail image URL of second NFT collection
    """
    return {
        "coin_0_name": "Bitcoin",
        "coin_0_symbol": "btc",
        "coin_0_price": 43500.0,
        "coin_0_market_cap": 857000000000.0,
        "coin_0_price_change_percentage_24h": 2.45,
        "coin_0_image_url": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        "coin_0_sparkline": "42000,42500,43000,43500",
        "coin_0_market_cap_rank": 1,
        "coin_1_name": "Ethereum",
        "coin_1_symbol": "eth",
        "coin_1_price": 2650.0,
        "coin_1_market_cap": 318000000000.0,
        "coin_1_price_change_percentage_24h": 3.12,
        "coin_1_image_url": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
        "coin_1_sparkline": "2580,2600,2630,2650",
        "coin_1_market_cap_rank": 2,
        "category_0_name": "Layer 1",
        "category_0_coin_count": 45,
        "category_0_market_cap": 1.2e+12,
        "category_0_volume": 35e+9,
        "category_0_24h_change_usd": 4.2,
        "category_0_24h_change_btc": 3.8,
        "category_0_sparkline_url": "https://sparkline.coingecko.com/layer1.png",
        "category_1_name": "DeFi",
        "category_1_coin_count": 120,
        "category_1_market_cap": 85e+9,
        "category_1_volume": 12e+9,
        "category_1_24h_change_usd": 5.1,
        "category_1_24h_change_btc": 4.7,
        "category_1_sparkline_url": "https://sparkline.coingecko.com/defi.png",
        "nft_0_name": "Bored Ape Yacht Club",
        "nft_0_symbol": "BAYC",
        "nft_0_floor_price": 12.5,
        "nft_0_volume_24h": 3.2,
        "nft_0_average_sale_price": 14.1,
        "nft_0_price_change_percentage": 8.3,
        "nft_0_native_currency": "ETH",
        "nft_0_thumbnail": "https://nft.coingecko.com/bayc.jpg",
        "nft_1_name": "CryptoPunks",
        "nft_1_symbol": "PUNKS",
        "nft_1_floor_price": 25.8,
        "nft_1_volume_24h": 5.7,
        "nft_1_average_sale_price": 27.3,
        "nft_1_price_change_percentage": -2.1,
        "nft_1_native_currency": "ETH",
        "nft_1_thumbnail": "https://nft.coingecko.com/punks.jpg"
    }

def coingecko_api_server_API_trending_search() -> Dict[str, Any]:
    """
    Fetches and returns the current trending search data from CoinGecko API,
    including trending coins, categories, and NFT collections.

    Returns:
        Dict containing:
        - coins (List[Dict]): List of trending coins with name, symbol, price,
          market cap, 24h change, image URLs, sparkline, and market cap rank
        - categories (List[Dict]): List of trending categories with name,
          coin count, market cap, volume, 24h changes in USD/BTC, and sparkline URL
        - nfts (List[Dict]): List of trending NFTs with name, symbol, floor price,
          24h volume, average sale price, price change percentage, native currency,
          and thumbnail image
    """
    try:
        api_data = call_external_api("coingecko-api-server-API-trending-search")

        coins = [
            {
                "name": api_data["coin_0_name"],
                "symbol": api_data["coin_0_symbol"],
                "price": api_data["coin_0_price"],
                "market_cap": api_data["coin_0_market_cap"],
                "price_change_percentage_24h": api_data["coin_0_price_change_percentage_24h"],
                "image_url": api_data["coin_0_image_url"],
                "sparkline": api_data["coin_0_sparkline"],
                "market_cap_rank": api_data["coin_0_market_cap_rank"]
            },
            {
                "name": api_data["coin_1_name"],
                "symbol": api_data["coin_1_symbol"],
                "price": api_data["coin_1_price"],
                "market_cap": api_data["coin_1_market_cap"],
                "price_change_percentage_24h": api_data["coin_1_price_change_percentage_24h"],
                "image_url": api_data["coin_1_image_url"],
                "sparkline": api_data["coin_1_sparkline"],
                "market_cap_rank": api_data["coin_1_market_cap_rank"]
            }
        ]

        categories = [
            {
                "name": api_data["category_0_name"],
                "coin_count": api_data["category_0_coin_count"],
                "market_cap": api_data["category_0_market_cap"],
                "volume": api_data["category_0_volume"],
                "24h_change_usd": api_data["category_0_24h_change_usd"],
                "24h_change_btc": api_data["category_0_24h_change_btc"],
                "sparkline_url": api_data["category_0_sparkline_url"]
            },
            {
                "name": api_data["category_1_name"],
                "coin_count": api_data["category_1_coin_count"],
                "market_cap": api_data["category_1_market_cap"],
                "volume": api_data["category_1_volume"],
                "24h_change_usd": api_data["category_1_24h_change_usd"],
                "24h_change_btc": api_data["category_1_24h_change_btc"],
                "sparkline_url": api_data["category_1_sparkline_url"]
            }
        ]

        nfts = [
            {
                "name": api_data["nft_0_name"],
                "symbol": api_data["nft_0_symbol"],
                "floor_price": api_data["nft_0_floor_price"],
                "volume_24h": api_data["nft_0_volume_24h"],
                "average_sale_price": api_data["nft_0_average_sale_price"],
                "price_change_percentage": api_data["nft_0_price_change_percentage"],
                "native_currency": api_data["nft_0_native_currency"],
                "thumbnail": api_data["nft_0_thumbnail"]
            },
            {
                "name": api_data["nft_1_name"],
                "symbol": api_data["nft_1_symbol"],
                "floor_price": api_data["nft_1_floor_price"],
                "volume_24h": api_data["nft_1_volume_24h"],
                "average_sale_price": api_data["nft_1_average_sale_price"],
                "price_change_percentage": api_data["nft_1_price_change_percentage"],
                "native_currency": api_data["nft_1_native_currency"],
                "thumbnail": api_data["nft_1_thumbnail"]
            }
        ]

        return {
            "coins": coins,
            "categories": categories,
            "nfts": nfts
        }

    except Exception as e:
        # In case of any error, return empty data structure
        return {
            "coins": [],
            "categories": [],
            "nfts": []
        }