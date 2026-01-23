from typing import Dict, List, Any, Optional
from datetime import datetime

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google News top stories.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - news_stories_0_title (str): Title of the first news story
        - news_stories_0_source (str): Source of the first news story
        - news_stories_0_published (str): ISO 8601 timestamp when the first story was published
        - news_stories_0_url (str): URL of the first news story
        - news_stories_0_summary (str): Summary of the first news story (if summarize enabled)
        - news_stories_0_relevance_score (float): Relevance score of the first story
        - news_stories_1_title (str): Title of the second news story
        - news_stories_1_source (str): Source of the second news story
        - news_stories_1_published (str): ISO 8601 timestamp when the second story was published
        - news_stories_1_url (str): URL of the second news story
        - news_stories_1_summary (str): Summary of the second news story (if summarize enabled)
        - news_stories_1_relevance_score (float): Relevance score of the second story
        - total_results (int): Total number of top news stories retrieved
        - time_period_days (int): Number of days in the period covered
        - fetched_at (str): ISO 8601 timestamp when the data was fetched
        - metadata_region (str): Region used for fetching news
        - metadata_language (str): Language used for fetching news
        - metadata_category (str): Category or feed type used
    """
    return {
        "news_stories_0_title": "Global Markets Surge on Economic Recovery Hopes",
        "news_stories_0_source": "Financial Times",
        "news_stories_0_published": "2023-10-05T08:30:00Z",
        "news_stories_0_url": "https://example.com/story1",
        "news_stories_0_summary": "Stock markets worldwide rose sharply as investors reacted positively to new economic data suggesting a rebound in consumer spending and manufacturing activity.",
        "news_stories_0_relevance_score": 0.95,
        "news_stories_1_title": "Climate Summit Reaches Historic Emissions Agreement",
        "news_stories_1_source": "BBC News",
        "news_stories_1_published": "2023-10-04T14:20:00Z",
        "news_stories_1_url": "https://example.com/story2",
        "news_stories_1_summary": "World leaders have agreed on a binding pact to reduce carbon emissions by 50% over the next decade, marking a major step in combating climate change.",
        "news_stories_1_relevance_score": 0.92,
        "total_results": 2,
        "time_period_days": 7,
        "fetched_at": "2023-10-05T10:00:00Z",
        "metadata_region": "US",
        "metadata_language": "en",
        "metadata_category": "top_stories"
    }

def google_news_and_trends_get_top_news(
    full_data: Optional[bool] = None,
    max_results: Optional[int] = None,
    period: Optional[int] = None,
    summarize: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get top news stories from Google News.

    Args:
        full_data (bool, optional): Return full data for each article. If False, a summary should be created.
        max_results (int, optional): Maximum number of results to return.
        period (int, optional): Number of days to look back for top articles.
        summarize (bool, optional): Generate a summary of the article using LLM or NLP.

    Returns:
        Dict containing:
        - news_stories (List[Dict]): List of news article objects with title, source, published timestamp, URL, summary, and relevance score
        - total_results (int): Total number of top news stories retrieved
        - time_period_days (int): Number of days in the period covered
        - fetched_at (str): ISO 8601 timestamp when data was fetched
        - metadata (Dict): Additional context such as region, language, or categorization
    """
    # Validate inputs
    if max_results is not None and (not isinstance(max_results, int) or max_results <= 0):
        raise ValueError("max_results must be a positive integer")
    if period is not None and (not isinstance(period, int) or period <= 0):
        raise ValueError("period must be a positive integer")

    # Call external API to get flattened data
    api_data = call_external_api("google-news-and-trends-get_top_news")

    # Construct news_stories list from indexed fields
    news_stories = [
        {
            "title": api_data["news_stories_0_title"],
            "source": api_data["news_stories_0_source"],
            "published": api_data["news_stories_0_published"],
            "url": api_data["news_stories_0_url"],
            "summary": api_data["news_stories_0_summary"] if summarize is not False else None,
            "relevance_score": api_data["news_stories_0_relevance_score"]
        },
        {
            "title": api_data["news_stories_1_title"],
            "source": api_data["news_stories_1_source"],
            "published": api_data["news_stories_1_published"],
            "url": api_data["news_stories_1_url"],
            "summary": api_data["news_stories_1_summary"] if summarize is not False else None,
            "relevance_score": api_data["news_stories_1_relevance_score"]
        }
    ]

    # Apply max_results limit if specified
    if max_results is not None:
        news_stories = news_stories[:max_results]

    # Construct final result matching output schema
    result = {
        "news_stories": news_stories,
        "total_results": min(len(news_stories), api_data["total_results"]),
        "time_period_days": api_data["time_period_days"] if period is None else period,
        "fetched_at": api_data["fetched_at"],
        "metadata": {
            "region": api_data["metadata_region"],
            "language": api_data["metadata_language"],
            "category": api_data["metadata_category"]
        }
    }

    return result