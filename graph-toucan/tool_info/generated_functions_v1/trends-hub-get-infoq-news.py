from typing import Dict,Any,Optional
def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - news_0_title (str): Title of the first news article
        - news_0_description (str): Description of the first news article
        - news_0_category (str): Category of the first news article
        - news_0_author (str): Author of the first news article
        - news_0_publish_time (str): Publish time of the first news article
        - news_0_link (str): URL link of the first news article
        - news_1_title (str): Title of the second news article
        - news_1_description (str): Description of the second news article
        - news_1_category (str): Category of the second news article
        - news_1_author (str): Author of the second news article
        - news_1_publish_time (str): Publish time of the second news article
        - news_1_link (str): URL link of the second news article
    """
    return {
        "news_0_title": "AI在云原生架构中的新突破",
        "news_0_description": "最新研究表明，AI模型训练效率提升300%，推动云原生技术革新。",
        "news_0_category": "AI",
        "news_0_author": "张伟",
        "news_0_publish_time": "2023-10-01T08:00:00Z",
        "news_0_link": "https://infoq.com/news/ai-cloud-native-breakthrough",

        "news_1_title": "微服务设计模式最佳实践",
        "news_1_description": "本文深入探讨了现代微服务架构中常用的设计模式及其应用场景。",
        "news_1_category": "架构设计",
        "news_1_author": "李娜",
        "news_1_publish_time": "2023-09-30T14:30:00Z",
        "news_1_link": "https://infoq.com/news/microservices-design-patterns"
    }


def trends_hub_get_infoq_news(region: Optional[str] = None) -> Dict[str, Any]:
    """
    获取 InfoQ 技术资讯，包含软件开发、架构设计、云计算、AI等企业级技术内容和前沿开发者动态。
    
    Args:
        region (Optional[str]): 可选的地区参数，用于过滤特定区域的技术新闻（目前未启用具体逻辑）。
        
    Returns:
        Dict containing:
            - news_list (List[Dict]): 新闻文章列表，每篇文章包含以下字段：
                - title (str): 文章标题
                - description (str): 文章描述
                - category (str): 分类（如 AI、架构设计、云计算等）
                - author (str): 作者姓名
                - publish_time (str): 发布时间（ISO 8601 格式）
                - link (str): 原文链接
                
    Example:
        {
            "news_list": [
                {
                    "title": "AI在云原生架构中的新突破",
                    "description": "最新研究表明，AI模型训练效率提升300%...",
                    "category": "AI",
                    "author": "张伟",
                    "publish_time": "2023-10-01T08:00:00Z",
                    "link": "https://infoq.com/news/ai-cloud-native-breakthrough"
                },
                ...
            ]
        }
    """
    # 调用外部API获取扁平化数据
    api_data = call_external_api("trends-hub-get-infoq-news")
    
    # 显式构造符合输出 schema 的嵌套结构
    news_list = [
        {
            "title": api_data["news_0_title"],
            "description": api_data["news_0_description"],
            "category": api_data["news_0_category"],
            "author": api_data["news_0_author"],
            "publish_time": api_data["news_0_publish_time"],
            "link": api_data["news_0_link"]
        },
        {
            "title": api_data["news_1_title"],
            "description": api_data["news_1_description"],
            "category": api_data["news_1_category"],
            "author": api_data["news_1_author"],
            "publish_time": api_data["news_1_publish_time"],
            "link": api_data["news_1_link"]
        }
    ]
    
    # 构造最终结果
    result = {
        "news_list": news_list
    }
    
    return result