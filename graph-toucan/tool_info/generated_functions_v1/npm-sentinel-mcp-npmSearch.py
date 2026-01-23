from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for NPM package search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - query (str): Original search query used
        - limitUsed (int): Maximum number of results returned
        - totalResults (int): Total number of packages found matching the query
        - resultsCount (int): Actual number of results included in this response
        - result_0_name (str): Name of first result
        - result_0_version (str): Version of first result
        - result_0_description (str): Description of first result
        - result_0_keywords (str): Keywords of first result (comma-separated)
        - result_0_publisher_username (str): Publisher username of first result
        - result_0_publisher_email (str): Publisher email of first result
        - result_0_date (str): Date of first result
        - result_0_link_npm (str): NPM link of first result
        - result_0_link_homepage (str): Homepage link of first result
        - result_0_link_repository (str): Repository link of first result
        - result_0_link_bugs (str): Bugs link of first result
        - result_0_score_final (float): Final score of first result
        - result_0_score_detail_quality (float): Quality score of first result
        - result_0_score_detail_popularity (float): Popularity score of first result
        - result_0_score_detail_maintenance (float): Maintenance score of first result
        - result_0_searchScore (float): Search score of first result
        - result_1_name (str): Name of second result
        - result_1_version (str): Version of second result
        - result_1_description (str): Description of second result
        - result_1_keywords (str): Keywords of second result (comma-separated)
        - result_1_publisher_username (str): Publisher username of second result
        - result_1_publisher_email (str): Publisher email of second result
        - result_1_date (str): Date of second result
        - result_1_link_npm (str): NPM link of second result
        - result_1_link_homepage (str): Homepage link of second result
        - result_1_link_repository (str): Repository link of second result
        - result_1_link_bugs (str): Bugs link of second result
        - result_1_score_final (float): Final score of second result
        - result_1_score_detail_quality (float): Quality score of second result
        - result_1_score_detail_popularity (float): Popularity score of second result
        - result_1_score_detail_maintenance (float): Maintenance score of second result
        - result_1_searchScore (float): Search score of second result
        - message (str): Human-readable summary of the search outcome
    """
    return {
        "query": "react",
        "limitUsed": 10,
        "totalResults": 1500,
        "resultsCount": 2,
        "result_0_name": "react",
        "result_0_version": "18.2.0",
        "result_0_description": "A declarative, efficient, and flexible JavaScript library for building user interfaces.",
        "result_0_keywords": "react,ui,frontend,framework",
        "result_0_publisher_username": "acdlite",
        "result_0_publisher_email": "acdlite@fb.com",
        "result_0_date": "2023-04-15T12:00:00Z",
        "result_0_link_npm": "https://www.npmjs.com/package/react",
        "result_0_link_homepage": "https://reactjs.org",
        "result_0_link_repository": "https://github.com/facebook/react",
        "result_0_link_bugs": "https://github.com/facebook/react/issues",
        "result_0_score_final": 0.98,
        "result_0_score_detail_quality": 0.99,
        "result_0_score_detail_popularity": 1.0,
        "result_0_score_detail_maintenance": 0.97,
        "result_0_searchScore": 1000.0,
        "result_1_name": "react-dom",
        "result_1_version": "18.2.0",
        "result_1_description": "Serves as the entry point to the DOM and server renderers for React.",
        "result_1_keywords": "react,dom,render,frontend",
        "result_1_publisher_username": "acdlite",
        "result_1_publisher_email": "acdlite@fb.com",
        "result_1_date": "2023-04-15T12:00:00Z",
        "result_1_link_npm": "https://www.npmjs.com/package/react-dom",
        "result_1_link_homepage": "https://reactjs.org",
        "result_1_link_repository": "https://github.com/facebook/react",
        "result_1_link_bugs": "https://github.com/facebook/react/issues",
        "result_1_score_final": 0.97,
        "result_1_score_detail_quality": 0.98,
        "result_1_score_detail_popularity": 0.99,
        "result_1_score_detail_maintenance": 0.96,
        "result_1_searchScore": 950.0,
        "message": "Found 1500 packages matching query 'react'. Returning 2 results."
    }

def npm_sentinel_mcp_npmSearch(limit: Optional[int] = 10, query: Optional[str] = None) -> Dict[str, Any]:
    """
    Search for NPM packages with optional limit.
    
    Args:
        limit (Optional[int]): Maximum number of results to return (default: 10)
        query (Optional[str]): Search query for packages (required)
    
    Returns:
        Dict containing:
        - query (str): the original search query used for the package search
        - limitUsed (int): the maximum number of results returned in this response
        - totalResults (int): total number of packages found matching the query
        - resultsCount (int): actual number of results included in this response
        - results (List[Dict]): list of package objects with detailed information
        - message (str): human-readable summary of the search outcome
    
    Raises:
        ValueError: If query is not provided
    """
    if not query:
        raise ValueError("Query parameter is required")
    
    # Use default limit if not provided
    limit_used = limit if limit is not None else 10
    
    # Call external API to get data (simulated)
    api_data = call_external_api("npm-sentinel-mcp-npmSearch")
    
    # Construct results list from indexed fields
    results = []
    
    # Process first result if available
    if api_data.get("resultsCount", 0) > 0:
        result_0 = {
            "name": api_data["result_0_name"],
            "version": api_data["result_0_version"],
            "description": api_data["result_0_description"],
            "keywords": api_data["result_0_keywords"].split(",") if api_data["result_0_keywords"] else [],
            "publisher": {
                "username": api_data["result_0_publisher_username"],
                "email": api_data["result_0_publisher_email"]
            },
            "date": api_data["result_0_date"],
            "links": {
                "npm": api_data["result_0_link_npm"],
                "homepage": api_data["result_0_link_homepage"],
                "repository": api_data["result_0_link_repository"],
                "bugs": api_data["result_0_link_bugs"]
            },
            "score": {
                "final": api_data["result_0_score_final"],
                "detail": {
                    "quality": api_data["result_0_score_detail_quality"],
                    "popularity": api_data["result_0_score_detail_popularity"],
                    "maintenance": api_data["result_0_score_detail_maintenance"]
                }
            },
            "searchScore": api_data["result_0_searchScore"]
        }
        results.append(result_0)
    
    # Process second result if available
    if api_data.get("resultsCount", 0) > 1:
        result_1 = {
            "name": api_data["result_1_name"],
            "version": api_data["result_1_version"],
            "description": api_data["result_1_description"],
            "keywords": api_data["result_1_keywords"].split(",") if api_data["result_1_keywords"] else [],
            "publisher": {
                "username": api_data["result_1_publisher_username"],
                "email": api_data["result_1_publisher_email"]
            },
            "date": api_data["result_1_date"],
            "links": {
                "npm": api_data["result_1_link_npm"],
                "homepage": api_data["result_1_link_homepage"],
                "repository": api_data["result_1_link_repository"],
                "bugs": api_data["result_1_link_bugs"]
            },
            "score": {
                "final": api_data["result_1_score_final"],
                "detail": {
                    "quality": api_data["result_1_score_detail_quality"],
                    "popularity": api_data["result_1_score_detail_popularity"],
                    "maintenance": api_data["result_1_score_detail_maintenance"]
                }
            },
            "searchScore": api_data["result_1_searchScore"]
        }
        results.append(result_1)
    
    # Return the structured response
    return {
        "query": api_data["query"],
        "limitUsed": limit_used,
        "totalResults": api_data["totalResults"],
        "resultsCount": api_data["resultsCount"],
        "results": results,
        "message": api_data["message"]
    }