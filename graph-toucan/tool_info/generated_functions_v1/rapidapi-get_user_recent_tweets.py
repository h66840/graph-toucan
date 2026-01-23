from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for getting user recent tweets.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - tweet_0_tweet_id (str): ID of the first tweet
        - tweet_0_created_at (str): Creation timestamp of the first tweet
        - tweet_0_text (str): Text content of the first tweet
        - tweet_0_favorites (int): Number of favorites for the first tweet
        - tweet_0_bookmarks (int): Number of bookmarks for the first tweet
        - tweet_0_quotes (int): Number of quote tweets for the first tweet
        - tweet_0_views (int): Number of views for the first tweet
        - tweet_0_prev_cursor (str): Previous cursor for pagination of the first tweet
        - tweet_0_next_cursor (str): Next cursor for pagination of the first tweet
        - tweet_1_tweet_id (str): ID of the second tweet
        - tweet_1_created_at (str): Creation timestamp of the second tweet
        - tweet_1_text (str): Text content of the second tweet
        - tweet_1_favorites (int): Number of favorites for the second tweet
        - tweet_1_bookmarks (int): Number of bookmarks for the second tweet
        - tweet_1_quotes (int): Number of quote tweets for the second tweet
        - tweet_1_views (int): Number of views for the second tweet
        - tweet_1_prev_cursor (str): Previous cursor for pagination of the second tweet
        - tweet_1_next_cursor (str): Next cursor for pagination of the second tweet
    """
    return {
        "tweet_0_tweet_id": "1598374629102745601",
        "tweet_0_created_at": "2023-10-15T08:30:22Z",
        "tweet_0_text": "Just had the best coffee to start the day! #morningvibes",
        "tweet_0_favorites": 24,
        "tweet_0_bookmarks": 5,
        "tweet_0_quotes": 2,
        "tweet_0_views": 312,
        "tweet_0_prev_cursor": "prev_123",
        "tweet_0_next_cursor": "next_456",
        "tweet_1_tweet_id": "1598374123456789002",
        "tweet_1_created_at": "2023-10-14T19:15:47Z",
        "tweet_1_text": "Finished reading an amazing book about space exploration 🚀",
        "tweet_1_favorites": 41,
        "tweet_1_bookmarks": 8,
        "tweet_1_quotes": 3,
        "tweet_1_views": 567,
        "tweet_1_prev_cursor": "prev_789",
        "tweet_1_next_cursor": "next_012"
    }

def rapidapi_get_user_recent_tweets(username: str) -> Dict[str, Any]:
    """
    Fetches recent tweets for a given Twitter username using RapidAPI.
    
    Args:
        username (str): The Twitter username to fetch recent tweets for. Required.
    
    Returns:
        Dict containing a list of tweet objects with fields:
        - tweets (List[Dict]): List of tweet dictionaries containing:
            - tweet_id (str)
            - created_at (str)
            - text (str)
            - favorites (int)
            - bookmarks (int)
            - quotes (int)
            - views (int)
            - prev_cursor (str)
            - next_cursor (str)
    
    Raises:
        ValueError: If username is empty or not provided
    """
    if not username or not username.strip():
        raise ValueError("Username is required and cannot be empty")
    
    username = username.strip()
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("rapidapi-get_user_recent_tweets")
    
    # Construct tweets list from flattened API data
    tweets = [
        {
            "tweet_id": api_data["tweet_0_tweet_id"],
            "created_at": api_data["tweet_0_created_at"],
            "text": api_data["tweet_0_text"],
            "favorites": api_data["tweet_0_favorites"],
            "bookmarks": api_data["tweet_0_bookmarks"],
            "quotes": api_data["tweet_0_quotes"],
            "views": api_data["tweet_0_views"],
            "prev_cursor": api_data["tweet_0_prev_cursor"],
            "next_cursor": api_data["tweet_0_next_cursor"]
        },
        {
            "tweet_id": api_data["tweet_1_tweet_id"],
            "created_at": api_data["tweet_1_created_at"],
            "text": api_data["tweet_1_text"],
            "favorites": api_data["tweet_1_favorites"],
            "bookmarks": api_data["tweet_1_bookmarks"],
            "quotes": api_data["tweet_1_quotes"],
            "views": api_data["tweet_1_views"],
            "prev_cursor": api_data["tweet_1_prev_cursor"],
            "next_cursor": api_data["tweet_1_next_cursor"]
        }
    ]
    
    return {
        "tweets": tweets
    }