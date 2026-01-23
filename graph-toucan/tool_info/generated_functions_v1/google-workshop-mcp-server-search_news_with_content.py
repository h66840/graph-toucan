from typing import Dict, List, Any, Optional
import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching news search results from an external API.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - news_results_0_title (str): Title of the first news article
        - news_results_0_source (str): Source of the first news article
        - news_results_0_date (str): Publication date of the first news article
        - news_results_0_url (str): URL of the first news article
        - news_results_1_title (str): Title of the second news article
        - news_results_1_source (str): Source of the second news article
        - news_results_1_date (str): Publication date of the second news article
        - news_results_1_url (str): URL of the second news article
        - first_article_content (str): Full textual content of the first article
        - total_results_count (int): Total number of articles found
        - search_metadata_keyword (str): The keyword used in the search
        - search_metadata_timestamp (str): ISO format timestamp of the search
        - search_metadata_reliability (float): Reliability score of the results (0.0 to 1.0)
        - search_metadata_source_count (int): Number of distinct sources used
    """
    return {
        "news_results_0_title": "AI Technology Advances in South Korea",
        "news_results_0_source": "Korea Times",
        "news_results_0_date": "2024-03-15T08:30:00Z",
        "news_results_0_url": "https://example.com/news/ai-advances-korea",
        "news_results_1_title": "Seoul Hosts Global Tech Summit on Artificial Intelligence",
        "news_results_1_source": "Tech Daily",
        "news_results_1_date": "2024-03-14T12:15:00Z",
        "news_results_1_url": "https://example.com/news/seoul-tech-summit",
        "first_article_content": (
            "South Korea has made significant progress in artificial intelligence research. "
            "The Ministry of Science and ICT announced new investments in AI startups and "
            "academic research programs. Experts predict that these developments will boost "
            "the national economy and enhance technological competitiveness globally. "
            "The government plans to establish AI innovation hubs in major cities by 2025."
        ),
        "total_results_count": 47,
        "search_metadata_keyword": "AI technology",
        "search_metadata_timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "search_metadata_reliability": 0.94,
        "search_metadata_source_count": 12,
    }


def google_workshop_mcp_server_search_news_with_content(keyword: str) -> Dict[str, Any]:
    """
    키워드로 뉴스 검색 및 첫 번째 기사 내용 가져오기

    Args:
        keyword (str): 검색할 키워드

    Returns:
        Dict containing:
        - news_results (List[Dict]): List of news articles with title, source, publication date, and URL
        - first_article_content (str): Full textual content of the first (most relevant) article
        - total_results_count (int): Total number of news articles found
        - search_metadata (Dict): Metadata about the search operation including keyword, timestamp, reliability, and source count

    Raises:
        ValueError: If keyword is empty or not a string
    """
    if not keyword:
        raise ValueError("Keyword must be a non-empty string.")
    if not isinstance(keyword, str):
        raise ValueError("Keyword must be a string.")

    # Call external API (simulated)
    api_data = call_external_api("google-workshop-mcp-server-search_news_with_content")

    # Construct news_results list from indexed fields
    news_results: List[Dict[str, Any]] = [
        {
            "title": api_data["news_results_0_title"],
            "source": api_data["news_results_0_source"],
            "publication_date": api_data["news_results_0_date"],
            "url": api_data["news_results_0_url"],
        },
        {
            "title": api_data["news_results_1_title"],
            "source": api_data["news_results_1_source"],
            "publication_date": api_data["news_results_1_date"],
            "url": api_data["news_results_1_url"],
        },
    ]

    # Construct search_metadata
    search_metadata: Dict[str, Any] = {
        "keyword": api_data["search_metadata_keyword"],
        "timestamp": api_data["search_metadata_timestamp"],
        "reliability": api_data["search_metadata_reliability"],
        "source_count": api_data["search_metadata_source_count"],
    }

    # Build final result structure
    result = {
        "news_results": news_results,
        "first_article_content": api_data["first_article_content"],
        "total_results_count": api_data["total_results_count"],
        "search_metadata": search_metadata,
    }

    return result