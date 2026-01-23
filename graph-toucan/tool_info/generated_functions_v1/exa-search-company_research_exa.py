from typing import Dict, List, Any, Optional
import datetime
import random
import string


def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for company research using Exa AI.

    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - requestId (str): Unique identifier for the search request
        - autopromptString (str): Automatically generated search query string
        - autoDate (str): Date when autoprompt was generated, in ISO format
        - resolvedSearchType (str): Type of search algorithm used
        - searchTime (float): Total time taken for the search in milliseconds
        - costDollars_total (float): Total cost in USD
        - costDollars_search (float): Cost component for search in USD
        - costDollars_contents (float): Cost component for contents in USD
        - result_0_title (str): Title of first result
        - result_0_url (str): URL of first result
        - result_0_publishedDate (str): Published date of first result in ISO format
        - result_0_author (str): Author of first result
        - result_0_text (str): Excerpt text of first result
        - result_0_image (str): Image URL of first result (optional)
        - result_0_favicon (str): Favicon URL of first result (optional)
        - result_1_title (str): Title of second result
        - result_1_url (str): URL of second result
        - result_1_publishedDate (str): Published date of second result in ISO format
        - result_1_author (str): Author of second result
        - result_1_text (str): Excerpt text of second result
        - result_1_image (str): Image URL of second result (optional)
        - result_1_favicon (str): Favicon URL of second result (optional)
    """
    now_iso = datetime.datetime.now().isoformat()
    random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    return {
        "requestId": f"req_{random_id}",
        "autopromptString": f"comprehensive business overview, financials, news, and industry analysis for {random_id[:8]} Corp",
        "autoDate": now_iso,
        "resolvedSearchType": "neural",
        "searchTime": round(random.uniform(100.0, 500.0), 2),
        "costDollars_total": round(random.uniform(0.01, 0.1), 4),
        "costDollars_search": round(random.uniform(0.005, 0.05), 4),
        "costDollars_contents": round(random.uniform(0.005, 0.05), 4),
        "result_0_title": "Company Overview and Market Position",
        "result_0_url": "https://example.com/company-overview",
        "result_0_publishedDate": (datetime.datetime.now() - datetime.timedelta(days=2)).isoformat(),
        "result_0_author": "Business Insights Journal",
        "result_0_text": "Detailed analysis of the company's market strategy, competitive advantages, and growth trajectory.",
        "result_0_image": "https://example.com/images/company1.jpg",
        "result_0_favicon": "https://example.com/favicon.ico",
        "result_1_title": "Financial Performance and Investment Outlook",
        "result_1_url": "https://finance.example.com/report",
        "result_1_publishedDate": (datetime.datetime.now() - datetime.timedelta(days=5)).isoformat(),
        "result_1_author": "Financial Analyst Weekly",
        "result_1_text": "Quarterly earnings summary, revenue trends, and expert investment recommendations.",
        "result_1_image": "https://finance.example.com/charts/q4.png",
        "result_1_favicon": "https://finance.example.com/favicon.ico"
    }


def exa_search_company_research_exa(companyName: str, numResults: Optional[int] = 5) -> Dict[str, Any]:
    """
    Research companies using Exa AI - finds comprehensive information about businesses, organizations, and corporations.
    Provides insights into company operations, news, financial information, and industry analysis.

    Args:
        companyName (str): Name of the company to research (required)
        numResults (int, optional): Number of search results to return (default: 5)

    Returns:
        Dict containing:
        - requestId (str): unique identifier for the search request
        - autopromptString (str): automatically generated search query string used for company research
        - autoDate (str): date when the autoprompt was generated, in ISO format
        - resolvedSearchType (str): type of search algorithm used, e.g., "neural"
        - results (List[Dict]): list of search result items with keys:
            - title (str)
            - url (str)
            - publishedDate (str)
            - author (str)
            - text (str)
            - image (str, optional)
            - favicon (str, optional)
        - searchTime (float): total time taken for the search in milliseconds
        - costDollars (Dict): breakdown of costs in USD with keys:
            - total (float)
            - search (float)
            - contents (float)

    Raises:
        ValueError: If companyName is empty or None
    """
    if not companyName or not companyName.strip():
        raise ValueError("companyName is required and cannot be empty")
    
    if numResults is None:
        numResults = 5
    else:
        numResults = max(1, min(numResults, 10))  # Clamp between 1 and 10
    
    # Call external API (simulated)
    api_data = call_external_api("exa-search-company_research_exa")
    
    # Construct results list from indexed fields
    results = []
    for i in range(min(numResults, 2)):  # We only have 2 simulated results
        result_prefix = f"result_{i}_"
        result = {
            "title": api_data[f"{result_prefix}title"],
            "url": api_data[f"{result_prefix}url"],
            "publishedDate": api_data[f"{result_prefix}publishedDate"],
            "author": api_data[f"{result_prefix}author"],
            "text": api_data[f"{result_prefix}text"]
        }
        
        # Add optional fields if present and not None
        if f"{result_prefix}image" in api_data and api_data[f"{result_prefix}image"]:
            result["image"] = api_data[f"{result_prefix}image"]
        if f"{result_prefix}favicon" in api_data and api_data[f"{result_prefix}favicon"]:
            result["favicon"] = api_data[f"{result_prefix}favicon"]
            
        results.append(result)
    
    # Construct cost breakdown
    cost_dollars = {
        "total": api_data["costDollars_total"],
        "search": api_data["costDollars_search"],
        "contents": api_data["costDollars_contents"]
    }
    
    # Build final response structure
    response = {
        "requestId": api_data["requestId"],
        "autopromptString": api_data["autopromptString"],
        "autoDate": api_data["autoDate"],
        "resolvedSearchType": api_data["resolvedSearchType"],
        "results": results,
        "searchTime": api_data["searchTime"],
        "costDollars": cost_dollars
    }
    
    return response