from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Exa AI content crawling.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - request_id (str): Unique identifier for the request
        - result_0_id (str): ID of the first crawled result
        - result_0_title (str): Title of the first crawled page
        - result_0_url (str): URL of the first crawled page
        - result_0_published_date (str): Published date of the first page
        - result_0_author (str): Author of the first page
        - result_0_text (str): Extracted text content of the first page
        - result_0_image (str): Image URL of the first page (optional)
        - result_0_favicon (str): Favicon URL of the first page (optional)
        - result_1_id (str): ID of the second crawled result
        - result_1_title (str): Title of the second crawled page
        - result_1_url (str): URL of the second crawled page
        - result_1_published_date (str): Published date of the second page
        - result_1_author (str): Author of the second page
        - result_1_text (str): Extracted text content of the second page
        - result_1_image (str): Image URL of the second page (optional)
        - result_1_favicon (str): Favicon URL of the second page (optional)
        - status_0_id (str): ID of the first status entry
        - status_0_status (str): Status of the first crawl attempt
        - status_0_error (str): Error message if first crawl failed (optional)
        - status_1_id (str): ID of the second status entry
        - status_1_status (str): Status of the second crawl attempt
        - status_1_error (str): Error message if second crawl failed (optional)
        - cost_dollars_total (float): Total cost in dollars
        - cost_dollars_contents (float): Cost breakdown for content extraction
        - search_time (float): Time taken for the search/crawl operation in seconds
    """
    return {
        "request_id": "req_1234567890abcdef",
        "result_0_id": "res_001",
        "result_0_title": "Introduction to Artificial Intelligence",
        "result_0_url": "https://example.com/ai-intro",
        "result_0_published_date": "2023-10-15T08:00:00Z",
        "result_0_author": "John Doe",
        "result_0_text": "Artificial Intelligence (AI) is a wonderful field that enables machines to think and act like humans. This article provides an overview of AI concepts, history, and applications in modern technology. AI has evolved significantly over the decades...",
        "result_0_image": "https://example.com/images/ai.jpg",
        "result_0_favicon": "https://example.com/favicon.ico",
        "result_1_id": "res_002",
        "result_1_title": "Machine Learning Basics",
        "result_1_url": "https://example.com/ml-basics",
        "result_1_published_date": "2023-09-22T10:30:00Z",
        "result_1_author": "Jane Smith",
        "result_1_text": "Machine Learning is a subset of AI that focuses on building systems that learn from data. This guide covers fundamental ML algorithms, training processes, and real-world use cases. Supervised and unsupervised learning are explained with examples...",
        "result_1_image": "https://example.com/images/ml.jpg",
        "result_1_favicon": "https://example.com/favicon.ico",
        "status_0_id": "res_001",
        "status_0_status": "success",
        "status_0_error": "",
        "status_1_id": "res_002",
        "status_1_status": "success",
        "status_1_error": "",
        "cost_dollars_total": 0.045,
        "cost_dollars_contents": 0.035,
        "search_time": 2.34
    }

def exa_search_crawling_exa(url: str, maxCharacters: Optional[int] = 3000) -> Dict[str, Any]:
    """
    Extract and crawl content from a specific URL using Exa AI.
    
    This function simulates retrieving full text content, metadata, and structured information
    from a web page. It returns detailed results including text, title, author, publication date,
    and other metadata.
    
    Args:
        url (str): The URL to crawl and extract content from (required)
        maxCharacters (Optional[int]): Maximum number of characters to extract (default: 3000)
    
    Returns:
        Dict containing:
        - requestId (str): unique identifier for the request
        - results (List[Dict]): list of crawled page results with fields 'id', 'title', 'url',
          'publishedDate', 'author', 'text', and optionally 'image', 'favicon'
        - statuses (List[Dict]): list of status objects with 'id', 'status', and optional 'error'
        - costDollars (Dict): contains 'total' cost and 'contents' breakdown
        - searchTime (float): time taken for the search/crawl operation in seconds
    
    Raises:
        ValueError: If url is empty or not a string
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    if maxCharacters is not None and (not isinstance(maxCharacters, int) or maxCharacters <= 0):
        raise ValueError("maxCharacters must be a positive integer")
    
    # Call external API to get flattened data
    api_data = call_external_api("exa-search-crawling_exa")
    
    # Construct results list
    results = [
        {
            "id": api_data["result_0_id"],
            "title": api_data["result_0_title"],
            "url": api_data["result_0_url"],
            "publishedDate": api_data["result_0_published_date"],
            "author": api_data["result_0_author"],
            "text": api_data["result_0_text"][:maxCharacters] if maxCharacters else api_data["result_0_text"]
        },
        {
            "id": api_data["result_1_id"],
            "title": api_data["result_1_title"],
            "url": api_data["result_1_url"],
            "publishedDate": api_data["result_1_published_date"],
            "author": api_data["result_1_author"],
            "text": api_data["result_1_text"][:maxCharacters] if maxCharacters else api_data["result_1_text"]
        }
    ]
    
    # Add optional image and favicon if present
    if api_data.get("result_0_image"):
        results[0]["image"] = api_data["result_0_image"]
    if api_data.get("result_0_favicon"):
        results[0]["favicon"] = api_data["result_0_favicon"]
    if api_data.get("result_1_image"):
        results[1]["image"] = api_data["result_1_image"]
    if api_data.get("result_1_favicon"):
        results[1]["favicon"] = api_data["result_1_favicon"]
    
    # Construct statuses list
    statuses = [
        {
            "id": api_data["status_0_id"],
            "status": api_data["status_0_status"]
        },
        {
            "id": api_data["status_1_id"],
            "status": api_data["status_1_status"]
        }
    ]
    
    # Add error field only if present
    if api_data.get("status_0_error"):
        statuses[0]["error"] = api_data["status_0_error"]
    if api_data.get("status_1_error"):
        statuses[1]["error"] = api_data["status_1_error"]
    
    # Construct costDollars object
    cost_dollars = {
        "total": api_data["cost_dollars_total"],
        "contents": api_data["cost_dollars_contents"]
    }
    
    # Return final structured response
    return {
        "requestId": api_data["request_id"],
        "results": results,
        "statuses": statuses,
        "costDollars": cost_dollars,
        "searchTime": api_data["search_time"]
    }