from typing import Dict,Any
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): Title of the weekly news edition
        - number (int): Issue number of the weekly news
        - id (str): Unique identifier for the weekly news edition
        - content (str): Main content or summary text of the weekly news
        - url (str): Direct URL to view the full weekly news online
        - item_0_title (str): Title of the first featured news item
        - item_0_url (str): URL of the first featured news item
        - item_0_rank (int): Rank of the first featured news item
        - item_1_title (str): Title of the second featured news item
        - item_1_url (str): URL of the second featured news item
        - item_1_rank (int): Rank of the second featured news item
    """
    return {
        "title": "GeekNews Weekly Edition #123",
        "number": 123,
        "id": "weekly-123",
        "content": "This week in tech: major advancements in AI and cloud computing.",
        "url": "https://geeknews.example.com/weekly/123",
        "item_0_title": "New AI Model Breaks Performance Records",
        "item_0_url": "https://geeknews.example.com/news/ai-record",
        "item_0_rank": 1,
        "item_1_title": "Cloud Providers Announce New Security Features",
        "item_1_url": "https://geeknews.example.com/news/cloud-security",
        "item_1_rank": 2
    }


def geeknews_server_get_weekly_news(weekly_id: str = "") -> Dict[str, Any]:
    """
    GeekNews에서 주간 뉴스를 가져오는 도구

    Args:
        weekly_id (str, optional): 주간 뉴스 ID (빈 문자열인 경우 가장 최근 주간 뉴스를 가져옴)

    Returns:
        Dict[str, Any]: 주간 뉴스 정보 containing:
            - title (str): title of the weekly news edition
            - number (int): issue number of the weekly news
            - id (str): unique identifier for the weekly news edition
            - content (str): main content or summary text of the weekly news
            - url (str): direct URL to view the full weekly news online
            - items (List[Dict]): list of featured news items in this edition, each with 'title', 'url', and 'rank' fields
    """
    if not isinstance(weekly_id, str):
        raise TypeError("weekly_id must be a string")

    # Call external API to get flat data
    api_data = call_external_api("geeknews-server-get_weekly_news")

    # Construct nested structure matching output schema
    result = {
        "title": api_data["title"],
        "number": api_data["number"],
        "id": api_data["id"],
        "content": api_data["content"],
        "url": api_data["url"],
        "items": [
            {
                "title": api_data["item_0_title"],
                "url": api_data["item_0_url"],
                "rank": api_data["item_0_rank"]
            },
            {
                "title": api_data["item_1_title"],
                "url": api_data["item_1_url"],
                "rank": api_data["item_1_rank"]
            }
        ]
    }

    return result