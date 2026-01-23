from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for documentation search.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first matching documentation page
        - result_0_description (str): Description of the first matching documentation page
        - result_0_path (str): Path to the first matching documentation page
        - result_0_relevanceScore (float): Relevance score of the first result
        - result_1_title (str): Title of the second matching documentation page
        - result_1_description (str): Description of the second matching documentation page
        - result_1_path (str): Path to the second matching documentation page
        - result_1_relevanceScore (float): Relevance score of the second result
    """
    return {
        "result_0_title": "Getting Started with Atlas",
        "result_0_description": "Introduction to Atlas documentation and basic setup instructions.",
        "result_0_path": "/docs/atlas/getting-started",
        "result_0_relevanceScore": 0.95,
        "result_1_title": "Atlas Query Language Guide",
        "result_1_description": "Detailed guide on using Atlas Query Language for data retrieval.",
        "result_1_path": "/docs/atlas/aql-guide",
        "result_1_relevanceScore": 0.87
    }

def atlas_docs_search_docs(docName: str, query: str) -> Dict[str, Any]:
    """
    Searches a documentation set for specific content.
    
    This function searches within the specified documentation set for pages
    matching the given query. It returns a list of matching pages ranked by relevance,
    including their titles, descriptions, paths, and relevance scores.
    
    Args:
        docName (str): Name of the documentation set to search within
        query (str): Search query to find relevant pages within the documentation set
    
    Returns:
        Dict containing a single key 'results' with a list of dictionaries,
        each representing a matching documentation page with keys:
        - title (str): Page title
        - description (str): Page description
        - path (str): Path to the page
        - relevanceScore (float): Relevance score between 0 and 1
    
    Raises:
        ValueError: If docName or query is empty
    """
    if not docName:
        raise ValueError("docName is required")
    if not query:
        raise ValueError("query is required")
    
    # Call external API to get search results as flat structure
    api_data = call_external_api("atlas-docs-search_docs")
    
    # Construct the nested results structure from flat API data
    results = [
        {
            "title": api_data["result_0_title"],
            "description": api_data["result_0_description"],
            "path": api_data["result_0_path"],
            "relevanceScore": api_data["result_0_relevanceScore"]
        },
        {
            "title": api_data["result_1_title"],
            "description": api_data["result_1_description"],
            "path": api_data["result_1_path"],
            "relevanceScore": api_data["result_1_relevanceScore"]
        }
    ]
    
    return {"results": results}