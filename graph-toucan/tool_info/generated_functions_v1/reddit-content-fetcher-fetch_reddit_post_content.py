from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Reddit post content.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - title (str): Title of the Reddit post
        - score (int): Upvote score of the post
        - author (str): Username of the post author
        - post_type (str): Type of the post ("link" or "text")
        - content_url (str): URL to the full post on Reddit
        - comment_0_author (str): Author of the first top-level comment
        - comment_0_score (int): Score of the first top-level comment
        - comment_0_text (str): Text content of the first top-level comment
        - comment_0_reply_0_author (str): Author of first reply to first comment
        - comment_0_reply_0_score (int): Score of first reply to first comment
        - comment_0_reply_0_text (str): Text of first reply to first comment
        - comment_1_author (str): Author of the second top-level comment
        - comment_1_score (int): Score of the second top-level comment
        - comment_1_text (str): Text content of the second top-level comment
        - comment_1_reply_0_author (str): Author of first reply to second comment
        - comment_1_reply_0_score (int): Score of first reply to second comment
        - comment_1_reply_0_text (str): Text of first reply to second comment
    """
    return {
        "title": "Why Python is the best programming language",
        "score": 1250,
        "author": "python_enthusiast",
        "post_type": "text",
        "content_url": "https://www.reddit.com/r/Python/comments/abc123/why_python_is_the_best/",
        "comment_0_author": "code_novice",
        "comment_0_score": 45,
        "comment_0_text": "I agree! Python's syntax is so clean and readable.",
        "comment_0_reply_0_author": "dev_guru",
        "comment_0_reply_0_score": 12,
        "comment_0_reply_0_text": "True, but don't forget about performance trade-offs.",
        "comment_1_author": "rust_advocate",
        "comment_1_score": 30,
        "comment_1_text": "Rust is better for systems programming though.",
        "comment_1_reply_0_author": "python_enthusiast",
        "comment_1_reply_0_score": 25,
        "comment_1_reply_0_text": "Agreed! Different tools for different jobs."
    }

def reddit_content_fetcher_fetch_reddit_post_content(
    post_id: str,
    comment_limit: Optional[int] = 10,
    comment_depth: Optional[int] = 2
) -> Dict[str, Any]:
    """
    Fetch detailed content of a specific Reddit post including top-level comments and nested replies.

    Args:
        post_id (str): Reddit post ID (required)
        comment_limit (int, optional): Number of top-level comments to fetch. Defaults to 10.
        comment_depth (int, optional): Maximum depth of comment tree to traverse. Defaults to 2.

    Returns:
        Dict containing:
            - title (str): title of the Reddit post
            - score (int): upvote score of the post
            - author (str): username of the post author
            - post_type (str): type of the post ("link" or "text")
            - content_url (str): URL to the full post on Reddit
            - comments (List[Dict]): list of top-level comments, each with 'author', 'score', and 'text' fields;
              may contain nested replies up to specified depth

    Raises:
        ValueError: If post_id is empty or None
    """
    if not post_id or not post_id.strip():
        raise ValueError("post_id is required and cannot be empty")

    # Fetch data from simulated external API
    api_data = call_external_api("reddit-content-fetcher-fetch_reddit_post_content")

    # Construct comments with nested replies based on comment_depth
    comments = []

    # Process first comment
    if "comment_0_text" in api_data and api_data["comment_0_text"]:
        comment_0 = {
            "author": api_data["comment_0_author"],
            "score": api_data["comment_0_score"],
            "text": api_data["comment_0_text"]
        }
        # Add replies if depth allows and reply data exists
        if comment_depth > 1 and "comment_0_reply_0_text" in api_data and api_data["comment_0_reply_0_text"]:
            comment_0["replies"] = [{
                "author": api_data["comment_0_reply_0_author"],
                "score": api_data["comment_0_reply_0_score"],
                "text": api_data["comment_0_reply_0_text"]
            }]
        comments.append(comment_0)

    # Process second comment
    if "comment_1_text" in api_data and api_data["comment_1_text"]:
        comment_1 = {
            "author": api_data["comment_1_author"],
            "score": api_data["comment_1_score"],
            "text": api_data["comment_1_text"]
        }
        # Add replies if depth allows and reply data exists
        if comment_depth > 1 and "comment_1_reply_0_text" in api_data and api_data["comment_1_reply_0_text"]:
            comment_1["replies"] = [{
                "author": api_data["comment_1_reply_0_author"],
                "score": api_data["comment_1_reply_0_score"],
                "text": api_data["comment_1_reply_0_text"]
            }]
        comments.append(comment_1)

    # Apply comment limit
    limited_comments = comments[:min(comment_limit or 10, len(comments))]

    # Construct final result matching output schema
    result = {
        "title": api_data["title"],
        "score": api_data["score"],
        "author": api_data["author"],
        "post_type": api_data["post_type"],
        "content_url": api_data["content_url"],
        "comments": limited_comments
    }

    return result