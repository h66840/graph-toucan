from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching stock news data from external API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - news_0_keyword (str): Keyword for the first news item
        - news_0_title (str): Title of the first news item
        - news_0_content (str): Content of the first news item
        - news_0_publish_time (str): Publish time of the first news item
        - news_0_source (str): Source of the first news item
        - news_0_url (str): URL of the first news item
        - news_1_keyword (str): Keyword for the second news item
        - news_1_title (str): Title of the second news item
        - news_1_content (str): Content of the second news item
        - news_1_publish_time (str): Publish time of the second news item
        - news_1_source (str): Source of the second news item
        - news_1_url (str): URL of the second news item
    """
    return {
        "news_0_keyword": "earnings",
        "news_0_title": "Company A Reports Strong Q3 Earnings",
        "news_0_content": "Company A has announced better than expected quarterly results with revenue growth of 15% year over year.",
        "news_0_publish_time": "2023-10-15 09:30:00",
        "news_0_source": "Financial News Network",
        "news_0_url": "https://example.com/news/1",
        "news_1_keyword": "expansion",
        "news_1_title": "Company A Announces New Factory in Asia",
        "news_1_content": "The company plans to invest $200 million in a new manufacturing facility to meet growing demand.",
        "news_1_publish_time": "2023-10-14 14:20:00",
        "news_1_source": "Business Daily",
        "news_1_url": "https://example.com/news/2"
    }

def akshare_one_mcp_server_get_news_data(symbol: str, recent_n: Optional[int] = None) -> Dict[str, Any]:
    """
    Get stock-related news data for a given symbol.
    
    Args:
        symbol (str): Stock symbol/ticker (e.g. '000001')
        recent_n (Optional[int]): Number of most recent records to return. If None, returns default number (2).
    
    Returns:
        Dict containing a list of news items, each with keyword, title, content, publish_time, source, and url.
    
    Raises:
        ValueError: If symbol is empty or None
    """
    if not symbol:
        raise ValueError("Symbol must be provided and cannot be empty")
    
    # Fetch data from simulated external API
    api_data = call_external_api("akshare-one-mcp-server-get_news_data")
    
    # Construct news list from flattened API response
    news_list = [
        {
            "keyword": api_data["news_0_keyword"],
            "title": api_data["news_0_title"],
            "content": api_data["news_0_content"],
            "publish_time": api_data["news_0_publish_time"],
            "source": api_data["news_0_source"],
            "url": api_data["news_0_url"]
        },
        {
            "keyword": api_data["news_1_keyword"],
            "title": api_data["news_1_title"],
            "content": api_data["news_1_content"],
            "publish_time": api_data["news_1_publish_time"],
            "source": api_data["news_1_source"],
            "url": api_data["news_1_url"]
        }
    ]
    
    # Apply recent_n limit if specified
    if recent_n is not None and recent_n > 0:
        news_list = news_list[:recent_n]
    
    return {"news_list": news_list}