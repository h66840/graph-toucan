from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LeetCode problem solutions.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - questionSlug (str): URL slug of the LeetCode problem
        - solutionArticles_totalNum (int): Total number of community solutions available
        - solutionArticles_hasNextPage (bool): Whether more solutions are available beyond current batch
        - solutionArticles_articles_0_title (str): Title of first solution article
        - solutionArticles_articles_0_topicId (int): Unique identifier for first solution article
        - solutionArticles_articles_0_slug (str): URL-friendly identifier for first solution article
        - solutionArticles_articles_0_summary (str): Brief excerpt of first solution content
        - solutionArticles_articles_0_articleUrl (str): Full URL to first solution on LeetCode
        - solutionArticles_articles_0_canSee (bool): Whether user can view full first article
        - solutionArticles_articles_0_hasVideoArticle (bool): Whether first solution has video explanation
        - solutionArticles_articles_1_title (str): Title of second solution article
        - solutionArticles_articles_1_topicId (int): Unique identifier for second solution article
        - solutionArticles_articles_1_slug (str): URL-friendly identifier for second solution article
        - solutionArticles_articles_1_summary (str): Brief excerpt of second solution content
        - solutionArticles_articles_1_articleUrl (str): Full URL to second solution on LeetCode
        - solutionArticles_articles_1_canSee (bool): Whether user can view full second article
        - solutionArticles_articles_1_hasVideoArticle (bool): Whether second solution has video explanation
    """
    return {
        "questionSlug": "two-sum",
        "solutionArticles_totalNum": 156,
        "solutionArticles_hasNextPage": True,
        "solutionArticles_articles_0_title": "Simple Python Solution Using Hash Map",
        "solutionArticles_articles_0_topicId": 12345,
        "solutionArticles_articles_0_slug": "simple-python-solution-using-hash-map",
        "solutionArticles_articles_0_summary": "This solution uses a hash map to find two numbers that add up to target in O(n) time.",
        "solutionArticles_articles_0_articleUrl": "https://leetcode.com/problems/two-sum/solutions/12345/simple-python-solution-using-hash-map/",
        "solutionArticles_articles_0_canSee": True,
        "solutionArticles_articles_0_hasVideoArticle": False,
        "solutionArticles_articles_1_title": "Java Two Pointer Approach with Sorting",
        "solutionArticles_articles_1_topicId": 12346,
        "solutionArticles_articles_1_slug": "java-two-pointer-approach-with-sorting",
        "solutionArticles_articles_1_summary": "Sorts array first then applies two pointers technique. Time complexity O(n log n).",
        "solutionArticles_articles_1_articleUrl": "https://leetcode.com/problems/two-sum/solutions/12346/java-two-pointer-approach-with-sorting/",
        "solutionArticles_articles_1_canSee": True,
        "solutionArticles_articles_1_hasVideoArticle": True,
    }

def leetcode_list_problem_solutions(
    questionSlug: str,
    limit: Optional[int] = 20,
    orderBy: Optional[str] = None,
    skip: Optional[int] = 0,
    tagSlugs: Optional[List[str]] = None,
    userInput: Optional[str] = None
) -> Dict[str, Any]:
    """
    Retrieves a list of community solutions for a specific LeetCode problem, including only metadata like topicId.
    To view the full content of a solution, use the 'get_problem_solution' tool with the topicId returned by this tool.

    Args:
        questionSlug (str): The URL slug/identifier of the problem to retrieve solutions for (e.g., 'two-sum', 'add-two-numbers').
        limit (int, optional): Maximum number of solutions to return per request. Default is 20.
        orderBy (str, optional): Sorting criteria: 'DEFAULT', 'MOST_VOTES', or 'MOST_RECENT'.
        skip (int, optional): Number of solutions to skip before starting to collect results. Default is 0.
        tagSlugs (List[str], optional): Array of tag identifiers to filter solutions by programming languages or topics.
        userInput (str, optional): Search term to filter solutions by title, content, or author name.

    Returns:
        Dict containing:
        - questionSlug (str): URL slug of the LeetCode problem
        - solutionArticles (Dict): Contains pagination info and list of solution articles with metadata:
            - totalNum (int): Total number of community solutions available
            - hasNextPage (bool): Whether more solutions are available beyond current batch
            - articles (List[Dict]): List of solution article metadata entries containing:
                - title (str): Title of the solution article
                - topicId (int): Unique identifier for the solution article
                - slug (str): URL-friendly identifier for the solution article
                - summary (str): Brief excerpt of the solution content
                - articleUrl (str): Full URL to the solution on LeetCode
                - canSee (bool): Whether the user has permission to view the full article
                - hasVideoArticle (bool): Whether the solution includes a video explanation

    Raises:
        ValueError: If limit is not a positive integer or skip is negative.
    """
    # Input validation
    if limit is not None:
        if not isinstance(limit, int) or limit <= 0:
            raise ValueError("limit must be a positive integer")
    
    if skip is not None:
        if not isinstance(skip, int) or skip < 0:
            raise ValueError("skip must be a non-negative integer")

    if not questionSlug or not isinstance(questionSlug, str):
        raise ValueError("questionSlug is required and must be a non-empty string")

    # Call external API to get flattened data
    api_data = call_external_api("leetcode-list_problem_solutions")

    # Construct nested structure matching output schema
    result = {
        "questionSlug": questionSlug,
        "solutionArticles": {
            "totalNum": api_data["solutionArticles_totalNum"],
            "hasNextPage": api_data["solutionArticles_hasNextPage"],
            "articles": [
                {
                    "title": api_data["solutionArticles_articles_0_title"],
                    "topicId": api_data["solutionArticles_articles_0_topicId"],
                    "slug": api_data["solutionArticles_articles_0_slug"],
                    "summary": api_data["solutionArticles_articles_0_summary"],
                    "articleUrl": api_data["solutionArticles_articles_0_articleUrl"],
                    "canSee": api_data["solutionArticles_articles_0_canSee"],
                    "hasVideoArticle": api_data["solutionArticles_articles_0_hasVideoArticle"]
                },
                {
                    "title": api_data["solutionArticles_articles_1_title"],
                    "topicId": api_data["solutionArticles_articles_1_topicId"],
                    "slug": api_data["solutionArticles_articles_1_slug"],
                    "summary": api_data["solutionArticles_articles_1_summary"],
                    "articleUrl": api_data["solutionArticles_articles_1_articleUrl"],
                    "canSee": api_data["solutionArticles_articles_1_canSee"],
                    "hasVideoArticle": api_data["solutionArticles_articles_1_hasVideoArticle"]
                }
            ]
        }
    }

    return result