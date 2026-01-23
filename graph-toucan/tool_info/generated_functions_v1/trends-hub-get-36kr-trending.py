from typing import Dict,Any
def trends_hub_get_36kr_trending(type: str = None) -> Dict[str, Any]:
    """
    获取 36 氪热榜，提供创业、商业、科技领域的热门资讯，包含投融资动态、新兴产业分析和商业模式创新信息
    
    Args:
        type (str, optional): 分类，可选值包括 'tech'（科技）、'business'（商业）、'startup'（创业）等，默认为 None 表示全部

    Returns:
        Dict containing a list of trending articles with detailed information.
        - trending_list (List[Dict]): 包含热门文章的列表，每篇文章包含以下字段：
            - title (str): 文章标题
            - cover (str): 封面图片 URL
            - author (str): 作者名称
            - publish_time (str): 发布时间（ISO 格式）
            - read_count (int): 阅读数
            - collect_count (int): 收藏数
            - comment_count (int): 评论数
            - praise_count (int): 点赞数
            - link (str): 文章链接
    """
    def call_external_api(tool_name: str) -> Dict[str, Any]:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - trending_0_title (str): First article title
            - trending_0_cover (str): First article cover image URL
            - trending_0_author (str): First article author name
            - trending_0_publish_time (str): First article publish time in ISO format
            - trending_0_read_count (int): First article read count
            - trending_0_collect_count (int): First article collect count
            - trending_0_comment_count (int): First article comment count
            - trending_0_praise_count (int): First article praise count
            - trending_0_link (str): First article URL
            - trending_1_title (str): Second article title
            - trending_1_cover (str): Second article cover image URL
            - trending_1_author (str): Second article author name
            - trending_1_publish_time (str): Second article publish time in ISO format
            - trending_1_read_count (int): Second article read count
            - trending_1_collect_count (int): Second article collect count
            - trending_1_comment_count (int): Second article comment count
            - trending_1_praise_count (int): Second article praise count
            - trending_1_link (str): Second article URL
        """
        return {
            "trending_0_title": "AI芯片独角兽完成5亿元B轮融资",
            "trending_0_cover": "https://example.com/cover1.jpg",
            "trending_0_author": "36氪财经",
            "trending_0_publish_time": "2024-03-15T10:30:00Z",
            "trending_0_read_count": 12800,
            "trending_0_collect_count": 420,
            "trending_0_comment_count": 87,
            "trending_0_praise_count": 950,
            "trending_0_link": "https://36kr.com/p/1234567890",

            "trending_1_title": "新能源汽车产业链迎来新变局",
            "trending_1_cover": "https://example.com/cover2.jpg",
            "trending_1_author": "未来商业研究院",
            "trending_1_publish_time": "2024-03-15T09:15:00Z",
            "trending_1_read_count": 11500,
            "trending_1_collect_count": 380,
            "trending_1_comment_count": 76,
            "trending_1_praise_count": 890,
            "trending_1_link": "https://36kr.com/p/1234567891"
        }

    try:
        # Validate input
        valid_types = {'tech', 'business', 'startup', 'finance', 'innovation'}
        if type is not None and not isinstance(type, str):
            raise TypeError("Parameter 'type' must be a string or None.")
        if type is not None and type not in valid_types:
            raise ValueError(f"Invalid type '{type}'. Must be one of {valid_types}.")

        # Fetch simulated external data
        api_data = call_external_api("trends-hub-get-36kr-trending")

        # Construct the result structure manually from flat API response
        trending_list = [
            {
                "title": api_data["trending_0_title"],
                "cover": api_data["trending_0_cover"],
                "author": api_data["trending_0_author"],
                "publish_time": api_data["trending_0_publish_time"],
                "read_count": api_data["trending_0_read_count"],
                "collect_count": api_data["trending_0_collect_count"],
                "comment_count": api_data["trending_0_comment_count"],
                "praise_count": api_data["trending_0_praise_count"],
                "link": api_data["trending_0_link"]
            },
            {
                "title": api_data["trending_1_title"],
                "cover": api_data["trending_1_cover"],
                "author": api_data["trending_1_author"],
                "publish_time": api_data["trending_1_publish_time"],
                "read_count": api_data["trending_1_read_count"],
                "collect_count": api_data["trending_1_collect_count"],
                "comment_count": api_data["trending_1_comment_count"],
                "praise_count": api_data["trending_1_praise_count"],
                "link": api_data["trending_1_link"]
            }
        ]

        # Apply filtering logic based on type if provided
        if type == "tech":
            trending_list = [item for item in trending_list if "芯片" in item["title"] or "AI" in item["title"]]
        elif type == "business":
            trending_list = [item for item in trending_list if "商业" in item["title"] or "产业链" in item["title"]]
        elif type == "startup":
            trending_list = [item for item in trending_list if "独角兽" in item["title"] or "融资" in item["title"]]

        return {"trending_list": trending_list}

    except Exception as e:
        # Handle unexpected errors gracefully
        raise RuntimeError(f"Failed to retrieve 36kr trending data: {str(e)}")