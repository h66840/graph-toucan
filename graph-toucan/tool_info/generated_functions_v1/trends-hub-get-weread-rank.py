from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for WeRead rank.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - book_0_title (str): Title of the first book
        - book_0_description (str): Description of the first book
        - book_0_cover (str): URL to the cover image of the first book
        - book_0_author (str): Author of the first book
        - book_0_publish_time (str): Publish time of the first book in ISO format
        - book_0_reading_count (int): Number of readings for the first book
        - book_0_link (str): Link to the first book on WeRead
        - book_1_title (str): Title of the second book
        - book_1_description (str): Description of the second book
        - book_1_cover (str): URL to the cover image of the second book
        - book_1_author (str): Author of the second book
        - book_1_publish_time (str): Publish time of the second book in ISO format
        - book_1_reading_count (int): Number of readings for the second book
        - book_1_link (str): Link to the second book on WeRead
    """
    return {
        "book_0_title": "三体",
        "book_0_description": "一部关于宇宙文明与人类命运的科幻巨作。",
        "book_0_cover": "https://example.com/covers/santi.jpg",
        "book_0_author": "刘慈欣",
        "book_0_publish_time": "2008-01-01T00:00:00",
        "book_0_reading_count": 125000,
        "book_0_link": "https://weread.qq.com/web/bookDetail/santi",
        
        "book_1_title": "活着",
        "book_1_description": "讲述一个人在动荡时代中坚韧生存的故事。",
        "book_1_cover": "https://example.com/covers/huozhe.jpg",
        "book_1_author": "余华",
        "book_1_publish_time": "1993-01-01T00:00:00",
        "book_1_reading_count": 210000,
        "book_1_link": "https://weread.qq.com/web/bookDetail/huozhe"
    }

def trends_hub_get_weread_rank(category: Optional[str] = None) -> Dict[str, Any]:
    """
    获取微信读书排行榜，包含热门小说、畅销书籍、新书推荐及各类文学作品的阅读数据和排名信息。

    Args:
        category (Optional[str]): 排行榜分区，如 "fiction", "best_seller", "new_books" 等。
                                 如果未提供，则返回默认综合榜单。

    Returns:
        Dict[str, Any]: 包含 books 列表的字典，每个 book 是一个字典，包含：
            - title (str): 书名
            - description (str): 书籍描述
            - cover (str): 封面图片链接
            - author (str): 作者
            - publish_time (str): 出版时间（ISO格式）
            - reading_count (int): 阅读人数
            - link (str): 书籍详情链接
    """
    # Validate input
    valid_categories = ["fiction", "best_seller", "new_books", "literature", "science", None]
    if category not in valid_categories:
        raise ValueError(f"Invalid category: {category}. Valid categories are {valid_categories[:-1]}")

    # Fetch data from simulated external API
    api_data = call_external_api("trends-hub-get-weread-rank")

    # Construct books list from flattened API response
    books: List[Dict[str, Any]] = [
        {
            "title": api_data["book_0_title"],
            "description": api_data["book_0_description"],
            "cover": api_data["book_0_cover"],
            "author": api_data["book_0_author"],
            "publish_time": api_data["book_0_publish_time"],
            "reading_count": api_data["book_0_reading_count"],
            "link": api_data["book_0_link"]
        },
        {
            "title": api_data["book_1_title"],
            "description": api_data["book_1_description"],
            "cover": api_data["book_1_cover"],
            "author": api_data["book_1_author"],
            "publish_time": api_data["book_1_publish_time"],
            "reading_count": api_data["book_1_reading_count"],
            "link": api_data["book_1_link"]
        }
    ]

    return {
        "books": books
    }