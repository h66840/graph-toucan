from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for cultural heritage recommendations.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - recommendation_0_title (str): Title of the first recommended artwork
        - recommendation_0_artist (str): Artist of the first recommended artwork
        - recommendation_0_year (int): Year of creation for the first artwork
        - recommendation_0_museum (str): Museum where the first artwork is located
        - recommendation_0_description (str): Description of the first artwork
        - recommendation_0_id (str): Unique ID of the first artwork
        - recommendation_1_title (str): Title of the second recommended artwork
        - recommendation_1_artist (str): Artist of the second recommended artwork
        - recommendation_1_year (int): Year of creation for the second artwork
        - recommendation_1_museum (str): Museum where the second artwork is located
        - recommendation_1_description (str): Description of the second artwork
        - recommendation_1_id (str): Unique ID of the second artwork
        - query_summary (str): Summary of the user interest that generated recommendations
    """
    return {
        "recommendation_0_title": "Starry Night",
        "recommendation_0_artist": "Vincent van Gogh",
        "recommendation_0_year": 1889,
        "recommendation_0_museum": "Museum of Modern Art",
        "recommendation_0_description": "A night sky filled with swirling clouds, shining stars, and a bright crescent moon.",
        "recommendation_0_id": "moa-vangogh-001",
        "recommendation_1_title": "The Scream",
        "recommendation_1_artist": "Edvard Munch",
        "recommendation_1_year": 1893,
        "recommendation_1_museum": "National Gallery, Oslo",
        "recommendation_1_description": "An expressionistic painting depicting a figure with an agonized expression against a landscape with a tumultuous orange sky.",
        "recommendation_1_id": "ng-oslo-munch-005",
        "query_summary": "Expressionist paintings with emotional intensity"
    }

def cultural_heritage_server_get_cultural_recommendations(user_interest: str) -> Dict[str, Any]:
    """
    Get AI-powered recommendations for cultural heritage items based on user interests.
    
    Args:
        user_interest (str): User's cultural interests (e.g., "modern art", "renaissance", "impressionist")
    
    Returns:
        Dict containing:
            - recommendations (List[Dict]): list of recommended artworks, each with 'title', 'artist', 'year', 'museum', 'description', and 'id' fields
            - query_summary (str): summary of the user interest or query topic that generated the recommendations
    
    Raises:
        ValueError: If user_interest is empty or not a string
    """
    if not user_interest:
        raise ValueError("user_interest is required")
    if not isinstance(user_interest, str):
        raise ValueError("user_interest must be a string")
    
    # Fetch data from simulated external API
    api_data = call_external_api("cultural-heritage-server-get_cultural_recommendations")
    
    # Construct recommendations list from flattened API response
    recommendations = [
        {
            "title": api_data["recommendation_0_title"],
            "artist": api_data["recommendation_0_artist"],
            "year": api_data["recommendation_0_year"],
            "museum": api_data["recommendation_0_museum"],
            "description": api_data["recommendation_0_description"],
            "id": api_data["recommendation_0_id"]
        },
        {
            "title": api_data["recommendation_1_title"],
            "artist": api_data["recommendation_1_artist"],
            "year": api_data["recommendation_1_year"],
            "museum": api_data["recommendation_1_museum"],
            "description": api_data["recommendation_1_description"],
            "id": api_data["recommendation_1_id"]
        }
    ]
    
    # Construct final result matching output schema
    result = {
        "recommendations": recommendations,
        "query_summary": api_data["query_summary"]
    }
    
    return result