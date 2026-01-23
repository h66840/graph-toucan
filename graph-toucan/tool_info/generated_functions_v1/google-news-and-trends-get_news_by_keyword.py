from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google News and Trends.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first article
        - result_0_url (str): URL of the first article
        - result_0_source (str): Source of the first article
        - result_0_published_time (str): Published time of the first article
        - result_0_snippet (str): Snippet of the first article
        - result_0_summary (str): Summary of the first article if summarize=True or full_data=True
        - result_1_title (str): Title of the second article
        - result_1_url (str): URL of the second article
        - result_1_source (str): Source of the second article
        - result_1_published_time (str): Published time of the second article
        - result_1_snippet (str): Snippet of the second article
        - result_1_summary (str): Summary of the second article if summarize=True or full_data=True
        - total_count (int): Total number of articles found
        - query_metadata_keyword (str): Search keyword used
        - query_metadata_period_days (int): Number of days to look back
        - query_metadata_max_results_requested (int): Maximum number of results requested
        - query_metadata_timestamp (str): Timestamp when the query was executed
        - has_more_results (bool): Whether more results are available beyond max_results
    """
    return {
        "result_0_title": "Artificial Intelligence Transforms Healthcare Industry",
        "result_0_url": "https://example-news.com/ai-healthcare-breakthrough",
        "result_0_source": "Tech Daily",
        "result_0_published_time": "2023-10-05T08:30:00Z",
        "result_0_snippet": "AI is revolutionizing diagnostics and patient care with new machine learning models.",
        "result_0_summary": "Advances in AI are enabling faster diagnosis and personalized treatment plans in healthcare.",
        "result_1_title": "Google Launches New AI-Powered Search Features",
        "result_1_url": "https://example-news.com/google-new-ai-search",
        "result_1_source": "Search Engine Journal",
        "result_1_published_time": "2023-10-04T14:22:00Z",
        "result_1_snippet": "Google introduces AI-generated summaries and enhanced contextual understanding in search.",
        "result_1_summary": "Google's latest update uses large language models to provide concise summaries directly in search results.",
        "total_count": 42,
        "query_metadata_keyword": "AI",
        "query_metadata_period_days": 7,
        "query_metadata_max_results_requested": 2,
        "query_metadata_timestamp": datetime.utcnow().isoformat() + "Z",
        "has_more_results": True,
    }


def google_news_and_trends_get_news_by_keyword(
    keyword: str,
    full_data: Optional[bool] = False,
    max_results: Optional[int] = 10,
    period: Optional[int] = 30,
    summarize: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Find articles by keyword using Google News.

    Args:
        full_data (bool, optional): Return full data for each article. If False a summary should be created by setting the summarize flag.
        keyword (str, required): Search term to find articles.
        max_results (int, optional): Maximum number of results to return.
        period (int, optional): Number of days to look back for articles.
        summarize (bool, optional): Generate a summary of the article, will first try LLM Sampling but if unavailable will use nlp.

    Returns:
        Dict containing:
        - results (List[Dict]): List of article objects with keys: title, url, source, published_time, snippet, and optionally summary
        - total_count (int): Total number of articles found
        - query_metadata (Dict): Metadata about the query including keyword, period_days, max_results_requested, and timestamp
        - has_more_results (bool): Whether more results exist beyond the returned set
    """
    if not keyword:
        raise ValueError("Keyword is required")

    if max_results is not None and max_results <= 0:
        raise ValueError("max_results must be a positive integer")

    if period is not None and period <= 0:
        raise ValueError("period must be a positive integer")

    # Call external API to get flattened data
    api_data = call_external_api("google-news-and-trends-get_news_by_keyword")

    # Construct results list from indexed fields
    results = []
    for i in range(2):  # We simulate 2 results as per call_external_api
        title_key = f"result_{i}_title"
        if title_key not in api_data:
            break

        article = {
            "title": api_data[f"result_{i}_title"],
            "url": api_data[f"result_{i}_url"],
            "source": api_data[f"result_{i}_source"],
            "published_time": api_data[f"result_{i}_published_time"],
            "snippet": api_data[f"result_{i}_snippet"],
        }

        # Add summary only if requested
        if summarize or full_data:
            article["summary"] = api_data[f"result_{i}_summary"]

        results.append(article)

    # Limit results based on max_results
    results = results[:max_results]

    # Construct final response
    response = {
        "results": results,
        "total_count": api_data["total_count"],
        "query_metadata": {
            "keyword": api_data["query_metadata_keyword"],
            "period_days": api_data["query_metadata_period_days"],
            "max_results_requested": api_data["query_metadata_max_results_requested"],
            "timestamp": api_data["query_metadata_timestamp"],
        },
        "has_more_results": api_data["has_more_results"],
    }

    return response