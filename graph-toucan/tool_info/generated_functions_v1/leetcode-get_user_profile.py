from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LeetCode user profile.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - username (str): LeetCode username of the user
        - profile_username (str): Username displayed on profile
        - profile_realName (str): Real or display name of the user
        - profile_userAvatar (str): URL to the user's avatar image
        - profile_countryName (str or None): Country associated with the user
        - profile_githubUrl (str or None): GitHub profile URL if provided
        - profile_company (str or None): Current company the user works at
        - profile_school (str or None): Educational institution attended
        - profile_ranking (int): Global ranking of the user on LeetCode
        - profile_totalSubmissionNum_0_difficulty (str): First submission difficulty level
        - profile_totalSubmissionNum_0_count (int): Number of solved problems for first difficulty
        - profile_totalSubmissionNum_0_submissions (int): Total submission attempts for first difficulty
        - profile_totalSubmissionNum_1_difficulty (str): Second submission difficulty level
        - profile_totalSubmissionNum_1_count (int): Number of solved problems for second difficulty
        - profile_totalSubmissionNum_1_submissions (int): Total submission attempts for second difficulty
    """
    return {
        "username": "johndoe",
        "profile_username": "johndoe",
        "profile_realName": "John Doe",
        "profile_userAvatar": "https://assets.leetcode.com/users/johndoe/avatar_123.png",
        "profile_countryName": "United States",
        "profile_githubUrl": "https://github.com/johndoe",
        "profile_company": "Google",
        "profile_school": "Stanford University",
        "profile_ranking": 4567,
        "profile_totalSubmissionNum_0_difficulty": "Easy",
        "profile_totalSubmissionNum_0_count": 150,
        "profile_totalSubmissionNum_0_submissions": 200,
        "profile_totalSubmissionNum_1_difficulty": "Medium",
        "profile_totalSubmissionNum_1_count": 85,
        "profile_totalSubmissionNum_1_submissions": 180,
    }

def leetcode_get_user_profile(username: str) -> Dict[str, Any]:
    """
    Retrieves profile information about a LeetCode user, including user stats, solved problems, and profile details.

    Args:
        username (str): LeetCode username to retrieve profile information for

    Returns:
        Dict containing:
        - username (str): LeetCode username of the user
        - profile (Dict): contains detailed profile information including real name, avatar URL, ranking, and submission statistics
          with keys:
          - username (str): username displayed on profile
          - realName (str): real or display name of the user
          - userAvatar (str): URL to the user's avatar image
          - countryName (str or None): country associated with the user
          - githubUrl (str or None): GitHub profile URL if provided
          - company (str or None): current company the user works at
          - school (str or None): educational institution attended
          - ranking (int): global ranking of the user on LeetCode
          - totalSubmissionNum (List[Dict]): list of submission counts grouped by difficulty; each dict contains
            'difficulty', 'count', and 'submissions'

    Raises:
        ValueError: If username is empty or None
    """
    if not username:
        raise ValueError("Username is required")

    # Fetch data from external API (simulated)
    api_data = call_external_api("leetcode-get_user_profile")

    # Construct totalSubmissionNum list from indexed fields
    total_submission_num = [
        {
            "difficulty": api_data["profile_totalSubmissionNum_0_difficulty"],
            "count": api_data["profile_totalSubmissionNum_0_count"],
            "submissions": api_data["profile_totalSubmissionNum_0_submissions"]
        },
        {
            "difficulty": api_data["profile_totalSubmissionNum_1_difficulty"],
            "count": api_data["profile_totalSubmissionNum_1_count"],
            "submissions": api_data["profile_totalSubmissionNum_1_submissions"]
        }
    ]

    # Construct profile dictionary
    profile = {
        "username": api_data["profile_username"],
        "realName": api_data["profile_realName"],
        "userAvatar": api_data["profile_userAvatar"],
        "countryName": api_data["profile_countryName"],
        "githubUrl": api_data["profile_githubUrl"],
        "company": api_data["profile_company"],
        "school": api_data["profile_school"],
        "ranking": api_data["profile_ranking"],
        "totalSubmissionNum": total_submission_num
    }

    # Construct final result
    result = {
        "username": api_data["username"],
        "profile": profile
    }

    return result