from typing import Dict, Any, Optional, List

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for LeetCode problem search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - filters_tags_0 (str): First tag in applied filters
        - filters_tags_1 (str): Second tag in applied filters
        - filters_difficulty (str): Difficulty level in filters
        - pagination_limit (int): Number of problems returned per page
        - problems_total (int): Total number of matching problems
        - problems_questions_0_title (str): Title of first problem
        - problems_questions_0_titleSlug (str): Title slug of first problem
        - problems_questions_0_difficulty (str): Difficulty of first problem
        - problems_questions_0_acRate (float): Acceptance rate of first problem
        - problems_questions_0_topicTags_0 (str): First topic tag of first problem
        - problems_questions_0_topicTags_1 (str): Second topic tag of first problem
        - problems_questions_1_title (str): Title of second problem
        - problems_questions_1_titleSlug (str): Title slug of second problem
        - problems_questions_1_difficulty (str): Difficulty of second problem
        - problems_questions_1_acRate (float): Acceptance rate of second problem
        - problems_questions_1_topicTags_0 (str): First topic tag of second problem
        - problems_questions_1_topicTags_1 (str): Second topic tag of second problem
    """
    return {
        "filters_tags_0": "array",
        "filters_tags_1": "dynamic-programming",
        "filters_difficulty": "medium",
        "pagination_limit": 2,
        "problems_total": 45,
        "problems_questions_0_title": "Two Sum",
        "problems_questions_0_titleSlug": "two-sum",
        "problems_questions_0_difficulty": "easy",
        "problems_questions_0_acRate": 47.5,
        "problems_questions_0_topicTags_0": "array",
        "problems_questions_0_topicTags_1": "hash-table",
        "problems_questions_1_title": "Longest Substring Without Repeating Characters",
        "problems_questions_1_titleSlug": "longest-substring-without-repeating-characters",
        "problems_questions_1_difficulty": "medium",
        "problems_questions_1_acRate": 31.2,
        "problems_questions_1_topicTags_0": "hash-table",
        "problems_questions_1_topicTags_1": "two-pointers"
    }

def leetcode_search_problems(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    searchKeywords: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Searches for LeetCode problems based on multiple filter criteria including categories, tags, 
    difficulty levels, and keywords, with pagination support.
    
    Args:
        category (Optional[str]): Problem category filter (e.g., 'algorithms', 'database', 'shell')
        difficulty (Optional[str]): Problem difficulty level filter ('easy', 'medium', 'hard')
        limit (Optional[int]): Maximum number of problems to return in a single request
        offset (Optional[int]): Number of problems to skip for pagination
        searchKeywords (Optional[str]): Keywords to search in problem titles and descriptions
        tags (Optional[List[str]]): List of topic tags to filter problems by
    
    Returns:
        Dict containing:
        - filters (Dict): Applied filter criteria including tags, difficulty, and other parameters
        - pagination (Dict): Pagination details with limit
        - problems (Dict): Contains total count and list of question details with title, titleSlug, 
                         difficulty, acRate, and topicTags
    
    Raises:
        ValueError: If limit is negative or offset is negative
    """
    # Input validation
    if limit is not None and limit < 0:
        raise ValueError("Limit cannot be negative")
    if offset is not None and offset < 0:
        raise ValueError("Offset cannot be negative")
    
    # Call external API to get flattened data
    api_data = call_external_api("leetcode-search_problems")
    
    # Construct the filters dictionary
    filters = {
        "tags": [api_data["filters_tags_0"], api_data["filters_tags_1"]]
    }
    
    # Only include difficulty in filters if it was provided as input or exists in API response
    if difficulty:
        filters["difficulty"] = difficulty
    elif api_data.get("filters_difficulty"):
        filters["difficulty"] = api_data["filters_difficulty"]
    
    # Add category to filters if provided
    if category:
        filters["category"] = category
    
    # Construct pagination info
    pagination_limit = limit if limit is not None else api_data["pagination_limit"]
    pagination = {
        "limit": pagination_limit
    }
    
    # Construct problems list
    questions = [
        {
            "title": api_data["problems_questions_0_title"],
            "titleSlug": api_data["problems_questions_0_titleSlug"],
            "difficulty": api_data["problems_questions_0_difficulty"],
            "acRate": api_data["problems_questions_0_acRate"],
            "topicTags": [api_data["problems_questions_0_topicTags_0"], api_data["problems_questions_0_topicTags_1"]]
        },
        {
            "title": api_data["problems_questions_1_title"],
            "titleSlug": api_data["problems_questions_1_titleSlug"],
            "difficulty": api_data["problems_questions_1_difficulty"],
            "acRate": api_data["problems_questions_1_acRate"],
            "topicTags": [api_data["problems_questions_1_topicTags_0"], api_data["problems_questions_1_topicTags_1"]]
        }
    ]
    
    # Apply keyword filtering if searchKeywords is provided
    if searchKeywords:
        search_keywords_lower = searchKeywords.lower()
        filtered_questions = []
        for q in questions:
            if (search_keywords_lower in q["title"].lower() or 
                any(search_keywords_lower in tag.lower() for tag in q["topicTags"])):
                filtered_questions.append(q)
        questions = filtered_questions
    
    # Apply difficulty filtering if specified
    if difficulty:
        questions = [q for q in questions if q["difficulty"].lower() == difficulty.lower()]
    
    # Apply tags filtering if specified
    if tags:
        filtered_questions = []
        for q in questions:
            if any(tag.lower() in [t.lower() for t in q["topicTags"]] for tag in tags):
                filtered_questions.append(q)
        questions = filtered_questions
    
    # Apply limit and offset (pagination)
    start_idx = offset if offset is not None else 0
    end_idx = start_idx + pagination_limit
    questions = questions[start_idx:end_idx]
    
    problems = {
        "total": api_data["problems_total"],
        "questions": questions
    }
    
    # Return the complete structured response
    return {
        "filters": filters,
        "pagination": pagination,
        "problems": problems
    }