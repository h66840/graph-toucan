from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching news data from external Yahoo Finance API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - news_0_title (str): Title of the first news article
        - news_0_summary (str): Summary of the first news article
        - news_0_description (str): Description of the first news article
        - news_0_url (str): URL of the first news article
        - news_1_title (str): Title of the second news article
        - news_1_summary (str): Summary of the second news article
        - news_1_description (str): Description of the second news article
        - news_1_url (str): URL of the second news article
    """
    return {
        "news_0_title": "Apple Reports Record Q4 Earnings",
        "news_0_summary": "Apple Inc. announces strong quarterly results driven by iPhone sales.",
        "news_0_description": "Apple has reported better-than-expected earnings for Q4, with revenue up 12% year-over-year. The growth was primarily fueled by strong demand for the latest iPhone models and services segment expansion.",
        "news_0_url": "https://finance.yahoo.com/news/apple-q4-earnings-report-2023",
        "news_1_title": "Apple Unveils New Campus Expansion Plans",
        "news_1_summary": "Apple plans to expand its Cupertino headquarters with new sustainable buildings.",
        "news_1_description": "The tech giant revealed plans to expand its Apple Park campus with two new energy-efficient buildings focused on research and development, emphasizing its commitment to sustainability.",
        "news_1_url": "https://finance.yahoo.com/news/apple-campus-expansion-2023"
    }

def yahoo_finance_server_get_yahoo_finance_news(ticker: str) -> Dict[str, Any]:
    """
    Get news for a given ticker symbol from Yahoo Finance.
    
    Args:
        ticker (str): The ticker symbol of the stock to get news for, e.g. "AAPL"
    
    Returns:
        Dict containing a list of news articles, each with 'title', 'summary', 'description', and 'url' fields.
    
    Raises:
        ValueError: If ticker is empty or not a string
    """
    if not isinstance(ticker, str):
        raise ValueError("Ticker must be a string")
    if not ticker.strip():
        raise ValueError("Ticker cannot be empty")
    
    # Fetch simulated external data
    api_data = call_external_api("yahoo-finance-server-get_yahoo_finance_news")
    
    # Construct news list from flattened API response
    news = [
        {
            "title": api_data["news_0_title"],
            "summary": api_data["news_0_summary"],
            "description": api_data["news_0_description"],
            "url": api_data["news_0_url"]
        },
        {
            "title": api_data["news_1_title"],
            "summary": api_data["news_1_summary"],
            "description": api_data["news_1_description"],
            "url": api_data["news_1_url"]
        }
    ]
    
    return {"news": news}