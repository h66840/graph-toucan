from typing import Dict, List, Any, Optional


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching internet hotspots data from external API.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - weibo_0_title (str): Title of the first trending topic on Weibo
        - weibo_0_rank (int): Rank of the first trending topic on Weibo
        - weibo_0_url (str): URL of the first trending topic on Weibo
        - toutiao_0_title (str): Title of the first trending topic on Toutiao
        - toutiao_0_url (str): URL of the first trending topic on Toutiao
        - zhihu_daily_0_title (str): Title of the first trending topic on Zhihu Daily
        - zhihu_daily_0_url (str): URL of the first trending topic on Zhihu Daily
        - hupu_0_title (str): Title of the first trending topic on Hupu
        - hupu_0_url (str): URL of the first trending topic on Hupu
        - kr36_0_title (str): Title of the first trending topic on 36Kr
        - kr36_0_url (str): URL of the first trending topic on 36Kr
        - bilibili_0_title (str): Title of the first trending topic on Bilibili
        - bilibili_0_url (str): URL of the first trending topic on Bilibili
        - zhihu_0_title (str): Title of the first trending topic on Zhihu
        - zhihu_0_url (str): URL of the first trending topic on Zhihu
        - it_news_0_title (str): Title of the first IT news item
        - it_news_0_summary (str): Summary of the first IT news item
        - huxiu_0_title (str): Title of the first trending topic on Huxiu
        - huxiu_0_url (str): URL of the first trending topic on Huxiu
        - pmcafe_0_title (str): Title of the first trending topic on PMCAFE
        - pmcafe_0_url (str): URL of the first trending topic on PMCAFE
        - baidu_0_title (str): Title of the first trending topic on Baidu
        - baidu_0_rank (int): Rank of the first trending topic on Baidu
        - douyin_0_title (str): Title of the first trending topic on Douyin
        - douyin_0_summary (str): Summary of the first trending topic on Douyin
        - douban_0_title (str): Title of the first trending topic on Douban
        - douban_0_url (str): URL of the first trending topic on Douban
    """
    return {
        "weibo_0_title": "Weibo Top Trending Topic",
        "weibo_0_rank": 1,
        "weibo_0_url": "https://weibo.com/trending/1",
        "toutiao_0_title": "Today's Headline News",
        "toutiao_0_url": "https://toutiao.com/news/1",
        "zhihu_daily_0_title": "Zhihu Daily Featured Story",
        "zhihu_daily_0_url": "https://daily.zhihu.com/story/1",
        "hupu_0_title": "Hupu Street Talk Highlight",
        "hupu_0_url": "https://bbs.hupu.com/1",
        "kr36_0_title": "36Kr Latest Innovation Report",
        "kr36_0_url": "https://36kr.com/report/1",
        "bilibili_0_title": "Bilibili Popular Video",
        "bilibili_0_url": "https://bilibili.com/video/1",
        "zhihu_0_title": "Zhihu Popular Question",
        "zhihu_0_url": "https://zhihu.com/question/1",
        "it_news_0_title": "Latest Tech Breakthrough",
        "it_news_0_summary": "A major advancement in AI technology was announced today.",
        "huxiu_0_title": "Huxiu Business Insight",
        "huxiu_0_url": "https://huxiu.com/article/1",
        "pmcafe_0_title": "Product Manager Strategy Guide",
        "pmcafe_0_url": "https://pmcafe.cn/guide/1",
        "baidu_0_title": "Baidu Most Searched Term",
        "baidu_0_rank": 1,
        "douyin_0_title": "Douyin Viral Short Video",
        "douyin_0_summary": "A short video about a dancing cat went viral.",
        "douban_0_title": "Douban Group Discussion",
        "douban_0_url": "https://douban.com/group/topic/1"
    }


def pulse_cn_mcp_server_internet_hotspots_aggregator(limit: Optional[int] = 10) -> Dict[str, List[Dict[str, Any]]]:
    """
    获取互联网热点聚合数据，返回包含热点内容的实时数据。

    支持多个平台的热点聚合，包括微博热搜、今日头条、知乎日报、虎扑步行街、36氪、哔哩哔哩热榜、
    知乎、IT资讯、虎嗅网、人人都是产品经理热榜、百度、抖音热点、豆瓣小组精选。

    Args:
        limit (Optional[int]): 每个分类显示的热点数量限制，默认为10。

    Returns:
        Dict[str, List[Dict[str, Any]]]: 包含平台名称作为键，每个值为一个包含热点信息的列表。
        每个热点信息字典包含 'title' 字段，并可能包含 'rank', 'url', 或 'summary' 字段。

    Raises:
        ValueError: 当 limit 不是正整数时抛出异常。
    """
    if limit is not None:
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer")

    # Fetch simulated data from external API
    api_data = call_external_api("pulse-cn-mcp-server-internet-hotspots-aggregator")

    # Construct the nested output structure
    hotspots: Dict[str, List[Dict[str, Any]]] = {}

    # Weibo
    weibo_items = []
    if "weibo_0_title" in api_data:
        item = {
            "title": api_data["weibo_0_title"],
            "url": api_data.get("weibo_0_url"),
        }
        if "weibo_0_rank" in api_data:
            item["rank"] = api_data["weibo_0_rank"]
        weibo_items.append(item)
    hotspots["weibo"] = weibo_items[:limit]

    # Toutiao
    toutiao_items = []
    if "toutiao_0_title" in api_data:
        item = {
            "title": api_data["toutiao_0_title"],
            "url": api_data.get("toutiao_0_url"),
        }
        toutiao_items.append(item)
    hotspots["toutiao"] = toutiao_items[:limit]

    # Zhihu Daily
    zhihu_daily_items = []
    if "zhihu_daily_0_title" in api_data:
        item = {
            "title": api_data["zhihu_daily_0_title"],
            "url": api_data.get("zhihu_daily_0_url"),
        }
        zhihu_daily_items.append(item)
    hotspots["zhihu_daily"] = zhihu_daily_items[:limit]

    # Hupu
    hupu_items = []
    if "hupu_0_title" in api_data:
        item = {
            "title": api_data["hupu_0_title"],
            "url": api_data.get("hupu_0_url"),
        }
        hupu_items.append(item)
    hotspots["hupu"] = hupu_items[:limit]

    # 36Kr
    kr36_items = []
    if "kr36_0_title" in api_data:
        item = {
            "title": api_data["kr36_0_title"],
            "url": api_data.get("kr36_0_url"),
        }
        kr36_items.append(item)
    hotspots["kr36"] = kr36_items[:limit]

    # Bilibili
    bilibili_items = []
    if "bilibili_0_title" in api_data:
        item = {
            "title": api_data["bilibili_0_title"],
            "url": api_data.get("bilibili_0_url"),
        }
        bilibili_items.append(item)
    hotspots["bilibili"] = bilibili_items[:limit]

    # Zhihu
    zhihu_items = []
    if "zhihu_0_title" in api_data:
        item = {
            "title": api_data["zhihu_0_title"],
            "url": api_data.get("zhihu_0_url"),
        }
        zhihu_items.append(item)
    hotspots["zhihu"] = zhihu_items[:limit]

    # IT News
    it_news_items = []
    if "it_news_0_title" in api_data:
        item = {
            "title": api_data["it_news_0_title"],
        }
        if "it_news_0_summary" in api_data:
            item["summary"] = api_data["it_news_0_summary"]
        it_news_items.append(item)
    hotspots["it_news"] = it_news_items[:limit]

    # Huxiu
    huxiu_items = []
    if "huxiu_0_title" in api_data:
        item = {
            "title": api_data["huxiu_0_title"],
            "url": api_data.get("huxiu_0_url"),
        }
        huxiu_items.append(item)
    hotspots["huxiu"] = huxiu_items[:limit]

    # PMCAFE
    pmcafe_items = []
    if "pmcafe_0_title" in api_data:
        item = {
            "title": api_data["pmcafe_0_title"],
            "url": api_data.get("pmcafe_0_url"),
        }
        pmcafe_items.append(item)
    hotspots["pmcafe"] = pmcafe_items[:limit]

    # Baidu
    baidu_items = []
    if "baidu_0_title" in api_data:
        item = {
            "title": api_data["baidu_0_title"],
        }
        if "baidu_0_rank" in api_data:
            item["rank"] = api_data["baidu_0_rank"]
        baidu_items.append(item)
    hotspots["baidu"] = baidu_items[:limit]

    # Douyin
    douyin_items = []
    if "douyin_0_title" in api_data:
        item = {
            "title": api_data["douyin_0_title"],
        }
        if "douyin_0_summary" in api_data:
            item["summary"] = api_data["douyin_0_summary"]
        douyin_items.append(item)
    hotspots["douyin"] = douyin_items[:limit]

    # Douban
    douban_items = []
    if "douban_0_title" in api_data:
        item = {
            "title": api_data["douban_0_title"],
            "url": api_data.get("douban_0_url"),
        }
        douban_items.append(item)
    hotspots["douban"] = douban_items[:limit]

    return hotspots