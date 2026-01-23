from typing import Dict, List, Any, Optional
import random
from datetime import datetime, timedelta

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for crypto-research-server-research_search_reports.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first matching report
        - result_0_date (str): Date of the first report in YYYY-MM-DD format
        - result_0_author (str): Author of the first report
        - result_0_summary (str): Summary of the first report
        - result_0_url (str): URL link to the first report
        - result_0_relevance_score (float): Relevance score between 0 and 1 for the first report
        - result_1_title (str): Title of the second matching report
        - result_1_date (str): Date of the second report in YYYY-MM-DD format
        - result_1_author (str): Author of the second report
        - result_1_summary (str): Summary of the second report
        - result_1_url (str): URL link to the second report
        - result_1_relevance_score (float): Relevance score between 0 and 1 for the second report
        - total_count (int): Total number of reports found matching the keyword
        - filter_day (str): Day filter applied (e.g., '2023-10-05')
        - filter_keyword (str): Keyword used in search
        - has_more (bool): Whether more results are available beyond current set
        - metadata_search_time_ms (int): Time taken for search in milliseconds
        - metadata_source_count (int): Number of sources searched
        - metadata_earliest_date (str): Earliest report date found in YYYY-MM-DD format
    """
    # Generate deterministic but realistic values based on tool name
    random.seed(tool_name.__hash__() % (2**32))

    today = datetime.today().strftime('%Y-%m-%d')
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    dates = [today, yesterday]

    return {
        "result_0_title": f"Market Analysis: {tool_name.split('_')[-1].title()} Trends",
        "result_0_date": random.choice(dates),
        "result_0_author": "Dr. Alice Chen",
        "result_0_summary": "Comprehensive analysis of recent cryptocurrency market movements with focus on volatility indicators and investor sentiment.",
        "result_0_url": "https://research.crypto.example.com/reports/12345",
        "result_0_relevance_score": round(random.uniform(0.7, 0.95), 3),
        
        "result_1_title": f"Technical Outlook: {tool_name.split('_')[-1].title()} Forecast",
        "result_1_date": random.choice(dates),
        "result_1_author": "James Rodriguez",
        "result_1_summary": "Technical indicators suggest bullish momentum continuing over the next quarter with key resistance levels identified.",
        "result_1_url": "https://research.crypto.example.com/reports/12346",
        "result_1_relevance_score": round(random.uniform(0.6, 0.9), 3),
        
        "total_count": random.randint(5, 20),
        "filter_day": dates[0],
        "filter_keyword": "bitcoin",
        "has_more": random.choice([True, False]),
        "metadata_search_time_ms": random.randint(45, 200),
        "metadata_source_count": random.randint(3, 8),
        "metadata_earliest_date": (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    }

def crypto_research_server_research_search_reports(
    keyword: str, 
    day: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for reports on Research knowledge base.
    
    Args:
        keyword (str): Keyword to search for reports (required)
        day (Optional[str]): Day of results in YYYY-MM-DD format (default: today)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of report objects with 'title', 'date', 'author', 
          'summary', 'url', and 'relevance_score' fields
        - total_count (int): Total number of reports found
        - filters_applied (Dict): Dictionary showing filters used ('day' and 'keyword')
        - has_more (bool): Whether more results are available
        - metadata (Dict): Additional info like 'search_time_ms', 'source_count', 'earliest_date'
    
    Raises:
        ValueError: If keyword is empty or None
    """
    if not keyword or not keyword.strip():
        raise ValueError("Parameter 'keyword' is required and cannot be empty")
    
    keyword = keyword.strip()
    
    # Use provided day or default to today
    target_day = day if day else datetime.today().strftime('%Y-%m-%d')
    
    # Call external API (simulated)
    api_data = call_external_api("crypto-research-server-research_search_reports")
    
    # Override keyword in filters with actual input
    api_data["filter_keyword"] = keyword
    api_data["filter_day"] = target_day
    
    # Construct results list from indexed fields
    results = [
        {
            "title": api_data["result_0_title"],
            "date": api_data["result_0_date"],
            "author": api_data["result_0_author"],
            "summary": api_data["result_0_summary"],
            "url": api_data["result_0_url"],
            "relevance_score": api_data["result_0_relevance_score"]
        },
        {
            "title": api_data["result_1_title"],
            "date": api_data["result_1_date"],
            "author": api_data["result_1_author"],
            "summary": api_data["result_1_summary"],
            "url": api_data["result_1_url"],
            "relevance_score": api_data["result_1_relevance_score"]
        }
    ]
    
    # Apply day filter if specified
    if target_day:
        filtered_results = [r for r in results if r["date"] == target_day]
        # If no results match the day, return the original ones (mimic real system behavior)
        if not filtered_results:
            filtered_results = results
        results = filtered_results
    
    # Construct final output matching schema
    output = {
        "results": results,
        "total_count": api_data["total_count"],
        "filters_applied": {
            "day": api_data["filter_day"],
            "keyword": api_data["filter_keyword"]
        },
        "has_more": api_data["has_more"],
        "metadata": {
            "search_time_ms": api_data["metadata_search_time_ms"],
            "source_count": api_data["metadata_source_count"],
            "earliest_date": api_data["metadata_earliest_date"]
        }
    }
    
    return output