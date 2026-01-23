from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for documentation search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - results_count (int): Total number of search results returned
        - result_0_file (str): File path of the first matched document
        - result_0_match_0_line (int): Line number of the first match in the first result
        - result_0_match_0_content (str): Content of the first match in the first result
        - result_0_match_0_context (str): Context around the first match in the first result
        - result_0_match_1_line (int): Line number of the second match in the first result
        - result_0_match_1_content (str): Content of the second match in the first result
        - result_0_match_1_context (str): Context around the second match in the first result
        - result_1_file (str): File path of the second matched document
        - result_1_match_0_line (int): Line number of the first match in the second result
        - result_1_match_0_content (str): Content of the first match in the second result
        - result_1_match_0_context (str): Context around the first match in the second result
        - result_1_match_1_line (int): Line number of the second match in the second result
        - result_1_match_1_content (str): Content of the second match in the second result
        - result_1_match_1_context (str): Context around the second match in the second result
    """
    return {
        "results_count": 2,
        "result_0_file": "user_guide.md",
        "result_0_match_0_line": 42,
        "result_0_match_0_content": "The quick brown fox jumps over the lazy dog.",
        "result_0_match_0_context": "In this example, the quick brown fox jumps over the lazy dog. This demonstrates basic behavior.",
        "result_0_match_1_line": 87,
        "result_0_match_1_content": "Quick access to settings is available via the dashboard.",
        "result_0_match_1_context": "For users needing quick access to settings, navigate to the dashboard and click 'Preferences'.",
        "result_1_file": "api_reference.md",
        "result_1_match_0_line": 15,
        "result_1_match_0_content": "The API provides quick response times under normal load.",
        "result_1_match_0_context": "Performance metrics show that the API provides quick response times under normal load conditions.",
        "result_1_match_1_line": 203,
        "result_1_match_1_content": "Quick start guide is available in the documentation section.",
        "result_1_match_1_context": "New developers should consult the quick start guide available in the documentation section."
    }

def aurora_documentation_search_docs(query: str, case_sensitive: Optional[bool] = False) -> Dict[str, Any]:
    """
    Search through documentation files for specific content.
    
    Args:
        query (str): Search query to find in documentation (required)
        case_sensitive (bool, optional): Whether search should be case sensitive. Defaults to False.
    
    Returns:
        Dict containing:
        - results_count (int): total number of search results returned
        - results (List[Dict]): list of matched documents, each containing 'file', 'matches' fields;
          'matches' is a list of occurrences with 'line', 'content', and 'context'
    
    Raises:
        ValueError: If query is empty or not provided
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    # Call external API to get flat data
    api_data = call_external_api("aurora-documentation-search_docs")
    
    # Construct results list from flattened API response
    results = []
    
    # Process first result
    if api_data.get("result_0_file"):
        matches = []
        if api_data.get("result_0_match_0_line") is not None:
            matches.append({
                "line": api_data["result_0_match_0_line"],
                "content": api_data["result_0_match_0_content"],
                "context": api_data["result_0_match_0_context"]
            })
        if api_data.get("result_0_match_1_line") is not None:
            matches.append({
                "line": api_data["result_0_match_1_line"],
                "content": api_data["result_0_match_1_content"],
                "context": api_data["result_0_match_1_context"]
            })
        
        results.append({
            "file": api_data["result_0_file"],
            "matches": matches
        })
    
    # Process second result
    if api_data.get("result_1_file"):
        matches = []
        if api_data.get("result_1_match_0_line") is not None:
            matches.append({
                "line": api_data["result_1_match_0_line"],
                "content": api_data["result_1_match_0_content"],
                "context": api_data["result_1_match_0_context"]
            })
        if api_data.get("result_1_match_1_line") is not None:
            matches.append({
                "line": api_data["result_1_match_1_line"],
                "content": api_data["result_1_match_1_content"],
                "context": api_data["result_1_match_1_context"]
            })
        
        results.append({
            "file": api_data["result_1_file"],
            "matches": matches
        })
    
    # Return final structured response
    return {
        "results_count": api_data["results_count"],
        "results": results
    }