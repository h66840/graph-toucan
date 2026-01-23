from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for task listing.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - totalTasks (int): Total number of available tasks
        - category_0_name (str): First category name
        - category_0_task_0_task (str): First task's task identifier in first category
        - category_0_task_0_description (str): First task's description in first category
        - category_0_task_0_nodeType (str): First task's node type in first category
        - category_0_task_1_task (str): Second task's task identifier in first category
        - category_0_task_1_description (str): Second task's description in first category
        - category_0_task_1_nodeType (str): Second task's node type in first category
        - category_1_name (str): Second category name
        - category_1_task_0_task (str): First task's task identifier in second category
        - category_1_task_0_description (str): First task's description in second category
        - category_1_task_0_nodeType (str): First task's node type in second category
        - category_1_task_1_task (str): Second task's task identifier in second category
        - category_1_task_1_description (str): Second task's description in second category
        - category_1_task_1_nodeType (str): Second task's node type in second category
    """
    return {
        "totalTasks": 6,
        "category_0_name": "HTTP/API",
        "category_0_task_0_task": "http_get_request",
        "category_0_task_0_description": "Perform an HTTP GET request to a specified URL",
        "category_0_task_0_nodeType": "HTTP_NODE",
        "category_0_task_1_task": "http_post_request",
        "category_0_task_1_description": "Perform an HTTP POST request with JSON payload",
        "category_0_task_1_nodeType": "HTTP_NODE",
        "category_1_name": "AI/LangChain",
        "category_1_task_0_task": "llm_text_generation",
        "category_1_task_0_description": "Generate text using a large language model",
        "category_1_task_0_nodeType": "LLM_NODE",
        "category_1_task_1_task": "llm_summarization",
        "category_1_task_1_description": "Summarize long text using LLM",
        "category_1_task_1_nodeType": "LLM_NODE",
    }

def ennkaheksa_list_tasks(category: Optional[str] = None) -> Dict[str, Any]:
    """
    List all available task templates. Optionally filter by category.
    
    Args:
        category (Optional[str]): Optional category filter. One of: HTTP/API, Webhooks, 
                                 Database, AI/LangChain, Data Processing, Communication.
                                 If None, returns all categories.

    Returns:
        Dict containing:
        - totalTasks (int): Total number of available tasks across all categories
        - categories (Dict): Mapping of category names to lists of task objects.
                             Each task has 'task', 'description', and 'nodeType' fields.
    """
    # Fetch simulated external data
    api_data = call_external_api("ennkaheksa-list_tasks")
    
    # Reconstruct nested structure
    categories: Dict[str, List[Dict[str, str]]] = {}
    
    # Process first category
    cat0_name = api_data["category_0_name"]
    if category is None or category == cat0_name:
        categories[cat0_name] = [
            {
                "task": api_data["category_0_task_0_task"],
                "description": api_data["category_0_task_0_description"],
                "nodeType": api_data["category_0_task_0_nodeType"]
            },
            {
                "task": api_data["category_0_task_1_task"],
                "description": api_data["category_0_task_1_description"],
                "nodeType": api_data["category_0_task_1_nodeType"]
            }
        ]
    
    # Process second category
    cat1_name = api_data["category_1_name"]
    if category is None or category == cat1_name:
        categories[cat1_name] = [
            {
                "task": api_data["category_1_task_0_task"],
                "description": api_data["category_1_task_0_description"],
                "nodeType": api_data["category_1_task_0_nodeType"]
            },
            {
                "task": api_data["category_1_task_1_task"],
                "description": api_data["category_1_task_1_description"],
                "nodeType": api_data["category_1_task_1_nodeType"]
            }
        ]
    
    # Count total tasks in returned categories
    total_tasks = sum(len(tasks) for tasks in categories.values())
    
    return {
        "totalTasks": total_tasks,
        "categories": categories
    }