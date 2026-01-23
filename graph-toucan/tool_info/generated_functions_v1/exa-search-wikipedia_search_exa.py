from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Wikipedia search via Exa.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_title (str): Title of the first Wikipedia article result
        - result_0_url (str): URL of the first Wikipedia article result
        - result_0_snippet (str): Snippet of the first Wikipedia article result
        - result_1_title (str): Title of the second Wikipedia article result
        - result_1_url (str): URL of the second Wikipedia article result
        - result_1_snippet (str): Snippet of the second Wikipedia article result
        - count (int): Number of results returned (2 in this simulation)
        - total_hits (int): Estimated total number of matching Wikipedia articles
        - query_id (str): Unique identifier for the search query
        - metadata_timestamp (str): Timestamp of the search execution
        - metadata_processing_time (float): Time taken to process the search (in seconds)
        - metadata_source (str): Source attribution for the data
    """
    return {
        "result_0_title": "Artificial Intelligence",
        "result_0_url": "https://en.wikipedia.org/wiki/Artificial_Intelligence",
        "result_0_snippet": "Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to natural intelligence displayed by humans and animals.",
        "result_1_title": "Machine Learning",
        "result_1_url": "https://en.wikipedia.org/wiki/Machine_Learning",
        "result_1_snippet": "Machine learning is a method of data analysis that automates analytical model building using algorithms that iteratively learn from data.",
        "count": 2,
        "total_hits": 1500,
        "query_id": "q123456789",
        "metadata_timestamp": "2023-10-05T14:48:00Z",
        "metadata_processing_time": 0.45,
        "metadata_source": "Wikipedia via Exa"
    }

def exa_search_wikipedia_search_exa(query: str, numResults: Optional[int] = 5) -> Dict[str, Any]:
    """
    Search Wikipedia articles using Exa AI - finds comprehensive, factual information from Wikipedia entries.
    
    Args:
        query (str): Wikipedia search query (topic, person, place, concept, etc.)
        numResults (Optional[int]): Number of Wikipedia articles to return (default: 5)
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of Wikipedia article entries with title, url, snippet
        - count (int): Total number of results returned
        - total_hits (int): Estimated total number of matching articles on Wikipedia
        - query_id (str): Unique identifier for this search query
        - metadata (Dict): Additional info about search execution including timestamp, processing time, and source
    
    Raises:
        ValueError: If query is empty or None
    """
    if not query or not query.strip():
        raise ValueError("Query parameter is required and cannot be empty")
    
    if numResults is None:
        numResults = 5
    elif numResults <= 0:
        raise ValueError("numResults must be a positive integer")
    
    # Call simulated external API
    api_data = call_external_api("exa-search-wikipedia_search_exa")
    
    # Construct results list from flattened API response
    results = [
        {
            "title": api_data["result_0_title"],
            "url": api_data["result_0_url"],
            "snippet": api_data["result_0_snippet"]
        },
        {
            "title": api_data["result_1_title"],
            "url": api_data["result_1_url"],
            "snippet": api_data["result_1_snippet"]
        }
    ]
    
    # Respect numResults limit
    limited_results = results[:numResults]
    
    # Construct final output matching schema
    output = {
        "results": limited_results,
        "count": min(len(limited_results), api_data["count"]),
        "total_hits": api_data["total_hits"],
        "query_id": api_data["query_id"],
        "metadata": {
            "timestamp": api_data["metadata_timestamp"],
            "processing_time": api_data["metadata_processing_time"],
            "source": api_data["metadata_source"]
        }
    }
    
    return output