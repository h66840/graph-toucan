def leetcode_get_problem(titleSlug: str) -> dict:
    """
    Retrieves details about a specific LeetCode problem, including its description, examples, constraints, and related information.
    
    Args:
        titleSlug (str): The URL slug/identifier of the problem (e.g., 'two-sum', 'add-two-numbers') as it appears in the LeetCode URL
        
    Returns:
        Dict with the following keys:
        - titleSlug (str): URL slug identifier of the problem
        - problem (Dict): contains detailed information about the LeetCode problem including title, content, difficulty, tags, code templates, test cases, hints, and similar questions
          - problem['titleSlug'] (str): URL slug identifier
          - problem['questionId'] (str): unique question ID assigned by LeetCode
          - problem['title'] (str): full title of the problem
          - problem['content'] (str): HTML-formatted problem description
          - problem['difficulty'] (str): difficulty level ("Easy", "Medium", or "Hard")
          - problem['topicTags'] (List[str]): list of topic tags like "array", "sliding-window"
          - problem['codeSnippets'] (List[Dict]): list of code templates per language with keys 'lang', 'langSlug', 'code'
          - problem['exampleTestcases'] (str or Dict): example input test cases
          - problem['hints'] (List[str]): list of hint strings
          - problem['similarQuestions'] (List[Dict]): list of similar problems with 'titleSlug' and 'difficulty'
    """
    def call_external_api(tool_name: str) -> dict:
        """
        Simulates fetching data from external API for LeetCode problem.
        
        Returns:
            Dict with simple fields only (str, int, float, bool):
            - titleSlug (str): URL slug of the problem
            - problem_titleSlug (str): URL slug inside problem object
            - problem_questionId (str): unique question ID
            - problem_title (str): full title of the problem
            - problem_content (str): HTML-formatted problem description
            - problem_difficulty (str): difficulty level
            - problem_topicTags_0 (str): first topic tag
            - problem_topicTags_1 (str): second topic tag
            - problem_codeSnippets_0_lang (str): first code snippet language name
            - problem_codeSnippets_0_langSlug (str): first code snippet language slug
            - problem_codeSnippets_0_code (str): first code snippet starter code
            - problem_codeSnippets_1_lang (str): second code snippet language name
            - problem_codeSnippets_1_langSlug (str): second code snippet language slug
            - problem_codeSnippets_1_code (str): second code snippet starter code
            - problem_exampleTestcases (str): example test cases as string
            - problem_hints_0 (str): first hint
            - problem_hints_1 (str): second hint
            - problem_similarQuestions_0_titleSlug (str): first similar question slug
            - problem_similarQuestions_0_difficulty (str): first similar question difficulty
            - problem_similarQuestions_1_titleSlug (str): second similar question slug
            - problem_similarQuestions_1_difficulty (str): second similar question difficulty
        """
        return {
            "titleSlug": "two-sum",
            "problem_titleSlug": "two-sum",
            "problem_questionId": "1",
            "problem_title": "Two Sum",
            "problem_content": "<p>Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.</p>",
            "problem_difficulty": "Easy",
            "problem_topicTags_0": "array",
            "problem_topicTags_1": "hash-table",
            "problem_codeSnippets_0_lang": "Python3",
            "problem_codeSnippets_0_langSlug": "python3",
            "problem_codeSnippets_0_code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:",
            "problem_codeSnippets_1_lang": "Java",
            "problem_codeSnippets_1_langSlug": "java",
            "problem_codeSnippets_1_code": "public class Solution {\n    public int[] twoSum(int[] nums, int target) {",
            "problem_exampleTestcases": "nums = [2,7,11,15], target = 9",
            "problem_hints_0": "A really brute force way would be to check every pair of indices and see if they sum up to the target.",
            "problem_hints_1": "Use a hash map to store the value and its index for O(1) lookups.",
            "problem_similarQuestions_0_titleSlug": "4sum-ii",
            "problem_similarQuestions_0_difficulty": "Medium",
            "problem_similarQuestions_1_titleSlug": "subarray-sum-equals-k",
            "problem_similarQuestions_1_difficulty": "Medium"
        }

    # Input validation
    if not isinstance(titleSlug, str):
        raise TypeError("titleSlug must be a string")
    if not titleSlug.strip():
        raise ValueError("titleSlug cannot be empty or whitespace")

    # Call external API to get flattened data
    api_data = call_external_api("leetcode-get_problem")

    # Construct nested output structure from flat API data
    result = {
        "titleSlug": api_data["titleSlug"],
        "problem": {
            "titleSlug": api_data["problem_titleSlug"],
            "questionId": api_data["problem_questionId"],
            "title": api_data["problem_title"],
            "content": api_data["problem_content"],
            "difficulty": api_data["problem_difficulty"],
            "topicTags": [
                api_data["problem_topicTags_0"],
                api_data["problem_topicTags_1"]
            ],
            "codeSnippets": [
                {
                    "lang": api_data["problem_codeSnippets_0_lang"],
                    "langSlug": api_data["problem_codeSnippets_0_langSlug"],
                    "code": api_data["problem_codeSnippets_0_code"]
                },
                {
                    "lang": api_data["problem_codeSnippets_1_lang"],
                    "langSlug": api_data["problem_codeSnippets_1_langSlug"],
                    "code": api_data["problem_codeSnippets_1_code"]
                }
            ],
            "exampleTestcases": api_data["problem_exampleTestcases"],
            "hints": [
                api_data["problem_hints_0"],
                api_data["problem_hints_1"]
            ],
            "similarQuestions": [
                {
                    "titleSlug": api_data["problem_similarQuestions_0_titleSlug"],
                    "difficulty": api_data["problem_similarQuestions_0_difficulty"]
                },
                {
                    "titleSlug": api_data["problem_similarQuestions_1_titleSlug"],
                    "difficulty": api_data["problem_similarQuestions_1_difficulty"]
                }
            ]
        }
    }

    return result