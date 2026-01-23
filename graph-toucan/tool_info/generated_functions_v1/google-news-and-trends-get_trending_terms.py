from typing import Dict, List, Any, Optional
import time


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Google Trends.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - trend_0_keyword (str): First trending keyword
        - trend_0_volume (str): Search volume for first trend
        - trend_0_started (int): Unix timestamp when first trend started
        - trend_0_link (str): Direct link to Google Trends RSS for first trend
        - trend_0_picture (str): URL of associated image for first trend
        - trend_0_picture_source (str): Source website of the picture for first trend
        - trend_0_trend_keywords_0 (str): First related keyword for first trend
        - trend_0_trend_keywords_1 (str): Second related keyword for first trend
        - trend_0_news_0_source (str): Source of first news article for first trend
        - trend_0_news_0_title (str): Title of first news article for first trend
        - trend_0_news_0_url (str): URL of first news article for first trend
        - trend_0_news_0_picture (str): Picture URL of first news article for first trend
        - trend_0_news_1_source (str): Source of second news article for first trend
        - trend_0_news_1_title (str): Title of second news article for first trend
        - trend_0_news_1_url (str): URL of second news article for first trend
        - trend_0_news_1_picture (str): Picture URL of second news article for first trend
        - trend_1_keyword (str): Second trending keyword
        - trend_1_volume (str): Search volume for second trend
        - trend_1_started (int): Unix timestamp when second trend started
        - trend_1_link (str): Direct link to Google Trends RSS for second trend
        - trend_1_picture (str): URL of associated image for second trend
        - trend_1_picture_source (str): Source website of the picture for second trend
        - trend_1_trend_keywords_0 (str): First related keyword for second trend
        - trend_1_trend_keywords_1 (str): Second related keyword for second trend
        - trend_1_news_0_source (str): Source of first news article for second trend
        - trend_1_news_0_title (str): Title of first news article for second trend
        - trend_1_news_0_url (str): URL of first news article for second trend
        - trend_1_news_0_picture (str): Picture URL of first news article for second trend
        - trend_1_news_1_source (str): Source of second news article for second trend
        - trend_1_news_1_title (str): Title of second news article for second trend
        - trend_1_news_1_url (str): URL of second news article for second trend
        - trend_1_news_1_picture (str): Picture URL of second news article for second trend
    """
    current_time = int(time.time())
    return {
        "trend_0_keyword": "Artificial Intelligence",
        "trend_0_volume": "100000+",
        "trend_0_started": current_time - 3600,
        "trend_0_link": "https://trends.google.com/trends/rss/dailytrends?geo=US",
        "trend_0_picture": "https://example.com/ai.jpg",
        "trend_0_picture_source": "example.com",
        "trend_0_trend_keywords_0": "machine learning",
        "trend_0_trend_keywords_1": "neural networks",
        "trend_0_news_0_source": "TechCrunch",
        "trend_0_news_0_title": "AI Breakthrough in 2024",
        "trend_0_news_0_url": "https://techcrunch.com/ai-breakthrough",
        "trend_0_news_0_picture": "https://techcrunch.com/ai.jpg",
        "trend_0_news_1_source": "The Verge",
        "trend_0_news_1_title": "How AI is Changing the World",
        "trend_0_news_1_url": "https://theverge.com/ai-changing-world",
        "trend_0_news_1_picture": "https://theverge.com/ai-world.jpg",
        "trend_1_keyword": "Climate Change",
        "trend_1_volume": "50000+",
        "trend_1_started": current_time - 7200,
        "trend_1_link": "https://trends.google.com/trends/rss/dailytrends?geo=US",
        "trend_1_picture": "https://example.com/climate.jpg",
        "trend_1_picture_source": "climatewatch.org",
        "trend_1_trend_keywords_0": "global warming",
        "trend_1_trend_keywords_1": "renewable energy",
        "trend_1_news_0_source": "BBC News",
        "trend_1_news_0_title": "Record Temperatures in Europe",
        "trend_1_news_0_url": "https://bbc.com/record-temperatures",
        "trend_1_news_0_picture": "https://bbc.com/temp.jpg",
        "trend_1_news_1_source": "CNN",
        "trend_1_news_1_title": "Climate Summit Outcomes",
        "trend_1_news_1_url": "https://cnn.com/climate-summit",
        "trend_1_news_1_picture": "https://cnn.com/summit.jpg",
    }


def google_news_and_trends_get_trending_terms(full_data: Optional[bool] = False, geo: Optional[str] = "US") -> List[Dict[str, Any]]:
    """
    Returns google trends for a specific geo location.

    Args:
        full_data (bool, optional): Return full data for each trend. Should be False for most use cases.
        geo (str, optional): Country code, e.g. 'US', 'GB', 'IN', etc.

    Returns:
        List[Dict]: list of trending terms with their metadata, each containing:
            - keyword (str): the search term or phrase that is trending
            - volume (str): estimated search volume for the trend, e.g. '100+', '2000+', '10000+'
            - started (int): Unix timestamp indicating when the trend started, present only when available
            - link (str): direct link to the Google Trends RSS feed for the region
            - picture (str): URL of an associated image for the trend, if available
            - picture_source (str): source website of the associated picture
            - trend_keywords (List[str]): related keywords associated with the trend; may be empty
            - news (List[Dict]): list of news articles related to the trend, each with:
                - source (str): publication or website that published the news article
                - title (str): headline or title of the news article
                - picture (str): URL of the article's image
                - url (str): direct URL to the news article

    Raises:
        ValueError: If geo is not a valid country code
    """
    # Input validation
    if geo and not isinstance(geo, str):
        raise ValueError("geo must be a string")
    if full_data is not None and not isinstance(full_data, bool):
        raise ValueError("full_data must be a boolean")

    # Simulate country code validation
    valid_geo_codes = ["US", "GB", "IN", "CA", "AU", "DE", "FR", "JP", "CN", "BR"]
    if geo and geo not in valid_geo_codes:
        raise ValueError(f"Invalid geo code: {geo}. Must be one of {valid_geo_codes}")

    # Fetch data from external API (simulated)
    api_data = call_external_api("google-news-and-trends-get_trending_terms")

    # Construct the result list by mapping flat fields to nested structure
    trends = []

    for i in range(2):  # Two trends
        trend_key = f"trend_{i}"
        keyword = api_data.get(f"{trend_key}_keyword")
        if not keyword:
            continue

        # Build news articles list
        news_articles = []
        for j in range(2):  # Two news articles per trend
            news_source = api_data.get(f"{trend_key}_news_{j}_source")
            if not news_source:
                continue
            news_articles.append({
                "source": news_source,
                "title": api_data.get(f"{trend_key}_news_{j}_title", ""),
                "picture": api_data.get(f"{trend_key}_news_{j}_picture", ""),
                "url": api_data.get(f"{trend_key}_news_{j}_url", "")
            })

        # Build trend keywords list
        trend_keywords = []
        for j in range(2):  # Two related keywords per trend
            kw = api_data.get(f"{trend_key}_trend_keywords_{j}")
            if kw:
                trend_keywords.append(kw)

        # Construct the trend dictionary
        trend = {
            "keyword": keyword,
            "volume": api_data.get(f"{trend_key}_volume", ""),
            "started": api_data.get(f"{trend_key}_started"),
            "link": api_data.get(f"{trend_key}_link", ""),
            "picture": api_data.get(f"{trend_key}_picture", ""),
            "picture_source": api_data.get(f"{trend_key}_picture_source", ""),
            "trend_keywords": trend_keywords,
            "news": news_articles
        }

        trends.append(trend)

    return trends