def trends_hub_get_douyin_trending():
    """
    获取抖音热搜榜单，展示当下最热门的社会话题、娱乐事件、网络热点和流行趋势。

    Returns:
        Dict containing a list of trending topics with details such as title, event time, cover URL,
        popularity score, and link. The 'trending_items' key contains a list of dictionaries,
        each representing a trending topic.
    """
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API.

        Returns:
            Dict with simple fields only (str, int, float, bool):
            - trending_item_0_title (str): Title of the first trending topic
            - trending_item_0_event_time (str): Event time of the first trending topic
            - trending_item_0_cover_url (str): Cover image URL of the first trending topic
            - trending_item_0_popularity (int): Popularity score of the first trending topic
            - trending_item_0_link (str): Link to the first trending topic
            - trending_item_1_title (str): Title of the second trending topic
            - trending_item_1_event_time (str): Event time of the second trending topic
            - trending_item_1_cover_url (str): Cover image URL of the second trending topic
            - trending_item_1_popularity (int): Popularity score of the second trending topic
            - trending_item_1_link (str): Link to the second trending topic
        """
        return {
            "trending_item_0_title": "明星恋情曝光引发热议",
            "trending_item_0_event_time": "2025-04-05T10:30:00Z",
            "trending_item_0_cover_url": "https://example.com/cover1.jpg",
            "trending_item_0_popularity": 987654,
            "trending_item_0_link": "https://douyin.com/trend/1001",

            "trending_item_1_title": "新晋网红舞蹈挑战席卷全网",
            "trending_item_1_event_time": "2025-04-05T09:15:00Z",
            "trending_item_1_cover_url": "https://example.com/cover2.jpg",
            "trending_item_1_popularity": 876543,
            "trending_item_1_link": "https://douyin.com/trend/1002"
        }

    try:
        # Fetch simulated API data
        api_data = call_external_api("trends-hub-get-douyin-trending")

        # Construct the result structure according to output schema
        trending_items = [
            {
                "title": api_data["trending_item_0_title"],
                "event_time": api_data["trending_item_0_event_time"],
                "cover_url": api_data["trending_item_0_cover_url"],
                "popularity": api_data["trending_item_0_popularity"],
                "link": api_data["trending_item_0_link"]
            },
            {
                "title": api_data["trending_item_1_title"],
                "event_time": api_data["trending_item_1_event_time"],
                "cover_url": api_data["trending_item_1_cover_url"],
                "popularity": api_data["trending_item_1_popularity"],
                "link": api_data["trending_item_1_link"]
            }
        ]

        result = {
            "trending_items": trending_items
        }

        return result

    except KeyError as e:
        raise RuntimeError(f"Missing expected field in API response: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while processing trending data: {e}")