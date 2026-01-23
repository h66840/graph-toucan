def leetcode_get_problem_solution(topicId: str) -> dict:
    """
    Retrieves the complete content and metadata of a specific solution, including the full article text,
    author information, and related navigation links.

    Args:
        topicId (str): The unique topic ID of the solution to retrieve. This ID can be obtained from
                       the 'topicId' field in the response of the 'list_problem_solutions' tool.
                       Format is typically a string of numbers and letters that uniquely identifies
                       the solution in LeetCode's database.

    Returns:
        dict: A dictionary containing detailed information about the solution with the following structure:
            - topicId (str): unique identifier of the solution topic
            - solution (dict):
                - title (str): title of the solution article
                - slug (str): URL-friendly slug identifying the solution
                - content (str): full text content of the solution, including explanations, code snippets,
                                 and formatting in plain text with escaped characters like \\n and \\t
                - tags (list[dict]): list of tag objects associated with the solution, each containing a 'slug'
                - topic (dict):
                    - id (int): numeric ID of the current solution topic
                - prev (dict or None): previous solution in navigation order; contains 'slug' and 'topicId' if exists
                - next (dict or None): next solution in navigation order; contains 'slug' and 'topicId' if exists
    """
    if not isinstance(topicId, str) or not topicId.strip():
        raise ValueError("topicId must be a non-empty string")

    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API for retrieving problem solution details.

        Returns:
            Dict with simple scalar fields only (str, int, float, bool), representing flattened version
            of nested output schema:
            - topicId (str): Unique identifier of the solution topic
            - solution_title (str): Title of the solution article
            - solution_slug (str): URL-friendly slug identifying the solution
            - solution_content (str): Full text content of the solution
            - solution_tags_0_slug (str): First tag slug (e.g., 'dynamic-programming')
            - solution_tags_1_slug (str): Second tag slug (e.g., 'java')
            - solution_topic_id (int): Numeric ID of the current solution topic
            - solution_prev_slug (str): Slug of the previous solution in navigation
            - solution_prev_topicId (str): Topic ID of the previous solution
            - solution_next_slug (str): Slug of the next solution in navigation
            - solution_next_topicId (str): Topic ID of the next solution
        """
        return {
            "topicId": "12345abcde",
            "solution_title": "Two Sum Solution",
            "solution_slug": "two-sum-solution",
            "solution_content": "This article explains how to solve the Two Sum problem using hash map technique.\\nTime Complexity: O(n)\\nSpace Complexity: O(n)\\n\\nExample code:\\n```python\\ndef two_sum(nums, target):\\n    num_map = {}\\n    for i, num in enumerate(nums):\\n        complement = target - num\\n        if complement in num_map:\\n            return [num_map[complement], i]\\n        num_map[num] = i\\n```",
            "solution_tags_0_slug": "hash-table",
            "solution_tags_1_slug": "python",
            "solution_topic_id": 67890,
            "solution_prev_slug": "reverse-linked-list",
            "solution_prev_topicId": "6789fghij",
            "solution_next_slug": "three-sum-solution",
            "solution_next_topicId": "23456klmno"
        }

    try:
        # Fetch simulated API data with flat structure
        api_data = call_external_api("leetcode-get_problem_solution")

        # Construct nested output structure as per schema
        result = {
            "topicId": api_data["topicId"],
            "solution": {
                "title": api_data["solution_title"],
                "slug": api_data["solution_slug"],
                "content": api_data["solution_content"],
                "tags": [
                    {"slug": api_data["solution_tags_0_slug"]},
                    {"slug": api_data["solution_tags_1_slug"]}
                ],
                "topic": {
                    "id": api_data["solution_topic_id"]
                },
                "prev": {
                    "slug": api_data["solution_prev_slug"],
                    "topicId": api_data["solution_prev_topicId"]
                } if api_data["solution_prev_slug"] and api_data["solution_prev_topicId"] else None,
                "next": {
                    "slug": api_data["solution_next_slug"],
                    "topicId": api_data["solution_next_topicId"]
                } if api_data["solution_next_slug"] and api_data["solution_next_topicId"] else None
            }
        }

        return result

    except Exception as e:
        raise RuntimeError(f"Failed to retrieve solution for topicId '{topicId}': {str(e)}")