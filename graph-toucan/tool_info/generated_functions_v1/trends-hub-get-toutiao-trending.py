from typing import Dict,Any
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - trending_0_title (str): Title of the first trending item
        - trending_0_cover (str): Cover image URL of the first trending item
        - trending_0_popularity (int): Popularity score of the first trending item
        - trending_0_link (str): Link to the first trending item
        - trending_1_title (str): Title of the second trending item
        - trending_1_cover (str): Cover image URL of the second trending item
        - trending_1_popularity (int): Popularity score of the second trending item
        - trending_1_link (str): Link to the second trending item
    """
    return {
        "trending_0_title": "中国航天发布火星探测最新成果",
        "trending_0_cover": "https://example.com/mars.jpg",
        "trending_0_popularity": 987654,
        "trending_0_link": "https://example.com/news/1",
        "trending_1_title": "暑期旅游市场火爆，多地景区迎来客流高峰",
        "trending_1_cover": "https://example.com/travel.jpg",
        "trending_1_popularity": 876543,
        "trending_1_link": "https://example.com/news/2"
    }

def trends_hub_get_toutiao_trending() -> Dict[str, Any]:
    """
    获取今日头条热榜，包含时政要闻、社会事件、国际新闻、科技发展及娱乐八卦等多领域的热门中文资讯
    
    Returns:
        Dict containing a list of trending items, each with title, cover, popularity, and link.
        - trending_list (List[Dict]): List of trending news items with keys 'title', 'cover', 'popularity', 'link'
    """
    try:
        api_data = call_external_api("trends-hub-get-toutiao-trending")
        
        trending_list = [
            {
                "title": api_data["trending_0_title"],
                "cover": api_data["trending_0_cover"],
                "popularity": api_data["trending_0_popularity"],
                "link": api_data["trending_0_link"]
            },
            {
                "title": api_data["trending_1_title"],
                "cover": api_data["trending_1_cover"],
                "popularity": api_data["trending_1_popularity"],
                "link": api_data["trending_1_link"]
            }
        ]
        
        result = {
            "trending_list": trending_list
        }
        
        return result
        
    except KeyError as e:
        raise ValueError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing trending data: {e}")