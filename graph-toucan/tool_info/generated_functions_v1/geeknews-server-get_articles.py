from typing import List, Dict, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - article_0_title (str): Title of the first article
        - article_0_url (str): URL of the first article
        - article_0_points (int): Points for the first article
        - article_0_author (str): Author of the first article
        - article_0_time (str): Time when the first article was posted
        - article_0_rank (int): Rank of the first article
        - article_0_commentCount (int): Number of comments on the first article
        - article_1_title (str): Title of the second article
        - article_1_url (str): URL of the second article
        - article_1_points (int): Points for the second article
        - article_1_author (str): Author of the second article
        - article_1_time (str): Time when the second article was posted
        - article_1_rank (int): Rank of the second article
        - article_1_commentCount (int): Number of comments on the second article
    """
    return {
        "article_0_title": "The Rise of Quantum Computing in 2024",
        "article_0_url": "https://geeknews.example.com/quantum-computing-2024",
        "article_0_points": 150,
        "article_0_author": "alice_dev",
        "article_0_time": "2 hours ago",
        "article_0_rank": 1,
        "article_0_commentCount": 42,
        "article_1_title": "Why Rust is Taking Over Systems Programming",
        "article_1_url": "https://geeknews.example.com/rust-takeover",
        "article_1_points": 123,
        "article_1_author": "bob_engineer",
        "article_1_time": "3 hours ago",
        "article_1_rank": 2,
        "article_1_commentCount": 38,
    }

def geeknews_server_get_articles(type: str = "top", limit: int = 10) -> List[Dict[str, Any]]:
    """
    GeekNews에서 아티클을 가져오는 도구
    
    Args:
        type (str): 아티클 유형 (top, new, ask, show). 기본값은 'top'.
        limit (int): 반환할 아티클 수 (최대 30). 기본값은 10.
    
    Returns:
        List[Dict[str, Any]]: 각 아티클의 'title', 'url', 'points', 'author', 'time', 'rank', 'commentCount'를 포함하는 딕셔너리 목록.
    
    Raises:
        ValueError: 유효하지 않은 아티클 유형이 지정된 경우.
    """
    valid_types = ["top", "new", "ask", "show"]
    if type not in valid_types:
        raise ValueError(f"Invalid article type: {type}. Must be one of {valid_types}")
    
    if limit < 1:
        limit = 1
    elif limit > 30:
        limit = 30

    api_data = call_external_api("geeknews-server-get_articles")
    
    articles = []
    for i in range(min(limit, 2)):  # We only have 2 mock items
        prefix = f"article_{i}"
        article = {
            "title": api_data[f"{prefix}_title"],
            "url": api_data[f"{prefix}_url"],
            "points": api_data[f"{prefix}_points"],
            "author": api_data[f"{prefix}_author"],
            "time": api_data[f"{prefix}_time"],
            "rank": api_data[f"{prefix}_rank"],
            "commentCount": api_data[f"{prefix}_commentCount"]
        }
        articles.append(article)
    
    return articles