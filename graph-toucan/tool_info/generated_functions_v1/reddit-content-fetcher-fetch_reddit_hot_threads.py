from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Reddit hot threads.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - post_0_title (str): Title of the first post
        - post_0_score (int): Score (upvotes) of the first post
        - post_0_comments (int): Number of comments on the first post
        - post_0_author (str): Author username of the first post
        - post_0_type (str): Type of content in the first post (e.g., text, link)
        - post_0_content (str): Content/body of the first post
        - post_0_link (str): URL link to the first post
        - post_1_title (str): Title of the second post
        - post_1_score (int): Score (upvotes) of the second post
        - post_1_comments (int): Number of comments on the second post
        - post_1_author (str): Author username of the second post
        - post_1_type (str): Type of content in the second post (e.g., text, link)
        - post_1_content (str): Content/body of the second post
        - post_1_link (str): URL link to the second post
    """
    return {
        "post_0_title": "Why Reddit is the best platform for discussions",
        "post_0_score": 1542,
        "post_0_comments": 234,
        "post_0_author": "user_redditor123",
        "post_0_type": "text",
        "post_0_content": "This is a detailed explanation of why Reddit stands out among social platforms due to its community-driven nature.",
        "post_0_link": "https://www.reddit.com/r/RedditDiscussion/comments/abc123/why_reddit_is_the_best/",
        "post_1_title": "Check out this amazing Python trick!",
        "post_1_score": 987,
        "post_1_comments": 89,
        "post_1_author": "python_enthusiast",
        "post_1_type": "link",
        "post_1_content": "A short description of a cool Python feature involving context managers and decorators.",
        "post_1_link": "https://www.reddit.com/r/Python/comments/def456/check_out_this_amazing_python_trick/"
    }

def reddit_content_fetcher_fetch_reddit_hot_threads(subreddit: str, limit: Optional[int] = 10) -> Dict[str, Any]:
    """
    Fetch hot threads from a subreddit.
    
    Args:
        subreddit (str): Name of the subreddit (required)
        limit (int, optional): Number of posts to fetch (default: 10). Maximum of 2 simulated posts.
        
    Returns:
        Dict containing a list of post objects with keys:
            - posts (List[Dict]): list of post dictionaries containing 
              'title', 'score', 'comments', 'author', 'type', 'content', 'link' fields
    
    Raises:
        ValueError: If subreddit is empty or None
    """
    if not subreddit or not subreddit.strip():
        raise ValueError("Subreddit name is required and cannot be empty.")
    
    if limit is None:
        limit = 10
    
    # Clamp limit to maximum available simulated posts (2)
    effective_limit = min(limit, 2)
    
    # Fetch simulated data from external API
    api_data = call_external_api("reddit-content-fetcher-fetch_reddit_hot_threads")
    
    # Construct the list of posts from flattened API response
    posts: List[Dict[str, Any]] = []
    
    for i in range(effective_limit):
        post_key_prefix = f"post_{i}"
        try:
            post = {
                "title": api_data[f"{post_key_prefix}_title"],
                "score": api_data[f"{post_key_prefix}_score"],
                "comments": api_data[f"{post_key_prefix}_comments"],
                "author": api_data[f"{post_key_prefix}_author"],
                "type": api_data[f"{post_key_prefix}_type"],
                "content": api_data[f"{post_key_prefix}_content"],
                "link": api_data[f"{post_key_prefix}_link"]
            }
            posts.append(post)
        except KeyError as e:
            # In case some expected field is missing in simulation
            raise RuntimeError(f"Simulated data missing expected field: {e}")
    
    return {
        "posts": posts
    }