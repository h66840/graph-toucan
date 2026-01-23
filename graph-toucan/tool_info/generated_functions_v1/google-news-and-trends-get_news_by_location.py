from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google News and Trends.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - article_0_title (str): Title of the first article
        - article_0_source (str): Source of the first article
        - article_0_published_at (str): ISO datetime string of publication for first article
        - article_0_url (str): URL of the first article
        - article_0_summary (str): Summary of the first article (if summarize=True)
        - article_0_location_relevance (float): Confidence score of location match for first article
        - article_0_image_url (str): Image URL of the first article (optional)
        - article_1_title (str): Title of the second article
        - article_1_source (str): Source of the second article
        - article_1_published_at (str): ISO datetime string of publication for second article
        - article_1_url (str): URL of the second article
        - article_1_summary (str): Summary of the second article (if summarize=True)
        - article_1_location_relevance (float): Confidence score of location match for second article
        - article_1_image_url (str): Image URL of the second article (optional)
        - total_results (int): Total number of articles found matching the query
        - query_location (str): The resolved geographic location used in the search
        - time_period_days (int): Number of days back covered by the search
        - fetched_at (str): ISO 8601 timestamp when the results were retrieved
        - metadata_search_id (str): Unique identifier for the search
        - metadata_status (str): Status of the request (e.g., 'success')
        - metadata_provider (str): Provider name ('Google News')
        - metadata_warnings (str): Any warnings or limitations applied
    """
    now = datetime.utcnow()
    two_days_ago = (now - timedelta(days=2)).isoformat()
    one_day_ago = (now - timedelta(days=1)).isoformat()

    return {
        "article_0_title": "Major Storm Hits New York City",
        "article_0_source": "The New York Times",
        "article_0_published_at": f"{one_day_ago}Z",
        "article_0_url": "https://example.com/news/storm-nyc",
        "article_0_summary": "A powerful storm caused widespread power outages across New York City yesterday.",
        "article_0_location_relevance": 0.95,
        "article_0_image_url": "https://example.com/images/storm-nyc.jpg",

        "article_1_title": "Tech Conference Draws Crowds in NYC",
        "article_1_source": "TechCrunch",
        "article_1_published_at": f"{two_days_ago}Z",
        "article_1_url": "https://example.com/news/tech-conference-nyc",
        "article_1_summary": "Over 10,000 attendees gathered for the annual tech innovation summit in Manhattan.",
        "article_1_location_relevance": 0.89,
        "article_1_image_url": "https://example.com/images/tech-nyc.jpg",

        "total_results": 42,
        "query_location": "New York City, United States",
        "time_period_days": 7,
        "fetched_at": now.isoformat() + "Z",
        "metadata_search_id": "snk_123456789",
        "metadata_status": "success",
        "metadata_provider": "Google News",
        "metadata_warnings": "",
    }


def google_news_and_trends_get_news_by_location(
    location: str,
    full_data: Optional[bool] = None,
    max_results: Optional[int] = None,
    period: Optional[int] = None,
    summarize: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Find articles by location using Google News.

    Args:
        location (str): Name of city/state/country (required).
        full_data (bool, optional): Return full data for each article. If False, a summary should be created.
        max_results (int, optional): Maximum number of results to return.
        period (int, optional): Number of days to look back for articles.
        summarize (bool, optional): Generate a summary of the article.

    Returns:
        Dict containing:
        - articles (List[Dict]): List of news articles with structured information including title, source,
          published_at, url, summary (if summarize=True), location_relevance, and image_url.
        - total_results (int): Total number of articles found matching the query.
        - query_location (str): The resolved geographic location used in the search.
        - time_period_days (int): Number of days back covered by the search.
        - fetched_at (str): ISO 8601 timestamp when the results were retrieved.
        - metadata (Dict): Additional service-level metadata such as search_id, status, provider, and warnings.

    Raises:
        ValueError: If location is empty or not provided.
    """
    if not location or not location.strip():
        raise ValueError("Location is required and cannot be empty.")

    # Normalize location input
    normalized_location = location.strip().title()

    # Apply defaults
    full_data = True if full_data is None else full_data
    summarize = True if summarize is None else summarize
    max_results = max_results or 10
    period = period or 7

    # Fetch simulated external data
    api_data = call_external_api("google-news-and-trends-get_news_by_location")

    # Construct articles list from flattened API response
    articles = []
    for i in range(2):  # We have two articles in the mock data
        if i >= max_results:
            break
        title_key = f"article_{i}_title"
        if title_key not in api_data:
            continue

        article = {
            "title": api_data[f"article_{i}_title"],
            "source": api_data[f"article_{i}_source"],
            "published_at": api_data[f"article_{i}_published_at"],
            "url": api_data[f"article_{i}_url"],
            "location_relevance": api_data[f"article_{i}_location_relevance"],
        }

        # Add image_url if present
        image_url = api_data.get(f"article_{i}_image_url")
        if image_url:
            article["image_url"] = image_url

        # Add summary if requested
        if summarize:
            summary = api_data.get(f"article_{i}_summary")
            article["summary"] = summary or "Summary not available."

        articles.append(article)

    # Construct metadata
    metadata = {
        "search_id": api_data["metadata_search_id"],
        "status": api_data["metadata_status"],
        "provider": api_data["metadata_provider"],
    }
    if api_data["metadata_warnings"]:
        metadata["warnings"] = api_data["metadata_warnings"]

    # Final result
    result = {
        "articles": articles,
        "total_results": api_data["total_results"],
        "query_location": api_data["query_location"],
        "time_period_days": api_data["time_period_days"],
        "fetched_at": api_data["fetched_at"],
        "metadata": metadata,
    }

    return result