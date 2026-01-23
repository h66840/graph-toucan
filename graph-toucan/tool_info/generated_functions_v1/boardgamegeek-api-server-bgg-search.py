from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external BoardGameGeek API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - result_0_id (int): Board game ID for first result
        - result_0_name (str): Name of first game
        - result_0_description (str): Description of first game
        - result_0_year (int): Release year of first game
        - result_0_complexity (float): Complexity rating (1-5) of first game
        - result_0_players (str): Players range for first game
        - result_0_bgg_rating (float): BGG average rating of first game
        - result_0_bayes_average (float): BGG bayes average rating of first game
        - result_0_play_time (int): Average play time in minutes for first game
        - result_0_min_age (int): Minimum recommended age for first game
        - result_0_designer (str): Designer(s) of first game
        - result_0_publisher (str): Publisher(s) of first game
        - result_0_type (str): Type of first game ('boardgame' or 'boardgameexpansion')
        - result_0_thumbnail (str): URL to thumbnail image of first game
        - result_0_image (str): URL to full image of first game
        - result_0_categories (str): Comma-separated categories for first game
        - result_0_mechanics (str): Comma-separated mechanics for first game
        - result_0_num_ratings (int): Number of user ratings for first game
        - result_0_owned (int): Number of users who own first game
        - result_0_wishing (int): Number of users wishing for first game
        - result_0_trading (int): Number of users trading first game
        - result_0_wanting (int): Number of users wanting first game
        - result_1_id (int): Board game ID for second result
        - result_1_name (str): Name of second game
        - result_1_description (str): Description of second game
        - result_1_year (int): Release year of second game
        - result_1_complexity (float): Complexity rating (1-5) of second game
        - result_1_players (str): Players range for second game
        - result_1_bgg_rating (float): BGG average rating of second game
        - result_1_bayes_average (float): BGG bayes average rating of second game
        - result_1_play_time (int): Average play time in minutes for second game
        - result_1_min_age (int): Minimum recommended age for second game
        - result_1_designer (str): Designer(s) of second game
        - result_1_publisher (str): Publisher(s) of second game
        - result_1_type (str): Type of second game ('boardgame' or 'boardgameexpansion')
        - result_1_thumbnail (str): URL to thumbnail image of second game
        - result_1_image (str): URL to full image of second game
        - result_1_categories (str): Comma-separated categories for second game
        - result_1_mechanics (str): Comma-separated mechanics for second game
        - result_1_num_ratings (int): Number of user ratings for second game
        - result_1_owned (int): Number of users who own second game
        - result_1_wishing (int): Number of users wishing for second game
        - result_1_trading (int): Number of users trading second game
        - result_1_wanting (int): Number of users wanting second game
    """
    return {
        "result_0_id": 1234,
        "result_0_name": "Catan",
        "result_0_description": "A classic strategy game of settlement building in the island of Catan.",
        "result_0_year": 1995,
        "result_0_complexity": 2.3,
        "result_0_players": "3-4",
        "result_0_bgg_rating": 7.4,
        "result_0_bayes_average": 6.8,
        "result_0_play_time": 60,
        "result_0_min_age": 10,
        "result_0_designer": "Klaus Teuber",
        "result_0_publisher": "Mayfair Games",
        "result_0_type": "boardgame",
        "result_0_thumbnail": "https://cf.geekdo-images.com/thumb/img/ABC123=/fit-in/200x150/pic123456.jpg",
        "result_0_image": "https://cf.geekdo-images.com/original/img/ABC123=/fit-in/500x500/pic123456.jpg",
        "result_0_categories": "Economic, Exploration",
        "result_0_mechanics": "Dice Rolling, Trading, Worker Placement",
        "result_0_num_ratings": 150000,
        "result_0_owned": 85000,
        "result_0_wishing": 12000,
        "result_0_trading": 350,
        "result_0_wanting": 9800,
        "result_1_id": 5678,
        "result_1_name": "Ticket to Ride",
        "result_1_description": "A cross-country train adventure where players collect cards to claim railway routes.",
        "result_1_year": 2004,
        "result_1_complexity": 1.8,
        "result_1_players": "2-5",
        "result_1_bgg_rating": 7.2,
        "result_1_bayes_average": 6.7,
        "result_1_play_time": 45,
        "result_1_min_age": 8,
        "result_1_designer": "Alan R. Moon",
        "result_1_publisher": "Days of Wonder",
        "result_1_type": "boardgame",
        "result_1_thumbnail": "https://cf.geekdo-images.com/thumb/img/DEF456=/fit-in/200x150/pic789012.jpg",
        "result_1_image": "https://cf.geekdo-images.com/original/img/DEF456=/fit-in/500x500/pic789012.jpg",
        "result_1_categories": "Action / Dexterity, Educational",
        "result_1_mechanics": "Set Collection, Route Building",
        "result_1_num_ratings": 130000,
        "result_1_owned": 78000,
        "result_1_wishing": 15000,
        "result_1_trading": 280,
        "result_1_wanting": 11000,
    }

def boardgamegeek_api_server_bgg_search(query: str, limit: Optional[int] = 30, type: Optional[str] = "all") -> Dict[str, Any]:
    """
    Search for board games on BoardGameGeek (BGG) by name or part of a name using a broad search.
    
    Args:
        query (str): Game name to search for on BoardGameGeek (BGG). Required.
        limit (Optional[int]): Maximum number of results to return. Default is 30.
        type (Optional[str]): Filter by type. Options: 'boardgame', 'boardgameexpansion', or 'all'. Default is 'all'.
    
    Returns:
        Dict containing a list of board game search results with detailed information.
        Each result includes: id, name, description, year, complexity, players, bgg_rating,
        bayes_average, play_time, min_age, designer, publisher, type, thumbnail, image,
        categories, mechanics, num_ratings, owned, wishing, trading, wanting.
    
    Raises:
        ValueError: If query is empty or None.
    """
    if not query:
        raise ValueError("Query parameter is required and cannot be empty.")
    
    if limit is None:
        limit = 30
    if type is None:
        type = "all"
    
    # Validate type parameter
    valid_types = ["all", "boardgame", "boardgameexpansion"]
    if type not in valid_types:
        raise ValueError(f"Type must be one of {valid_types}")
    
    # Get data from simulated external API
    api_data = call_external_api("boardgamegeek-api-server-bgg-search")
    
    # Parse categories and mechanics from comma-separated strings
    def parse_comma_list(value: str) -> List[str]:
        return [item.strip() for item in value.split(",")] if value else []
    
    # Construct results list from flat API data
    results: List[Dict[str, Any]] = []
    
    for i in range(2):  # We have 2 simulated results
        prefix = f"result_{i}"
        game_type = api_data.get(f"{prefix}_type", "")
        
        # Apply type filtering if