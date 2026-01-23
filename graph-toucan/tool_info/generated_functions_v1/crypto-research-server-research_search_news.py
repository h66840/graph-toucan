from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for crypto research news search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first news article
        - result_0_content (str): Content of the first news article
        - result_0_category (str): Category of the first news article
        - result_0_source (str): Source of the first news article
        - result_0_publish_time (str): Publish time of the first news article (ISO format)
        - result_0_level (int): Level of the first news article (1-3)
        - result_0_url (str): URL of the first news article
        - result_1_title (str): Title of the second news article
        - result_1_content (str): Content of the second news article
        - result_1_category (str): Category of the second news article
        - result_1_source (str): Source of the second news article
        - result_1_publish_time (str): Publish time of the second news article (ISO format)
        - result_1_level (int): Level of the second news article (1-3)
        - result_1_url (str): URL of the second news article
        - total_count (int): Total number of matching news items found
        - error_message (str): Error message if request failed, empty string otherwise
        - status (str): Status of the request ('success' or 'error')
    """
    return {
        "result_0_title": "Bitcoin Reaches New All-Time High Amid Institutional Adoption",
        "result_0_content": "Bitcoin has surged past $100,000 as major financial institutions increase their exposure to cryptocurrency markets.",
        "result_0_category": "巨鲸动向",
        "result_0_source": "CryptoNewsDaily",
        "result_0_publish_time": "2023-11-15T14:30:00Z",
        "result_0_level": 3,
        "result_0_url": "https://example.com/news/bitcoin-atm-high",
        "result_1_title": "Ethereum Foundation Announces Major Upgrade for Q1 2024",
        "result_1_content": "The Ethereum development team revealed plans for a significant network upgrade aimed at improving scalability and reducing fees.",
        "result_1_category": "公链/L2",
        "result_1_source": "EthereumBlog",
        "result_1_publish_time": "2023-11-15T10:15:00Z",
        "result_1_level": 2,
        "result_1_url": "https://example.com/news/ethereum-upgrade",
        "total_count": 2,
        "error_message": "",
        "status": "success"
    }

def crypto_research_server_research_search_news(
    category: Optional[str] = None,
    day: Optional[str] = None,
    endDate: Optional[str] = None,
    keyword: Optional[str] = None,
    level: Optional[int] = 3,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
    source: Optional[str] = None,
    startDate: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for news on the Research knowledge base with specified filters.
    
    Args:
        category (Optional[str]): Category to search for news. Supported values: 
            ["Macro","巨鲸动向","相关项目","NFT & GameFi & SocialFi & DID & DAO & 内容创作",
             "交易所/钱包","公链/L2","投融资","监管","安全","AI相关","其他","工具","观点"]
        day (Optional[str]): Day of results (default today), format: YYYY-MM-DD
        endDate (Optional[str]): End date of results (default today), format: YYYY-MM-DD
        keyword (Optional[str]): Keyword to search for news
        level (Optional[int]): News level (default 3), 1: All, 2: Important, 3: Critical
        limit (Optional[int]): Limit of results (default 100, max 100)
        offset (Optional[int]): Offset of results (default 0)
        source (Optional[str]): Source to search for news
        startDate (Optional[str]): Start date of results (default today), format: YYYY-MM-DD
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of news articles with fields like 'title', 'content', 
          'category', 'source', 'publish_time', 'level', and 'url'
        - total_count (int): Total number of matching news items found
        - error_message (str): Error message if request failed
        - status (str): Status of the request ('success' or 'error')
    
    Raises:
        ValueError: If level is not in valid range (1-3) or limit exceeds 100
    """
    # Input validation
    if level is not None and (level < 1 or level > 3):
        return {
            "results": [],
            "total_count": 0,
            "error_message": "Invalid level value. Must be between 1 and 3.",
            "status": "error"
        }
    
    if limit and (limit < 1 or limit > 100):
        return {
            "results": [],
            "total_count": 0,
            "error_message": "Invalid limit value. Must be between 1 and 100.",
            "status": "error"
        }
    
    # Validate date formats if provided
    date_fields = [day, startDate, endDate]
    for date_str in [d for d in date_fields if d is not None]:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return {
                "results": [],
                "total_count": 0,
                "error_message": f"Invalid date format: {date_str}. Expected YYYY-MM-DD.",
                "status": "error"
            }
    
    # Call external API to get data
    api_data = call_external_api("crypto-research-server-research_search_news")
    
    # Construct results list from flattened API response
    results = []
    
    # Process first result if available
    if api_data.get("result_0_title"):
        results.append({
            "title": api_data["result_0_title"],
            "content": api_data["result_0_content"],
            "category": api_data["result_0_category"],
            "source": api_data["result_0_source"],
            "publish_time": api_data["result_0_publish_time"],
            "level": api_data["result_0_level"],
            "url": api_data["result_0_url"]
        })
    
    # Process second result if available
    if api_data.get("result_1_title"):
        results.append({
            "title": api_data["result_1_title"],
            "content": api_data["result_1_content"],
            "category": api_data["result_1_category"],
            "source": api_data["result_1_source"],
            "publish_time": api_data["result_1_publish_time"],
            "level": api_data["result_1_level"],
            "url": api_data["result_1_url"]
        })
    
    # Apply offset and limit manually
    start_idx = max(0, offset or 0)
    end_idx = start_idx + (limit or 100)
    paginated_results = results[start_idx:end_idx]
    
    # Return structured response matching output schema
    return {
        "results": paginated_results,
        "total_count": api_data["total_count"],
        "error_message": api_data["error_message"],
        "status": api_data["status"]
    }