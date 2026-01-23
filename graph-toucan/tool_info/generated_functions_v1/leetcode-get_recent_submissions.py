from typing import Dict, List, Any, Optional
from datetime import datetime


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LeetCode recent submissions.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - username (str): LeetCode username for which submissions were retrieved
        - total_count (int): Total number of recent submissions available
        - retrieval_timestamp (str): ISO 8601 timestamp when data was fetched
        - has_more (bool): Whether more submissions exist beyond limit
        - submission_0_title (str): Title of first submission
        - submission_0_slug (str): URL-friendly identifier of first problem
        - submission_0_status (str): Status of first submission (e.g., "Accepted")
        - submission_0_runtime (str): Runtime of first submission (e.g., "3 ms")
        - submission_0_memory (str): Memory usage of first submission (e.g., "42.1 MB")
        - submission_0_language (str): Programming language used in first submission
        - submission_0_timestamp (str): ISO 8601 timestamp of first submission
        - submission_0_url (str): Direct link to first submission
        - submission_0_difficulty (str): Difficulty level of first problem ("Easy", "Medium", "Hard")
        - submission_1_title (str): Title of second submission
        - submission_1_slug (str): URL-friendly identifier of second problem
        - submission_1_status (str): Status of second submission
        - submission_1_runtime (str): Runtime of second submission
        - submission_1_memory (str): Memory usage of second submission
        - submission_1_language (str): Programming language used in second submission
        - submission_1_timestamp (str): ISO 8601 timestamp of second submission
        - submission_1_url (str): Direct link to second submission
        - submission_1_difficulty (str): Difficulty level of second problem
    """
    return {
        "username": "johndoe",
        "total_count": 42,
        "retrieval_timestamp": datetime.now().isoformat(),
        "has_more": True,
        "submission_0_title": "Two Sum",
        "submission_0_slug": "two-sum",
        "submission_0_status": "Accepted",
        "submission_0_runtime": "3 ms",
        "submission_0_memory": "42.1 MB",
        "submission_0_language": "Python3",
        "submission_0_timestamp": "2023-10-05T08:30:00Z",
        "submission_0_url": "https://leetcode.com/submissions/detail/123456789/",
        "submission_0_difficulty": "Easy",
        "submission_1_title": "Add Two Numbers",
        "submission_1_slug": "add-two-numbers",
        "submission_1_status": "Wrong Answer",
        "submission_1_runtime": "12 ms",
        "submission_1_memory": "14.3 MB",
        "submission_1_language": "Java",
        "submission_1_timestamp": "2023-10-04T16:45:22Z",
        "submission_1_url": "https://leetcode.com/submissions/detail/123456788/",
        "submission_1_difficulty": "Medium"
    }


def leetcode_get_recent_submissions(username: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Retrieves a user's recent submissions on LeetCode Global, including both accepted and failed submissions with detailed metadata.

    Args:
        username (str): LeetCode username to retrieve recent submissions for (required)
        limit (Optional[int]): Maximum number of submissions to return (optional, defaults to server-defined limit)

    Returns:
        Dict containing:
        - submissions (List[Dict]): List of submission objects with detailed metadata
        - total_count (int): Total number of recent submissions available for the user
        - username (str): LeetCode username for which submissions were retrieved
        - retrieval_timestamp (str): ISO 8601 timestamp indicating when the data was fetched
        - has_more (bool): Indicates whether more submissions are available beyond the current limit

        Each submission dict contains:
        - title (str): Problem title
        - slug (str): URL-friendly problem identifier
        - status (str): Submission status ("Accepted", "Wrong Answer", etc.)
        - runtime (str): Runtime performance (e.g., "3 ms"), may be None
        - memory (str): Memory usage (e.g., "42.1 MB"), may be None
        - language (str): Programming language used (e.g., "Python3")
        - timestamp (str): ISO 8601 timestamp of submission
        - url (str): Direct link to the submission on LeetCode
        - difficulty (str): Problem difficulty ("Easy", "Medium", "Hard")

    Raises:
        ValueError: If username is empty or None
    """
    if not username:
        raise ValueError("Username is required")

    # Fetch data from external API (simulated)
    api_data = call_external_api("leetcode-get_recent_submissions")

    # Construct submissions list from indexed fields
    submissions = []
    for i in range(2):  # We have 2 submissions from the API response
        title_key = f"submission_{i}_title"
        if title_key not in api_data:
            break

        submission = {
            "title": api_data[f"submission_{i}_title"],
            "slug": api_data[f"submission_{i}_slug"],
            "status": api_data[f"submission_{i}_status"],
            "runtime": api_data[f"submission_{i}_runtime"],
            "memory": api_data[f"submission_{i}_memory"],
            "language": api_data[f"submission_{i}_language"],
            "timestamp": api_data[f"submission_{i}_timestamp"],
            "url": api_data[f"submission_{i}_url"],
            "difficulty": api_data[f"submission_{i}_difficulty"]
        }
        submissions.append(submission)

    # Apply limit if specified
    if limit is not None and limit > 0:
        submissions = submissions[:limit]

    # Construct final result matching output schema
    result = {
        "submissions": submissions,
        "total_count": api_data["total_count"],
        "username": api_data["username"],
        "retrieval_timestamp": api_data["retrieval_timestamp"],
        "has_more": api_data["has_more"]
    }

    return result