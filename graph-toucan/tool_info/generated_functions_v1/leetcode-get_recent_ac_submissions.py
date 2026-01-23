from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching recent accepted submissions data from LeetCode API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - username (str): LeetCode username for which submissions are retrieved
        - recent_ac_submissions_0_id (int): ID of the first accepted submission
        - recent_ac_submissions_0_title (str): Title of the first accepted submission
        - recent_ac_submissions_0_title_slug (str): URL-friendly title slug of the first submission
        - recent_ac_submissions_0_timestamp (int): Unix timestamp of the first submission
        - recent_ac_submissions_0_time_display (str): Human-readable time display of the first submission
        - recent_ac_submissions_0_language (str): Programming language used in the first submission
        - recent_ac_submissions_1_id (int): ID of the second accepted submission
        - recent_ac_submissions_1_title (str): Title of the second accepted submission
        - recent_ac_submissions_1_title_slug (str): URL-friendly title slug of the second submission
        - recent_ac_submissions_1_timestamp (int): Unix timestamp of the second submission
        - recent_ac_submissions_1_time_display (str): Human-readable time display of the second submission
        - recent_ac_submissions_1_language (str): Programming language used in the second submission
    """
    return {
        "username": "leetcode_user_123",
        "recent_ac_submissions_0_id": 1001,
        "recent_ac_submissions_0_title": "Two Sum",
        "recent_ac_submissions_0_title_slug": "two-sum",
        "recent_ac_submissions_0_timestamp": 1700000000,
        "recent_ac_submissions_0_time_display": "a few seconds ago",
        "recent_ac_submissions_0_language": "python3",
        "recent_ac_submissions_1_id": 1002,
        "recent_ac_submissions_1_title": "Add Two Numbers",
        "recent_ac_submissions_1_title_slug": "add-two-numbers",
        "recent_ac_submissions_1_timestamp": 1699999000,
        "recent_ac_submissions_1_time_display": "17 minutes ago",
        "recent_ac_submissions_1_language": "java"
    }

def leetcode_get_recent_ac_submissions(username: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieves a user's recent accepted (AC) submissions on LeetCode Global, focusing only on successfully completed problems.
    
    Args:
        username (str): LeetCode username to retrieve recent accepted submissions for
        limit (Optional[int]): Maximum number of accepted submissions to return (optional, defaults to server-defined limit)
    
    Returns:
        Dict containing:
        - username (str): LeetCode username for which submissions are retrieved
        - recent_ac_submissions (List[Dict]): list of accepted submissions, each containing 'id', 'title', 
          'title_slug', 'timestamp', 'time_display', 'language' fields
    
    Raises:
        ValueError: If username is empty or invalid
    """
    if not username or not username.strip():
        raise ValueError("Username is required and cannot be empty")
    
    # Call external API to get flattened data
    api_data = call_external_api("leetcode-get_recent_ac_submissions")
    
    # Validate that the returned data matches expected username
    if api_data.get("username") != username:
        # Simulate realistic behavior: if user not found, return empty list
        return {
            "username": username,
            "recent_ac_submissions": []
        }
    
    # Construct recent_ac_submissions list from flattened API data
    recent_ac_submissions: List[Dict[str, Any]] = []
    
    # Process first submission if available
    if "recent_ac_submissions_0_id" in api_data:
        recent_ac_submissions.append({
            "id": api_data["recent_ac_submissions_0_id"],
            "title": api_data["recent_ac_submissions_0_title"],
            "title_slug": api_data["recent_ac_submissions_0_title_slug"],
            "timestamp": api_data["recent_ac_submissions_0_timestamp"],
            "time_display": api_data["recent_ac_submissions_0_time_display"],
            "language": api_data["recent_ac_submissions_0_language"]
        })
    
    # Process second submission if available
    if "recent_ac_submissions_1_id" in api_data:
        recent_ac_submissions.append({
            "id": api_data["recent_ac_submissions_1_id"],
            "title": api_data["recent_ac_submissions_1_title"],
            "title_slug": api_data["recent_ac_submissions_1_title_slug"],
            "timestamp": api_data["recent_ac_submissions_1_timestamp"],
            "time_display": api_data["recent_ac_submissions_1_time_display"],
            "language": api_data["recent_ac_submissions_1_language"]
        })
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        recent_ac_submissions = recent_ac_submissions[:limit]
    
    return {
        "username": username,
        "recent_ac_submissions": recent_ac_submissions
    }