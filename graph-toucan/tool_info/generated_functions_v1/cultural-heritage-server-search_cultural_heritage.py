from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external cultural heritage API.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - result_0_title (str): Title of the first cultural heritage item
        - result_0_artist (str): Artist of the first item
        - result_0_year (str): Creation year of the first item
        - result_0_type (str): Type of the first item (e.g., painting, sculpture)
        - result_0_institution (str): Institution holding the first item
        - result_0_country (str): Country where the first item is located
        - result_0_description (str): Description of the first item
        - result_0_medium (str): Medium/material of the first item
        - result_0_dimensions (str): Dimensions of the first item
        - result_1_title (str): Title of the second cultural heritage item
        - result_1_artist (str): Artist of the second item
        - result_1_year (str): Creation year of the second item
        - result_1_type (str): Type of the second item
        - result_1_institution (str): Institution holding the second item
        - result_1_country (str): Country where the second item is located
        - result_1_description (str): Description of the second item
        - result_1_medium (str): Medium/material of the second item
        - result_1_dimensions (str): Dimensions of the second item
        - query (str): The original search query used
        - total_found (int): Total number of items found matching the query
        - success (bool): Whether the search was successful
        - error_message (str): Error message if search failed, otherwise null
    """
    return {
        "result_0_title": "Starry Night",
        "result_0_artist": "Vincent van Gogh",
        "result_0_year": "1889",
        "result_0_type": "Painting",
        "result_0_institution": "Museum of Modern Art",
        "result_0_country": "United States",
        "result_0_description": "A night sky filled with swirling clouds, shining stars, and a bright crescent moon.",
        "result_0_medium": "Oil on canvas",
        "result_0_dimensions": "73.7 cm × 92.1 cm",
        "result_1_title": "The Potato Eaters",
        "result_1_artist": "Vincent van Gogh",
        "result_1_year": "1885",
        "result_1_type": "Painting",
        "result_1_institution": "Van Gogh Museum",
        "result_1_country": "Netherlands",
        "result_1_description": "A painting depicting a group of peasants eating potatoes.",
        "result_1_medium": "Oil on canvas",
        "result_1_dimensions": "82 cm × 114 cm",
        "query": "Van Gogh",
        "total_found": 124,
        "success": True,
        "error_message": None
    }

def cultural_heritage_server_search_cultural_heritage(query: str, limit: Optional[int] = 5) -> Dict[str, Any]:
    """
    Search for cultural heritage items (artworks, artifacts, etc.) from European institutions.
    
    Args:
        query (str): Search term (artist name, artwork title, type, etc.)
        limit (int, optional): Maximum number of results to return. Defaults to 5.
    
    Returns:
        Dict containing:
        - results (List[Dict]): List of cultural heritage items with details including 'title', 'artist', 'year', 
          'type', 'institution', 'country', 'description', 'medium', 'dimensions'
        - query (str): The original search query used
        - total_found (int): Total number of items found for the query
        - success (bool): Whether the search returned valid results
        - error_message (str): Description of error if no items were found, otherwise None
    """
    if not query or not query.strip():
        return {
            "results": [],
            "query": "",
            "total_found": 0,
            "success": False,
            "error_message": "Query parameter is required and cannot be empty"
        }
    
    # Fetch simulated API data
    api_data = call_external_api("cultural-heritage-server-search_cultural_heritage")
    
    # Construct results list from flattened API data
    results = []
    
    # Process up to 2 results from API (simulated data only has 2)
    for i in range(min(2, limit or 5)):
        result_key = f"result_{i}_title"
        if result_key not in api_data or api_data[result_key] is None:
            continue
            
        item = {
            "title": api_data[f"result_{i}_title"],
            "artist": api_data[f"result_{i}_artist"],
            "year": api_data[f"result_{i}_year"],
            "type": api_data[f"result_{i}_type"],
            "institution": api_data[f"result_{i}_institution"],
            "country": api_data[f"result_{i}_country"],
            "description": api_data[f"result_{i}_description"],
            "medium": api_data[f"result_{i}_medium"],
            "dimensions": api_data[f"result_{i}_dimensions"]
        }
        results.append(item)
    
    # Return structured response matching output schema
    return {
        "results": results,
        "query": api_data["query"],
        "total_found": api_data["total_found"],
        "success": api_data["success"],
        "error_message": api_data["error_message"]
    }