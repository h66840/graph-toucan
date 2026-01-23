from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for The Verge daily news.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - article_0_title (str): Title of the first news article
        - article_0_link (str): URL link of the first news article
        - article_0_summary (str): Summary of the first news article
        - article_1_title (str): Title of the second news article
        - article_1_link (str): URL link of the second news article
        - article_1_summary (str): Summary of the second news article
    """
    return {
        "article_0_title": "Apple Unveils New iPhone with Advanced AI Features",
        "article_0_link": "https://www.theverge.com/2023/4/5/apple-iphone-ai-features",
        "article_0_summary": "Apple has announced a new generation of iPhone featuring advanced artificial intelligence capabilities, including real-time language translation and enhanced photo editing powered by on-device machine learning.",
        "article_1_title": "Tesla Launches Fully Autonomous Driving Update",
        "article_1_link": "https://www.theverge.com/2023/4/5/tesla-autonomous-driving-update",
        "article_1_summary": "Tesla rolls out its most ambitious software update yet, enabling full self-driving capabilities across its vehicle lineup, pending regulatory approval in several key markets."
    }

def the_verge_news_server_get_daily_news() -> Dict[str, Any]:
    """
    Get the latest news from The Verge for today.

    Returns:
        Dict containing a list of news articles, each with 'title', 'link', and 'summary' fields.
        - articles (List[Dict]): List of article dictionaries with string fields 'title', 'link', and 'summary'

    Example:
        {
            "articles": [
                {
                    "title": "Apple Unveils New iPhone with Advanced AI Features",
                    "link": "https://www.theverge.com/2023/4/5/apple-iphone-ai-features",
                    "summary": "Apple has announced..."
                },
                {
                    "title": "Tesla Launches Fully Autonomous Driving Update",
                    "link": "https://www.theverge.com/2023/4/5/tesla-autonomous-driving-update",
                    "summary": "Tesla rolls out..."
                }
            ]
        }

    Raises:
        KeyError: If expected fields are missing from the API response
        Exception: For any other processing errors
    """
    try:
        api_data = call_external_api("the-verge-news-server-get-daily-news")

        articles = [
            {
                "title": api_data["article_0_title"],
                "link": api_data["article_0_link"],
                "summary": api_data["article_0_summary"]
            },
            {
                "title": api_data["article_1_title"],
                "link": api_data["article_1_link"],
                "summary": api_data["article_1_summary"]
            }
        ]

        result = {
            "articles": articles
        }

        return result

    except KeyError as e:
        raise KeyError(f"Missing expected data field: {str(e)}") from e
    except Exception as e:
        raise Exception(f"Failed to process news data: {str(e)}") from e