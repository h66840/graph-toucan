from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for crypto research server.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - project_name (str): Name of the crypto project
        - twitter_username (str): Twitter handle associated with the project
        - description (str): Short description of the project's purpose and functionality
        - launch_date (str): Official launch date in ISO 8601 format (YYYY-MM-DD)
        - primary_chain (str): Main blockchain platform the project operates on
        - website_url (str): Official website URL for the project
        - whitepaper_url (str): URL to the project’s whitepaper or technical documentation
        - token_symbol (str): Cryptocurrency token symbol
        - category (str): Primary category of the project
        - status (str): Current operational status
        - team_size (int): Number of core team members
        - funding_round_0_round (str): First funding round type
        - funding_round_0_amount_usd (float): First funding amount in USD
        - funding_round_0_date (str): First funding round date (YYYY-MM-DD)
        - funding_round_0_investors (str): Comma-separated list of investors for first round
        - funding_round_1_round (str): Second funding round type
        - funding_round_1_amount_usd (float): Second funding amount in USD
        - funding_round_1_date (str): Second funding round date (YYYY-MM-DD)
        - funding_round_1_investors (str): Comma-separated list of investors for second round
        - partnership_0_partner_name (str): First partner name
        - partnership_0_announced_date (str): First partnership announced date (YYYY-MM-DD)
        - partnership_0_details (str): Details about first partnership
        - partnership_1_partner_name (str): Second partner name
        - partnership_1_announced_date (str): Second partnership announced date (YYYY-MM-DD)
        - partnership_1_details (str): Details about second partnership
        - social_links_discord (str): Discord server URL
        - social_links_telegram (str): Telegram group URL
        - social_links_github (str): GitHub repository URL
        - social_links_linkedin (str): LinkedIn company page URL
        - onchain_metrics_holders_count (int): Number of token holders
        - onchain_metrics_24h_volume_usd (float): 24-hour trading volume in USD
        - onchain_metrics_market_cap_usd (float): Market capitalization in USD
        - onchain_metrics_circulating_supply (int): Circulating supply of token
        - recent_update_0_title (str): Title of first recent update
        - recent_update_0_date (str): Date of first recent update (YYYY-MM-DD)
        - recent_update_0_summary (str): Summary of first recent update
        - recent_update_1_title (str): Title of second recent update
        - recent_update_1_date (str): Date of second recent update (YYYY-MM-DD)
        - recent_update_1_summary (str): Summary of second recent update
        - research_report_0_report_title (str): Title of first research report
        - research_report_0_publish_date (str): Publish date of first report (YYYY-MM-DD)
        - research_report_0_summary (str): Summary of first research report
        - research_report_0_url (str): URL to first research report
        - research_report_1_report_title (str): Title of second research report
        - research_report_1_publish_date (str): Publish date of second report (YYYY-MM-DD)
        - research_report_1_summary (str): Summary of second research report
        - research_report_1_url (str): URL to second research report
    """
    return {
        "project_name": "CryptoShield",
        "twitter_username": "CryptoShieldDAO",
        "description": "A decentralized insurance protocol protecting DeFi users from smart contract risks.",
        "launch_date": "2022-03-15",
        "primary_chain": "Ethereum",
        "website_url": "https://cryptoshield.io",
        "whitepaper_url": "https://cryptoshield.io/whitepaper.pdf",
        "token_symbol": "SHLD",
        "category": "DeFi",
        "status": "Active",
        "team_size": 12,
        "funding_round_0_round": "Seed",
        "funding_round_0_amount_usd": 2500000.0,
        "funding_round_0_date": "2021-08-10",
        "funding_round_0_investors": "a16z, Pantera Capital",
        "funding_round_1_round": "Series A",
        "funding_round_1_amount_usd": 7500000.0,
        "funding_round_1_date": "2022-01-20",
        "funding_round_1_investors": "Paradigm, Multicoin Capital",
        "partnership_0_partner_name": "Chainlink",
        "partnership_0_announced_date": "2022-05-14",
        "partnership_0_details": "Integration of Chainlink oracles for risk assessment",
        "partnership_1_partner_name": "Aave",
        "partnership_1_announced_date": "2022-07-23",
        "partnership_1_details": "Joint liquidity protection module development",
        "social_links_discord": "https://discord.gg/cryptoshield",
        "social_links_telegram": "https://t.me/cryptoshield_announcements",
        "social_links_github": "https://github.com/cryptoshield",
        "social_links_linkedin": "https://linkedin.com/company/cryptoshield",
        "onchain_metrics_holders_count": 48291,
        "onchain_metrics_24h_volume_usd": 3245000.0,
        "onchain_metrics_market_cap_usd": 187650000.0,
        "onchain_metrics_circulating_supply": 93825000,
        "recent_update_0_title": "V2 Protocol Upgrade",
        "recent_update_0_date": "2023-09-05",
        "recent_update_0_summary": "Launched new staking mechanism and improved claims process.",
        "recent_update_1_title": "New Coverage Options",
        "recent_update_1_date": "2023-10-18",
        "recent_update_1_summary": "Added coverage for cross-chain bridges and L2 solutions.",
        "research_report_0_report_title": "DeFi Insurance Landscape 2023",
        "research_report_0_publish_date": "2023-06-12",
        "research_report_0_summary": "Comprehensive analysis of DeFi insurance protocols and risk models.",
        "research_report_0_url": "https://research.example.com/defi-insurance-2023",
        "research_report_1_report_title": "Smart Contract Risk Assessment Framework",
        "research_report_1_publish_date": "2023-08-21",
        "research_report_1_summary": "Evaluation methodology for protocol security and vulnerability scoring.",
        "research_report_1_url": "https://research.example.com/sc-risk-framework"
    }

def crypto_research_server_research_get_project_by_twitter(username: str) -> Dict[str, Any]:
    """
    Get project details by Twitter username from the Research knowledge base.

    Args:
        username (str): Twitter username of the project (required)

    Returns:
        Dict containing detailed information about the crypto project including:
        - project_name (str)
        - twitter_username (str)
        - description (str)
        - launch_date (str): ISO 8601 format (YYYY-MM-DD)
        - primary_chain (str)
        - website_url (str)
        - whitepaper_url (str)
        - token_symbol (str)
        - category (str)
        - status (str)
        - team_size (int)
        - funding_rounds (List[Dict]): Each with 'round', 'amount_usd', 'date', 'investors'
        - partnerships (List[Dict]): Each with 'partner_name', 'announced_date', 'details'
        - social_links (Dict): With 'discord', 'telegram', 'github', 'linkedin'
        - onchain_metrics (Dict): With 'holders_count', '24h_volume_usd', 'market_cap_usd', 'circulating_supply'
        - recent_updates (List[Dict]): Each with 'title', 'date', 'summary'
        - research_reports (List[Dict]): Each with 'report_title', 'publish_date', 'summary', 'url'

    Raises:
        ValueError: If username is empty or None
    """
    if not username:
        raise ValueError("username is required")

    # Fetch simulated external data
    api_data = call_external_api("crypto-research-server-research_get_project_by_twitter")

    # Construct funding_rounds list
    funding_rounds = [
        {
            "round": api_data["funding_round_0_round"],
            "amount_usd": api_data["funding_round_0_amount_usd"],
            "date": api_data["funding_round_0_date"],
            "investors": api_data["funding_round_0_investors"]
        },
        {
            "round": api_data["funding_round_1_round"],
            "amount_usd": api_data["funding_round_1_amount_usd"],
            "date": api_data["funding_round_1_date"],
            "investors": api_data["funding_round_1_investors"]
        }
    ]

    # Construct partnerships list
    partnerships = [
        {
            "partner_name": api_data["partnership_0_partner_name"],
            "announced_date": api_data["partnership_0_announced_date"],
            "details": api_data["partnership_0_details"]
        },
        {
            "partner_name": api_data["partnership_1_partner_name"],
            "announced_date": api_data["partnership_1_announced_date"],
            "details": api_data["partnership_1_details"]
        }
    ]

    # Construct social_links dict
    social_links = {
        "discord": api_data["social_links_discord"],
        "telegram": api_data["social_links_telegram"],
        "github": api_data["social_links_github"],
        "linkedin": api_data["social_links_linkedin"]
    }

    # Construct onchain_metrics dict
    onchain_metrics = {
        "holders_count": api_data["onchain_metrics_holders_count"],
        "24h_volume_usd": api_data["onchain_metrics_24h_volume_usd"],
        "market_cap_usd": api_data["onchain_metrics_market_cap_usd"],
        "circulating_supply": api_data["onchain_metrics_circulating_supply"]
    }

    # Construct recent_updates list
    recent_updates = [
        {
            "title": api_data["recent_update_0_title"],
            "date": api_data["recent_update_0_date"],
            "summary": api_data["recent_update_0_summary"]
        },
        {
            "title": api_data["recent_update_1_title"],
            "date": api_data["recent_update_1_date"],
            "summary": api_data["recent_update_1_summary"]
        }
    ]

    # Construct research_reports list
    research_reports = [
        {
            "report_title": api_data["research_report_0_report_title"],
            "publish_date": api_data["research_report_0_publish_date"],
            "summary": api_data["research_report_0_summary"],
            "url": api_data["research_report_0_url"]
        },
        {
            "report_title": api_data["research_report_1_report_title"],
            "publish_date": api_data["research_report_1_publish_date"],
            "summary": api_data["research_report_1_summary"],
            "url": api_data["research_report_1_url"]
        }
    ]

    # Return structured data
    return {
        "project_name": api_data["project_name"],
        "twitter_username": api_data["twitter_username"],
        "description": api_data["description"],
        "launch_date": api_data["launch_date"],
        "primary_chain": api_data["primary_chain"],
        "website_url": api_data["website_url"],
        "whitepaper_url": api_data["whitepaper_url"],
        "token_symbol": api_data["token_symbol"],
        "category": api_data["category"],
        "status": api_data["status"],
        "team_size": api_data["team_size"],
        "funding_rounds": funding_rounds,
        "partnerships": partnerships,
        "social_links": social_links,
        "onchain_metrics": onchain_metrics,
        "recent_updates": recent_updates,
        "research_reports": research_reports
    }