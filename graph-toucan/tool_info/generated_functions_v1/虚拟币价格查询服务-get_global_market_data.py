from typing import Dict, Any
from datetime import datetime, timedelta
import random

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching global cryptocurrency market data from an external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - active_cryptocurrencies (int): Number of active cryptocurrencies
        - active_exchanges (str): Number of active exchanges, or "N/A"
        - total_market_cap_usd (str): Total market cap in USD with formatting
        - total_market_cap_cny (str): Total market cap in CNY with formatting
        - total_volume_24h_usd (str): 24h trading volume in USD with formatting
        - bitcoin_dominance (str): Bitcoin's market cap share as percentage string
        - ethereum_dominance (str): Ethereum's market cap share as percentage string
        - market_change_24h (str): 24h market change with arrow emoji and percentage
        - last_updated (str): Timestamp of data update in "YYYY-MM-DD HH:MM:SS"
    """
    # Generate realistic mock data
    btc_dominance = round(random.uniform(50.0, 60.0), 2)
    eth_dominance = round(random.uniform(10.0, 18.0), 2)
    market_change = round(random.uniform(-5.0, 5.0), 2)
    
    # Determine arrow based on market change
    arrow = "📈" if market_change >= 0 else "📉"
    market_change_str = f"{arrow} {abs(market_change):.2f}%"
    
    # Format large numbers with commas and currency symbols
    total_cap_usd = int(random.uniform(1.8e12, 2.5e12))
    total_cap_cny = int(total_cap_usd * 7.2)
    volume_usd = int(random.uniform(8e10, 1.5e11))
    
    total_market_cap_usd = f"${total_cap_usd:,.0f}"
    total_market_cap_cny = f"¥{total_cap_cny:,.0f}"
    total_volume_24h_usd = f"${volume_usd:,.0f}"
    
    # Random timestamp within last 10 minutes
    now = datetime.now() - timedelta(minutes=random.randint(0, 10), seconds=random.randint(0, 59))
    last_updated = now.strftime("%Y-%m-%d %H:%M:%S")
    
    return {
        "active_cryptocurrencies": random.randint(10000, 25000),
        "active_exchanges": str(random.randint(45, 60)) if random.random() > 0.1 else "N/A",
        "total_market_cap_usd": total_market_cap_usd,
        "total_market_cap_cny": total_market_cap_cny,
        "total_volume_24h_usd": total_volume_24h_usd,
        "bitcoin_dominance": f"{btc_dominance}%",
        "ethereum_dominance": f"{eth_dominance}%",
        "market_change_24h": market_change_str,
        "last_updated": last_updated
    }

def 虚拟币价格查询服务_get_global_market_data() -> Dict[str, Any]:
    """
    获取全球加密货币市场数据
    
    Returns:
        Dict containing global cryptocurrency market data with the following fields:
        - active_cryptocurrencies (int): number of active cryptocurrencies in the market
        - active_exchanges (str): number of active exchanges; "N/A" if not available
        - total_market_cap_usd (str): total market capitalization in USD, formatted with dollar sign and commas
        - total_market_cap_cny (str): total market capitalization in CNY, formatted with yuan sign and commas
        - total_volume_24h_usd (str): 24-hour total trading volume in USD, formatted with dollar sign and commas
        - bitcoin_dominance (str): percentage of Bitcoin's market cap share, e.g., "58.45%"
        - ethereum_dominance (str): percentage of Ethereum's market cap share, e.g., "12.64%"
        - market_change_24h (str): 24-hour change in total market value, including arrow emoji and percentage
        - last_updated (str): timestamp of data update in "YYYY-MM-DD HH:MM:SS" format
    
    Raises:
        Exception: If there is an error fetching or processing the market data
    """
    try:
        # Fetch data from simulated external API
        api_data = call_external_api("虚拟币价格查询服务_get_global_market_data")
        
        # Construct result dictionary matching the required output schema
        result = {
            "active_cryptocurrencies": api_data["active_cryptocurrencies"],
            "active_exchanges": api_data["active_exchanges"],
            "total_market_cap_usd": api_data["total_market_cap_usd"],
            "total_market_cap_cny": api_data["total_market_cap_cny"],
            "total_volume_24h_usd": api_data["total_volume_24h_usd"],
            "bitcoin_dominance": api_data["bitcoin_dominance"],
            "ethereum_dominance": api_data["ethereum_dominance"],
            "market_change_24h": api_data["market_change_24h"],
            "last_updated": api_data["last_updated"]
        }
        
        return result
        
    except Exception as e:
        # In a real implementation, we might log the error here
        raise Exception(f"Failed to retrieve global market data: {str(e)}")