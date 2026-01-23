from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for CoinGecko coin data by ID.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - id (str): Unique identifier for the cryptocurrency
        - name (str): Full name of the cryptocurrency
        - symbol (str): Symbol or ticker symbol of the cryptocurrency
        - web_slug (str): Web-friendly slug used in URLs
        - asset_platform_id (str): Platform ID on which the coin is based
        - block_time_in_minutes (int): Average block time in minutes
        - hashing_algorithm (str): Hashing algorithm used by the blockchain
        - category_0 (str): First category the cryptocurrency belongs to
        - category_1 (str): Second category the cryptocurrency belongs to
        - public_notice (str): Public notice related to the cryptocurrency
        - additional_notice_0 (str): First additional notice
        - additional_notice_1 (str): Second additional notice
        - genesis_date (str): Date when the blockchain's genesis block was created
        - country_origin (str): Country of origin for the cryptocurrency
        - sentiment_votes_up_percentage (float): Percentage of positive sentiment votes
        - sentiment_votes_down_percentage (float): Percentage of negative sentiment votes
        - watchlist_portfolio_users (int): Number of users who have added this coin to their watchlist
        - description_en (str): English description of the cryptocurrency
        - link_homepage_0 (str): First homepage URL
        - link_homepage_1 (str): Second homepage URL
        - link_blockchain_site_0 (str): First blockchain explorer URL
        - link_blockchain_site_1 (str): Second blockchain explorer URL
        - link_twitter (str): Twitter profile URL
        - image_thumb (str): Thumbnail image URL
        - image_small (str): Small image URL
        - image_large (str): Large image URL
        - market_data_current_price_usd (float): Current price in USD
        - market_data_current_price_btc (float): Current price in BTC
        - market_data_market_cap_usd (float): Market cap in USD
        - market_data_total_volume_usd (float): Total trading volume in USD
        - market_data_circulating_supply (float): Circulating supply
        - market_data_total_supply (float): Total supply
        - community_data_reddit_subscribers (int): Reddit subscribers count
        - community_data_twitter_followers (int): Twitter followers count
        - community_data_facebook_likes (int): Facebook page likes
        - developer_data_github_stars (int): GitHub repository stars
        - developer_data_github_forks (int): GitHub repository forks
        - developer_data_commits_last_4_weeks (int): Number of commits in last 4 weeks
        - status_update_0_description (str): First status update description
        - status_update_0_category (str): First status update category
        - status_update_1_description (str): Second status update description
        - status_update_1_category (str): Second status update category
        - ticker_0_base (str): First ticker base currency
        - ticker_0_target (str): First ticker target currency
        - ticker_0_market_name (str): First ticker exchange name
        - ticker_0_last_price (float): First ticker last traded price
        - ticker_0_volume (float): First ticker 24h volume
        - ticker_1_base (str): Second ticker base currency
        - ticker_1_target (str): Second ticker target currency
        - ticker_1_market_name (str): Second ticker exchange name
        - ticker_1_last_price (float): Second ticker last traded price
        - ticker_1_volume (float): Second ticker 24h volume
        - platform_ethereum (str): Ethereum contract address
        - platform_bsc (str): Binance Smart Chain contract address
        - detail_platform_ethereum_contract_address (str): Ethereum contract address in detail
        - detail_platform_bsc_contract_address (str): BSC contract address in detail
        - localization_en (str): Localized name in English
        - localization_zh (str): Localized name in Chinese
        - last_updated (str): Timestamp when the data was last updated
    """
    return {
        "id": "bitcoin",
        "name": "Bitcoin",
        "symbol": "btc",
        "web_slug": "bitcoin",
        "asset_platform_id": "ethereum",
        "block_time_in_minutes": 10,
        "hashing_algorithm": "SHA-256",
        "category_0": "cryptocurrency",
        "category_1": "store-of-value",
        "public_notice": "Open source decentralized cryptocurrency.",
        "additional_notice_0": "Not legal tender.",
        "additional_notice_1": "Use at your own risk.",
        "genesis_date": "2009-01-03",
        "country_origin": "USA",
        "sentiment_votes_up_percentage": 65.5,
        "sentiment_votes_down_percentage": 34.5,
        "watchlist_portfolio_users": 5000000,
        "description_en": "Bitcoin is a decentralized digital currency that enables instant payments to anyone, anywhere in the world.",
        "link_homepage_0": "https://bitcoin.org",
        "link_homepage_1": "https://bitcoincore.org",
        "link_blockchain_site_0": "https://blockchain.com",
        "link_blockchain_site_1": "https://blockstream.info",
        "link_twitter": "https://twitter.com/bitcoin",
        "image_thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png",
        "image_small": "https://assets.coingecko.com/coins/images/1/small/bitcoin.png",
        "image_large": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
        "market_data_current_price_usd": 45000.0,
        "market_data_current_price_btc": 1.0,
        "market_data_market_cap_usd": 880000000000.0,
        "market_data_total_volume_usd": 25000000000.0,
        "market_data_circulating_supply": 19500000.0,
        "market_data_total_supply": 21000000.0,
        "community_data_reddit_subscribers": 1500000,
        "community_data_twitter_followers": 750000,
        "community_data_facebook_likes": 250000,
        "developer_data_github_stars": 70000,
        "developer_data_github_forks": 35000,
        "developer_data_commits_last_4_weeks": 1200,
        "status_update_0_description": "Network upgrade scheduled.",
        "status_update_0_category": "network",
        "status_update_1_description": "New wallet release.",
        "status_update_1_category": "software",
        "ticker_0_base": "BTC",
        "ticker_0_target": "USD",
        "ticker_0_market_name": "Coinbase",
        "ticker_0_last_price": 45000.0,
        "ticker_0_volume": 500000000.0,
        "ticker_1_base": "BTC",
        "ticker_1_target": "EUR",
        "ticker_1_market_name": "Kraken",
        "ticker_1_last_price": 41500.0,
        "ticker_1_volume": 300000000.0,
        "platform_ethereum": "0x...",
        "platform_bsc": "0x...",
        "detail_platform_ethereum_contract_address": "0x...",
        "detail_platform_bsc_contract_address": "0x...",
        "localization_en": "Bitcoin",
        "localization_zh": "比特币",
        "last_updated": "2023-10-05T12:34:56Z"
    }


def coingecko_api_server_API_coins_id(
    id: str,
    community_data: Optional[bool] = True,
    developer_data: Optional[bool] = True,
    localization: Optional[bool] = True,
    market_data: Optional[bool] = True,
    sparkline: Optional[bool] = False,
    tickers: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Fetches cryptocurrency data by coin ID from CoinGecko API.

    Args:
        id (str): Coin ID (required). Refers to /coins/list endpoint.
        community_data (bool, optional): Include community data. Defaults to True.
        developer_data (bool, optional): Include developer data. Defaults to True.
        localization (bool, optional): Include localized names. Defaults to True.
        market_data (bool, optional): Include market data. Defaults to True.
        sparkline (bool, optional): Include sparkline 7 days data. Defaults to False.
        tickers (bool, optional): Include tickers data. Defaults to True.

    Returns:
        Dict containing detailed cryptocurrency information with the following structure:
        - id (str)
        - name (str)
        - symbol (str)
        - web_slug (str)
        - asset_platform_id (str)
        - block_time_in_minutes (int)
        - hashing_algorithm (str)
        - categories (list of str)
        - public_notice (str)
        - additional_notices (list of str)
        - genesis_date (str)
        - country_origin (str)
        - sentiment_votes_up_percentage (float)
        - sentiment_votes_down_percentage (float)
        - watchlist_portfolio_users (int)
        - description (dict with language codes as keys and text as values)
        - links (dict with various link types)
        - image (dict with thumb, small, large URLs)
        - market_data (dict with current_price, market_cap, total_volume, etc.)
        - community_data (dict with reddit, twitter, facebook stats)
        - developer_data (dict with github stats and commit activity)
        - status_updates (list of dicts with description and category)
        - tickers (list of dicts with base, target, market, last_price, volume, etc.)
        - platform (dict with contract addresses by platform)
        - localization (dict with names in various languages)
        - last_updated (str)
    """
    result = call_external_api("coingecko_api_server_API_coins_id")
    filtered_result = {}

    # Always include basic fields
    basic_fields = [
        "id", "name", "symbol", "web_slug", "asset_platform_id",
        "block_time_in_minutes", "hashing_algorithm", "genesis_date",
        "country_origin", "public_notice", "last_updated"
    ]
    for field in basic_fields:
        if field in result:
            filtered_result[field] = result[field]

    # Add categories
    categories = []
    if result.get("category_0"):
        categories.append(result["category_0"])
    if result.get("category_1"):
        categories.append(result["category_1"])
    filtered_result["categories"] = categories

    # Add additional notices
    additional_notices = []
    if result.get("additional_notice_0"):
        additional_notices.append(result["additional_notice_0"])
    if result.get("additional_notice_1"):
        additional_notices.append(result["additional_notice_1"])
    filtered_result["additional_notices"] = additional_notices

    # Add description
    description = {}
    if result.get("description_en"):
        description["en"] = result["description_en"]
    filtered_result["description"] = description

    # Add links
    links = {}
    if result.get("link_homepage_0") or result.get("link_homepage_1"):
        links["homepage"] = []
        if result.get("link_homepage_0"):
            links["homepage"].append(result["link_homepage_0"])
        if result.get("link_homepage_1"):
            links["homepage"].append(result["link_homepage_1"])
    if result.get("link_blockchain_site_0") or result.get("link_blockchain_site_1"):
        links["blockchain_site"] = []
        if result.get("link_blockchain_site_0"):
            links["blockchain_site"].append(result["link_blockchain_site_0"])
        if result.get("link_blockchain_site_1"):
            links["blockchain_site"].append(result["link_blockchain_site_1"])
    if result.get("link_twitter"):
        links["twitter"] = result["link_twitter"]
    filtered_result["links"] = links

    # Add images
    image = {}
    if result.get("image_thumb"):
        image["thumb"] = result["image_thumb"]
    if result.get("image_small"):
        image["small"] = result["image_small"]
    if result.get("image_large"):
        image["large"] = result["image_large"]
    filtered_result["image"] = image

    # Add market data
    if market_data:
        market_data_dict = {}
        if result.get("market_data_current_price_usd") is not None:
            market_data_dict["current_price"] = {"usd": result["market_data_current_price_usd"]}
            if result.get("market_data_current_price_btc") is not None:
                market_data_dict["current_price"]["btc"] = result["market_data_current_price_btc"]
        if result.get("market_data_market_cap_usd") is not None:
            market_data_dict["market_cap"] = {"usd": result["market_data_market_cap_usd"]}
        if result.get("market_data_total_volume_usd") is not None:
            market_data_dict["total_volume"] = {"usd": result["market_data_total_volume_usd"]}
        if result.get("market_data_circulating_supply") is not None:
            market_data_dict["circulating_supply"] = result["market_data_circulating_supply"]
        if result.get("market_data_total_supply") is not None:
            market_data_dict["total_supply"] = result["market_data_total_supply"]
        filtered_result["market_data"] = market_data_dict

    # Add community data
    if community_data:
        community_data_dict = {}
        if result.get("community_data_reddit_subscribers") is not None:
            community_data_dict["reddit_subscribers"] = result["community_data_reddit_subscribers"]
        if result.get("community_data_twitter_followers") is not None:
            community_data_dict["twitter_followers"] = result["community_data_twitter_followers"]
        if result.get("community_data_facebook_likes") is not None:
            community_data_dict["facebook_likes"] = result["community_data_facebook_likes"]
        filtered_result["community_data"] = community_data_dict

    # Add developer data
    if developer_data:
        developer_data_dict = {}
        if result.get("developer_data_github_stars") is not None:
            developer_data_dict["github_stars"] = result["developer_data_github_stars"]
        if result.get("developer_data_github_forks") is not None:
            developer_data_dict["github_forks"] = result["developer_data_github_forks"]
        if result.get("developer_data_commits_last_4_weeks") is not None:
            developer_data_dict["commits_last_4_weeks"] = result["developer_data_commits_last_4_weeks"]
        filtered_result["developer_data"] = developer_data_dict

    # Add status updates
    status_updates = []
    if result.get("status_update_0_description"):
        status_updates.append({
            "description": result["status_update_0_description"],
            "category": result["status_update_0_category"]
        })
    if result.get("status_update_1_description"):
        status_updates.append({
            "description": result["status_update_1_description"],
            "category": result["status_update_1_category"]
        })
    filtered_result["status_updates"] = status_updates

    # Add tickers
    if tickers:
        tickers_list = []
        if result.get("ticker_0_base"):
            tickers_list.append({
                "base": result["ticker_0_base"],
                "target": result["ticker_0_target"],
                "market": {"name": result["ticker_0_market_name"]},
                "last_price": result["ticker_0_last_price"],
                "volume": result["ticker_0_volume"]
            })
        if result.get("ticker_1_base"):
            tickers_list.append({
                "base": result["ticker_1_base"],
                "target": result["ticker_1_target"],
                "market": {"name": result["ticker_1_market_name"]},
                "last_price": result["ticker_1_last_price"],
                "volume": result["ticker_1_volume"]
            })
        filtered_result["tickers"] = tickers_list

    # Add platform data
    platform = {}
    if result.get("platform_ethereum"):
        platform["ethereum"] = result["platform_ethereum"]
    if result.get("platform_bsc"):
        platform["binance_smart_chain"] = result["platform_bsc"]
    if result.get("detail_platform_ethereum_contract_address"):
        if "ethereum" not in platform:
            platform["ethereum"] = result["detail_platform_ethereum_contract_address"]
    if result.get("detail_platform_bsc_contract_address"):
        if "binance_smart_chain" not in platform:
            platform["binance_smart_chain"] = result["detail_platform_bsc_contract_address"]
    filtered_result["platform"] = platform

    # Add localization
    if localization:
        localization_dict = {}
        if result.get("localization_en"):
            localization_dict["en"] = result["localization_en"]
        if result.get("localization_zh"):
            localization_dict["zh"] = result["localization_zh"]
        filtered_result["localization"] = localization_dict

    # Add sentiment data
    sentiment_data = {}
    if result.get("sentiment_votes_up_percentage") is not None:
        sentiment_data["up_percentage"] = result["sentiment_votes_up_percentage"]
    if result.get("sentiment_votes_down_percentage") is not None:
        sentiment_data["down_percentage"] = result["sentiment_votes_down_percentage"]
    if sentiment_data:
        filtered_result["sentiment_data"] = sentiment_data

    # Add watchlist data
    if result.get("watchlist_portfolio_users") is not None:
        filtered_result["watchlist_portfolio_users"] = result["watchlist_portfolio_users"]

    # Add sparkline data if requested
    if sparkline:
        filtered_result["sparkline_in_7d"] = {
            "price": [40000, 41000, 42000, 43000, 44000, 45000, 46000]
        }

    return filtered_result