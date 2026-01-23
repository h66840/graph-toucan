from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching news data from external API for a given ticker.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - news_0_date (str): Date of the first news article
        - news_0_title (str): Title of the first news article
        - news_0_publisher (str): Publisher of the first news article
        - news_0_link (str): URL link of the first news article
        - news_0_summary (str): Summary of the first news article
        - news_1_date (str): Date of the second news article
        - news_1_title (str): Title of the second news article
        - news_1_publisher (str): Publisher of the second news article
        - news_1_link (str): URL link of the second news article
        - news_1_summary (str): Summary of the second news article
    """
    return {
        "news_0_date": "2023-10-05",
        "news_0_title": "Tech Giant Reports Strong Quarterly Earnings",
        "news_0_publisher": "Financial Times",
        "news_0_link": "https://example.com/news1",
        "news_0_summary": "The company exceeded revenue expectations driven by cloud growth.",
        
        "news_1_date": "2023-10-04",
        "news_1_title": "New Product Launch Boosts Stock",
        "news_1_publisher": "Bloomberg",
        "news_1_link": "https://example.com/news2",
        "news_1_summary": "Innovation in AI chips leads to investor optimism."
    }

def finance_mcp_server_get_news(ticker: str, count: Optional[int] = None) -> Dict[str, Any]:
    """
    Get the news of a stock or cryptocurrency ticker.
    
    Args:
        ticker (str): The stock or crypto ticker symbol (e.g., AAPL, BTC-USD). Required.
        count (Optional[int]): The number of news articles to retrieve. If not provided, defaults to 2.
    
    Returns:
        Dict containing a list of news articles with keys:
        - news_articles (List[Dict]): List of news articles, each containing 'date', 'title', 
          'publisher', 'link', and 'summary' fields.
    
    Raises:
        ValueError: If ticker is empty or None.
    """
    if not ticker:
        raise ValueError("ticker is required and cannot be empty")
    
    # Default count to 2 if not specified
    if count is None:
        count = 2
    elif count <= 0:
        return {"news_articles": []}
    
    # Fetch simulated external data
    api_data = call_external_api("finance-mcp-server-get_news")
    
    news_articles: List[Dict[str, str]] = []
    
    # Extract up to `count` articles (currently supporting max 2 from API simulation)
    for i in range(min(count, 2)):
        article = {
            "date": api_data.get(f"news_{i}_date", ""),
            "title": api_data.get(f"news_{i}_title", ""),
            "publisher": api_data.get(f"news_{i}_publisher", ""),
            "link": api_data.get(f"news_{i}_link", ""),
            "summary": api_data.get(f"news_{i}_summary", "")
        }
        news_articles.append(article)
    
    return {"news_articles": news_articles}