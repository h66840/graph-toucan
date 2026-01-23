def call_external_api(tool_name: str) -> dict:
    """
    Simulates fetching data from external API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - date (str): the date of the daily challenge in YYYY-MM-DD format
        - problem_link (str): relative URL path to the problem on LeetCode
        - problem_title (str): title of the coding problem
        - problem_title_slug (str): URL-friendly slug version of the problem title
        - problem_difficulty (str): difficulty level of the problem (e.g., "Easy", "Medium", "Hard")
        - problem_description (str): HTML-formatted description of the problem including examples and constraints
        - problem_constraints_0 (str): first constraint string
        - problem_constraints_1 (str): second constraint string
        - problem_examples_0_input (str): input for first example case
        - problem_examples_0_output (str): output for first example case
        - problem_examples_0_explanation (str): explanation for first example case
        - problem_examples_1_input (str): input for second example case
        - problem_examples_1_output (str): output for second example case
        - problem_examples_1_explanation (str): explanation for second example case
        - problem_topics_0 (str): first topic tag associated with the problem
        - problem_topics_1 (str): second topic tag associated with the problem
        - problem_code_templates_0_lang (str): programming language name for first code template
        - problem_code_templates_0_langSlug (str): URL-friendly language slug for first code template
        - problem_code_templates_0_code (str): code template for first language
        - problem_code_templates_1_lang (str): programming language name for second code template
        - problem_code_templates_1_langSlug (str): URL-friendly language slug for second code template
        - problem_code_templates_1_code (str): code template for second language
        - problem_stats_total_accepted (str): total number of accepted submissions (formatted string)
        - problem_stats_total_submissions (str): total number of submissions (formatted string)
        - problem_stats_acceptance_rate (str): acceptance rate percentage as a string
        - problem_hints_0 (str): first hint provided for solving the problem
        - problem_hints_1 (str): second hint provided for solving the problem
        - problem_sample_test_case (str): sample test case input provided for testing
        - problem_function_name (str): name of the function to implement in the solution
        - problem_parameters_0_name (str): name of first function parameter
        - problem_parameters_0_type (str): type of first function parameter
        - problem_parameters_1_name (str): name of second function parameter
        - problem_parameters_1_type (str): type of second function parameter
        - problem_return_type (str): return type of the function
    """
    return {
        "date": "2023-12-05",
        "problem_link": "/problems/two-sum",
        "problem_title": "Two Sum",
        "problem_title_slug": "two-sum",
        "problem_difficulty": "Easy",
        "problem_description": "<p>Given an array of integers <code>nums</code> and an integer <code>target</code>, return indices of the two numbers such that they add up to <code>target</code>.</p><p>You may assume that each input would have exactly one solution, and you may not use the same element twice.</p>",
        "problem_constraints_0": "2 <= nums.length <= 10^4",
        "problem_constraints_1": "-10^9 <= nums[i] <= 10^9",
        "problem_examples_0_input": "nums = [2,7,11,15], target = 9",
        "problem_examples_0_output": "[0,1]",
        "problem_examples_0_explanation": "Because nums[0] + nums[1] == 9, we return [0, 1].",
        "problem_examples_1_input": "nums = [3,2,4], target = 6",
        "problem_examples_1_output": "[1,2]",
        "problem_examples_1_explanation": "Because nums[1] + nums[2] == 6, we return [1, 2].",
        "problem_topics_0": "Array",
        "problem_topics_1": "Hash Table",
        "problem_code_templates_0_lang": "Python",
        "problem_code_templates_0_langSlug": "python3",
        "problem_code_templates_0_code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:",
        "problem_code_templates_1_lang": "Java",
        "problem_code_templates_1_langSlug": "java",
        "problem_code_templates_1_code": "class Solution {\n    public int[] twoSum(int[] nums, int target) {",
        "problem_stats_total_accepted": "15.6M",
        "problem_stats_total_submissions": "30.4M",
        "problem_stats_acceptance_rate": "51.3%",
        "problem_hints_0": "A really brute force way would be to check every combination.",
        "problem_hints_1": "Use a hash map to store values and their indices.",
        "problem_sample_test_case": "[2,7,11,15]\n9",
        "problem_function_name": "twoSum",
        "problem_parameters_0_name": "nums",
        "problem_parameters_0_type": "List[int]",
        "problem_parameters_1_name": "target",
        "problem_parameters_1_type": "int",
        "problem_return_type": "List[int]"
    }


def leetcode_get_daily_challenge() -> dict:
    """
    Retrieves today's LeetCode Daily Challenge problem with complete details, including problem description, constraints, and examples.
    
    Returns:
        A dictionary containing all details of the daily challenge with the following structure:
        - date (str): the date of the daily challenge in YYYY-MM-DD format
        - problem_link (str): relative URL path to the problem on LeetCode
        - problem_title (str): title of the coding problem
        - problem_title_slug (str): URL-friendly slug version of the problem title
        - problem_difficulty (str): difficulty level of the problem (e.g., "Easy", "Medium", "Hard")
        - problem_description (str): HTML-formatted description of the problem including examples and constraints
        - problem_constraints (List[str]): list of constraint strings extracted from the problem statement
        - problem_examples (List[Dict]): list of example cases, each with 'input', 'output', and 'explanation' fields
        - problem_topics (List[str]): list of topic tags associated with the problem (e.g., "Array", "Math")
        - problem_code_templates (List[Dict]): list of code templates for different programming languages, each with 'lang', 'langSlug', and 'code' fields
        - problem_stats_total_accepted (str): total number of accepted submissions (formatted string)
        - problem_stats_total_submissions (str): total number of submissions (formatted string)
        - problem_stats_acceptance_rate (str): acceptance rate percentage as a string
        - problem_hints (List[str]): list of hints provided for solving the problem
        - problem_sample_test_case (str): sample test case input provided for testing
        - problem_function_name (str): name of the function to implement in the solution
        - problem_parameters (List[Dict]): list of function parameters, each with 'name' and 'type' fields
        - problem_return_type (str): return type of the function
    
    Raises:
        Exception: If there is any error while retrieving or processing the daily challenge data.
    """
    try:
        api_data = call_external_api("leetcode-get_daily_challenge")
        
        result = {
            "date": api_data["date"],
            "problem_link": api_data["problem_link"],
            "problem_title": api_data["problem_title"],
            "problem_title_slug": api_data["problem_title_slug"],
            "problem_difficulty": api_data["problem_difficulty"],
            "problem_description": api_data["problem_description"],
            "problem_constraints": [
                api_data["problem_constraints_0"],
                api_data["problem_constraints_1"]
            ],
            "problem_examples": [
                {
                    "input": api_data["problem_examples_0_input"],
                    "output": api_data["problem_examples_0_output"],
                    "explanation": api_data["problem_examples_0_explanation"]
                },
                {
                    "input": api_data["problem_examples_1_input"],
                    "output": api_data["problem_examples_1_output"],
                    "explanation": api_data["problem_examples_1_explanation"]
                }
            ],
            "problem_topics": [
                api_data["problem_topics_0"],
                api_data["problem_topics_1"]
            ],
            "problem_code_templates": [
                {
                    "lang": api_data["problem_code_templates_0_lang"],
                    "langSlug": api_data["problem_code_templates_0_langSlug"],
                    "code": api_data["problem_code_templates_0_code"]
                },
                {
                    "lang": api_data["problem_code_templates_1_lang"],
                    "langSlug": api_data["problem_code_templates_1_langSlug"],
                    "code": api_data["problem_code_templates_1_code"]
                }
            ],
            "problem_stats_total_accepted": api_data["problem_stats_total_accepted"],
            "problem_stats_total_submissions": api_data["problem_stats_total_submissions"],
            "problem_stats_acceptance_rate": api_data["problem_stats_acceptance_rate"],
            "problem_hints": [
                api_data["problem_hints_0"],
                api_data["problem_hints_1"]
            ],
            "problem_sample_test_case": api_data["problem_sample_test_case"],
            "problem_function_name": api_data["problem_function_name"],
            "problem_parameters": [
                {
                    "name": api_data["problem_parameters_0_name"],
                    "type": api_data["problem_parameters_0_type"]
                },
                {
                    "name": api_data["problem_parameters_1_name"],
                    "type": api_data["problem_parameters_1_type"]
                }
            ],
            "problem_return_type": api_data["problem_return_type"]
        }
        
        return result
        
    except KeyError as e:
        raise Exception(f"Missing expected field in API response: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to retrieve daily challenge: {str(e)}")