from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for The Verge weekly news.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - news_article_0_title (str): Title of the first news article
        - news_article_0_link (str): URL link of the first news article
        - news_article_0_summary (str): Summary of the first news article
        - news_article_1_title (str): Title of the second news article
        - news_article_1_link (str): URL link of the second news article
        - news_article_1_summary (str): Summary of the second news article
    """
    return {
        "news_article_0_title": "Apple Unveils New MacBook Pro with M3 Chip",
        "news_article_0_link": "https://www.theverge.com/2023/10/30/macbook-pro-m3-launch",
        "news_article_0_summary": "Apple has announced a new lineup of MacBook Pro laptops powered by the M3 series chips, featuring improved performance and battery life.",
        "news_article_1_title": "Tesla Releases Full Self-Driving Beta to All US Customers",
        "news_article_1_link": "https://www.theverge.com/2023/10/29/tesla-fsd-beta-public-release",
        "news_article_1_summary": "Tesla is expanding its Full Self-Driving beta program to all owners in the United States, marking a significant step toward autonomous driving."
    }

def the_verge_news_server_get_weekly_news() -> Dict[str, Any]:
    """
    Get the latest news from The Verge for the past week.

    Returns:
        Dict containing a list of news articles, each with 'title', 'link', and 'summary' fields.
    
    Example:
        {
            "news_articles": [
                {
                    "title": "Apple Unveils New MacBook Pro with M3 Chip",
                    "link": "https://www.theverge.com/2023/10/30/macbook-pro-m3-launch",
                    "summary": "Apple has announced a new lineup of MacBook Pro laptops powered by the M3 series chips, featuring improved performance and battery life."
                },
                {
                    "title": "Tesla Releases Full Self-Driving Beta to All US Customers",
                    "link": "https://www.theverge.com/2023/10/29/tesla-fsd-beta-public-release",
                    "summary": "Tesla is expanding its Full Self-Driving beta program to all owners in the United States, marking a significant step toward autonomous driving."
                }
            ]
        }
    """
    try:
        api_data = call_external_api("the-verge-news-server-get-weekly-news")
        
        news_articles: List[Dict[str, str]] = [
            {
                "title": api_data["news_article_0_title"],
                "link": api_data["news_article_0_link"],
                "summary": api_data["news_article_0_summary"]
            },
            {
                "title": api_data["news_article_1_title"],
                "link": api_data["news_article_1_link"],
                "summary": api_data["news_article_1_summary"]
            }
        ]
        
        return {
            "news_articles": news_articles
        }
    except KeyError as e:
        raise KeyError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while fetching or processing news data: {e}")