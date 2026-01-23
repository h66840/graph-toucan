from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for The Verge news search.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first article
        - result_0_url (str): URL of the first article
        - result_0_published_date (str): Published date of the first article (ISO format)
        - result_0_summary (str): Summary of the first article
        - result_1_title (str): Title of the second article
        - result_1_url (str): URL of the second article
        - result_1_published_date (str): Published date of the second article (ISO format)
        - result_1_summary (str): Summary of the second article
        - total_count (int): Total number of articles found
        - search_query (str): The keyword used in the search
        - time_period_days (int): Number of days in the past that were searched
        - status (str): Status of the operation ("success" or "error")
        - error_message (str): Error message if any, otherwise empty string
    """
    # Simulate realistic data based on keyword
    sample_titles = [
        "Apple Unveils New iPhone with Advanced AI Features",
        "Tesla Launches Next-Gen Autonomous Driving System",
        "Microsoft Announces Major Cloud Computing Update",
        "Google Reveals Breakthrough in Quantum Computing",
        "Amazon Expands Drone Delivery Service Nationwide"
    ]
    sample_summaries = [
        "The latest iPhone model features enhanced camera systems and on-device machine learning capabilities.",
        "Tesla's new autonomous system promises safer and more efficient self-driving experiences.",
        "Microsoft's cloud update includes improved security protocols and faster data processing.",
        "Google's quantum computing breakthrough could revolutionize data encryption methods.",
        "Amazon's drone delivery expansion aims to reduce shipping times across urban areas."
    ]

    # Randomly pick two different articles
    selected_indices = random.sample(range(len(sample_titles)), 2)
    titles = [sample_titles[i] for i in selected_indices]
    summaries = [sample_summaries[i] for i in selected_indices]

    # Generate recent dates within the specified time period
    now = datetime.now()
    date1 = (now - timedelta(days=random.randint(1, 15))).isoformat()
    date2 = (now - timedelta(days=random.randint(1, 15))).isoformat()

    return {
        "result_0_title": titles[0],
        "result_0_url": f"https://www.theverge.com/{random.randint(100000, 999999)}/apple-iphone-ai",
        "result_0_published_date": date1,
        "result_0_summary": summaries[0],
        "result_1_title": titles[1],
        "result_1_url": f"https://www.theverge.com/{random.randint(100000, 999999)}/tesla-autonomous-driving",
        "result_1_published_date": date2,
        "result_1_summary": summaries[1],
        "total_count": 2,
        "search_query": "technology",
        "time_period_days": 30,
        "status": "success",
        "error_message": ""
    }


def the_verge_news_server_search_news(days: Optional[int] = 30, keyword: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for news articles from The Verge by keyword.

    Args:
        days (Optional[int]): Number of days to look back (default: 30)
        keyword (Optional[str]): Keyword to search for in news articles (required)

    Returns:
        Dict containing:
        - results (List[Dict]): list of news articles, each containing 'title', 'url', 'published_date', and 'summary' fields
        - total_count (int): total number of articles found matching the search criteria
        - search_query (str): the keyword used in the search
        - time_period_days (int): number of days in the past that were searched
        - status (str): indicates success or failure of the search operation
        - error_message (str): description of the error if no articles were found or an issue occurred

    Raises:
        ValueError: If keyword is not provided
    """
    # Input validation
    if not keyword:
        return {
            "results": [],
            "total_count": 0,
            "search_query": "",
            "time_period_days": days or 30,
            "status": "error",
            "error_message": "Keyword is required for search"
        }

    # Validate days parameter
    if days is None:
        days = 30
    elif days <= 0:
        days = 30

    # Call external API (simulation)
    try:
        api_data = call_external_api("the-verge-news-server-search-news")

        # Update search query with actual input keyword
        api_data["search_query"] = keyword
        api_data["time_period_days"] = days

        # Construct results list from flattened API response
        results = [
            {
                "title": api_data["result_0_title"],
                "url": api_data["result_0_url"],
                "published_date": api_data["result_0_published_date"],
                "summary": api_data["result_0_summary"]
            },
            {
                "title": api_data["result_1_title"],
                "url": api_data["result_1_url"],
                "published_date": api_data["result_1_published_date"],
                "summary": api_data["result_1_summary"]
            }
        ]

        # Return structured response matching output schema
        return {
            "results": results,
            "total_count": api_data["total_count"],
            "search_query": api_data["search_query"],
            "time_period_days": api_data["time_period_days"],
            "status": api_data["status"],
            "error_message": api_data["error_message"]
        }

    except Exception as e:
        return {
            "results": [],
            "total_count": 0,
            "search_query": keyword or "",
            "time_period_days": days,
            "status": "error",
            "error_message": str(e)
        }