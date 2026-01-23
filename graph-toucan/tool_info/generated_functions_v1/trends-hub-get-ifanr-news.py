def trends_hub_get_ifanr_news(limit: int = 10, offset: int = 0) -> dict:
    """
    获取爱范儿科技快讯，包含最新的科技产品、数码设备、互联网动态等前沿科技资讯。

    Args:
        limit (int, optional): 返回新闻条数限制，默认为10
        offset (int, optional): 偏移量，用于分页，默认为0

    Returns:
        dict: 包含 news_list 字段的字典，news_list 是新闻条目的列表，每个条目包含 title、description 和 link
    """
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - news_0_title (str): First news item title
            - news_0_description (str): First news item description
            - news_0_link (str): First news item URL link
            - news_1_title (str): Second news item title
            - news_1_description (str): Second news item description
            - news_1_link (str): Second news item URL link
        """
        return {
            "news_0_title": "苹果发布新款iPhone 15 Pro，搭载A17芯片",
            "news_0_description": "苹果公司在秋季发布会上推出了iPhone 15 Pro系列，采用钛合金边框设计，性能大幅提升。",
            "news_0_link": "https://www.ifanr.com/news/iphone15-pro-launch",
            "news_1_title": "特斯拉推出完全自动驾驶FSD Beta 12版本",
            "news_1_description": "特斯拉向更多用户推送FSD Beta 12，系统实现端到端神经网络控制。",
            "news_1_link": "https://www.ifanr.com/news/tesla-fsd-beta12"
        }

    # 输入参数验证
    if limit < 1:
        raise ValueError("limit must be a positive integer")
    if offset < 0:
        raise ValueError("offset must be a non-negative integer")

    # 调用外部API获取数据（模拟）
    api_data = call_external_api("trends-hub-get-ifanr-news")

    # 构建符合输出结构的新闻列表
    news_items = []
    for i in range(2):  # 模拟最多返回2条数据
        title_key = f"news_{i}_title"
        desc_key = f"news_{i}_description"
        link_key = f"news_{i}_link"

        if title_key in api_data and api_data[title_key]:
            news_items.append({
                "title": api_data[title_key],
                "description": api_data[desc_key],
                "link": api_data[link_key]
            })

    # 应用 offset 和 limit 进行分页处理
    start_idx = offset
    end_idx = offset + limit
    paginated_news = news_items[start_idx:end_idx]

    return {"news_list": paginated_news}