from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google News and Trends.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first news article
        - result_0_source (str): Source of the first news article
        - result_0_published_at (str): Publication timestamp of the first article in ISO format
        - result_0_url (str): URL of the first news article
        - result_0_summary (str): Summary of the first news article
        - result_1_title (str): Title of the second news article
        - result_1_source (str): Source of the second news article
        - result_1_published_at (str): Publication timestamp of the second article in ISO format
        - result_1_url (str): URL of the second news article
        - result_1_summary (str): Summary of the second news article
        - error (str): Error message if any occurred, otherwise empty string
    """
    now = datetime.utcnow()
    return {
        "result_0_title": "Breakthrough in Renewable Energy Technology",
        "result_0_source": "Tech Times",
        "result_0_published_at": (now - timedelta(hours=12)).isoformat(),
        "result_0_url": "https://example.com/renewable-energy-breakthrough",
        "result_0_summary": "Scientists have developed a new solar panel that is twice as efficient as current models.",
        "result_1_title": "Global Climate Summit Reaches Historic Agreement",
        "result_1_source": "World News Network",
        "result_1_published_at": (now - timedelta(hours=18)).isoformat(),
        "result_1_url": "https://example.com/climate-summit-agreement",
        "result_1_summary": "Over 100 countries agreed on stricter emissions targets to combat climate change.",
        "error": ""
    }


def google_news_and_trends_get_news_by_topic(
    topic: str,
    full_data: Optional[bool] = None,
    max_results: Optional[int] = None,
    period: Optional[int] = None,
    summarize: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Find articles by topic using Google News.

    Args:
        topic (str): Topic to search for articles. Must be one of the predefined topics.
        full_data (bool, optional): Return full data for each article. If False, a summary is created.
        max_results (int, optional): Maximum number of results to return. Defaults to 2.
        period (int, optional): Number of days to look back for articles.
        summarize (bool, optional): Generate a summary of the article using LLM or NLP.

    Returns:
        Dict containing:
            - results (List[Dict]): List of news articles with 'title', 'source', 'published_at', 'url', and 'summary'.
            - error (str): Error message if the request failed, otherwise empty string.

    Raises:
        ValueError: If the topic is not in the allowed list of topics.
    """
    allowed_topics = {
        "WORLD", "NATION", "BUSINESS", "TECHNOLOGY", "ENTERTAINMENT", "SPORTS", "SCIENCE", "HEALTH",
        "POLITICS", "CELEBRITIES", "TV", "MUSIC", "MOVIES", "THEATER", "SOCCER", "CYCLING", "MOTOR SPORTS",
        "TENNIS", "COMBAT SPORTS", "BASKETBALL", "BASEBALL", "FOOTBALL", "SPORTS BETTING", "WATER SPORTS",
        "HOCKEY", "GOLF", "CRICKET", "RUGBY", "ECONOMY", "PERSONAL FINANCE", "FINANCE", "DIGITAL CURRENCIES",
        "MOBILE", "ENERGY", "GAMING", "INTERNET SECURITY", "GADGETS", "VIRTUAL REALITY", "ROBOTICS", "NUTRITION",
        "PUBLIC HEALTH", "MENTAL HEALTH", "MEDICINE", "SPACE", "WILDLIFE", "ENVIRONMENT", "NEUROSCIENCE", "PHYSICS",
        "GEOLOGY", "PALEONTOLOGY", "SOCIAL SCIENCES", "EDUCATION", "JOBS", "ONLINE EDUCATION", "HIGHER EDUCATION",
        "VEHICLES", "ARTS-DESIGN", "BEAUTY", "FOOD", "TRAVEL", "SHOPPING", "HOME", "OUTDOORS", "FASHION"
    }

    if topic.upper() not in allowed_topics:
        return {
            "results": [],
            "error": f"Invalid topic: {topic}. Must be one of {sorted(allowed_topics)}"
        }

    try:
        # Set defaults
        max_results = max_results or 2
        if max_results < 1:
            max_results = 1
        elif max_results > 10:
            max_results = 10  # Cap max results

        # Call external API (simulated)
        api_data = call_external_api("google-news-and-trends-get_news_by_topic")

        # Check for error from API
        if api_data.get("error"):
            return {
                "results": [],
                "error": api_data["error"]
            }

        # Construct results list from flattened API response
        results = []
        for i in range(min(max_results, 2)):  # We only have 2 simulated results
            title_key = f"result_{i}_title"
            source_key = f"result_{i}_source"
            published_at_key = f"result_{i}_published_at"
            url_key = f"result_{i}_url"
            summary_key = f"result_{i}_summary"

            if title_key not in api_data:
                continue

            article = {
                "title": api_data[title_key],
                "source": api_data[source_key],
                "published_at": api_data[published_at_key],
                "url": api_data[url_key],
                "summary": api_data[summary_key]
            }
            results.append(article)

        return {
            "results": results,
            "error": ""
        }

    except Exception as e:
        return {
            "results": [],
            "error": f"Failed to retrieve news articles: {str(e)}"
        }