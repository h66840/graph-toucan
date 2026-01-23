from typing import Dict, List, Any, Optional

import sys
import os

# State Manager Injection
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

try:
    from state_manager import sys_state
except ImportError:
    pass # Fallback handled inside call_external_api checks or mock


def _original_call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for boardgame recommendations.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - recommendation_0_id (int): BGG ID of the first recommended game
        - recommendation_0_name (str): Name of the first recommended game
        - recommendation_0_description (str): Description of the first recommended game
        - recommendation_0_year (int): Release year of the first game
        - recommendation_0_complexity (float): Complexity rating (1-5) of the first game
        - recommendation_0_players (str): Players range for the first game
        - recommendation_0_bgg_rating (float): BGG average rating of the first game
        - recommendation_0_bayes_average (float): Bayes average rating of the first game
        - recommendation_0_play_time (int): Average play time in minutes for the first game
        - recommendation_0_min_age (int): Minimum recommended age for the first game
        - recommendation_0_designer (str): Designer(s) of the first game
        - recommendation_0_publisher (str): Publisher(s) of the first game
        - recommendation_0_type (str): Type of the first game (e.g., boardgame, expansion)
        - recommendation_0_thumbnail (str): URL to thumbnail image of the first game
        - recommendation_0_image (str): URL to full image of the first game
        - recommendation_0_categories (str): Comma-separated categories for the first game
        - recommendation_0_mechanics (str): Comma-separated mechanics for the first game
        - recommendation_0_num_ratings (int): Number of ratings for the first game
        - recommendation_0_owned (int): Number of users who own the first game
        - recommendation_0_wishing (int): Number of users wishing for the first game
        - recommendation_0_trading (int): Number of users trading the first game
        - recommendation_0_wanting (int): Number of users wanting the first game
        - recommendation_1_id (int): BGG ID of the second recommended game
        - recommendation_1_name (str): Name of the second recommended game
        - recommendation_1_description (str): Description of the second recommended game
        - recommendation_1_year (int): Release year of the second game
        - recommendation_1_complexity (float): Complexity rating (1-5) of the second game
        - recommendation_1_players (str): Players range for the second game
        - recommendation_1_bgg_rating (float): BGG average rating of the second game
        - recommendation_1_bayes_average (float): Bayes average rating of the second game
        - recommendation_1_play_time (int): Average play time in minutes for the second game
        - recommendation_1_min_age (int): Minimum recommended age for the second game
        - recommendation_1_designer (str): Designer(s) of the second game
        - recommendation_1_publisher (str): Publisher(s) of the second game
        - recommendation_1_type (str): Type of the second game (e.g., boardgame, expansion)
        - recommendation_1_thumbnail (str): URL to thumbnail image of the second game
        - recommendation_1_image (str): URL to full image of the second game
        - recommendation_1_categories (str): Comma-separated categories for the second game
        - recommendation_1_mechanics (str): Comma-separated mechanics for the second game
        - recommendation_1_num_ratings (int): Number of ratings for the second game
        - recommendation_1_owned (int): Number of users who own the second game
        - recommendation_1_wishing (int): Number of users wishing for the second game
        - recommendation_1_trading (int): Number of users trading the second game
        - recommendation_1_wanting (int): Number of users wanting the second game
    """
    return {
        "recommendation_0_id": 123456,
        "recommendation_0_name": "Wingspan",
        "recommendation_0_description": "A competitive, medium-weight, card-driven, engine-building board game from Stonemaier Games.",
        "recommendation_0_year": 2019,
        "recommendation_0_complexity": 2.3,
        "recommendation_0_players": "1-5",
        "recommendation_0_bgg_rating": 8.1,
        "recommendation_0_bayes_average": 7.9,
        "recommendation_0_play_time": 40,
        "recommendation_0_min_age": 10,
        "recommendation_0_designer": "Elizabeth Hargrave",
        "recommendation_0_publisher": "Stonemaier Games",
        "recommendation_0_type": "boardgame",
        "recommendation_0_thumbnail": "https://example.com/wingspan_thumb.jpg",
        "recommendation_0_image": "https://example.com/wingspan.jpg",
        "recommendation_0_categories": "Animals, Card Game, Educational",
        "recommendation_0_mechanics": "Card Drafting, Hand Management, Set Collection",
        "recommendation_0_num_ratings": 150000,
        "recommendation_0_owned": 85000,
        "recommendation_0_wishing": 25000,
        "recommendation_0_trading": 1200,
        "recommendation_0_wanting": 5000,
        "recommendation_1_id": 789012,
        "recommendation_1_name": "Pandemic Legacy: Season 1",
        "recommendation_1_description": "A cooperative campaign game with legacy elements where your choices affect future games.",
        "recommendation_1_year": 2015,
        "recommendation_1_complexity": 3.8,
        "recommendation_1_players": "2-4",
        "recommendation_1_bgg_rating": 8.4,
        "recommendation_1_bayes_average": 8.2,
        "recommendation_1_play_time": 60,
        "recommendation_1_min_age": 13,
        "recommendation_1_designer": "Matt Leacock, Rob Daviau",
        "recommendation_1_publisher": "Z-Man Games",
        "recommendation_1_type": "boardgame",
        "recommendation_1_thumbnail": "https://example.com/pandemic_legacy_thumb.jpg",
        "recommendation_1_image": "https://example.com/pandemic_legacy.jpg",
        "recommendation_1_categories": "Adventure, Medical, Modern",
        "recommendation_1_mechanics": "Cooperative Play, Legacy, Variable Player Powers",
        "recommendation_1_num_ratings": 120000,
        "recommendation_1_owned": 60000,
        "recommendation_1_wishing": 18000,
        "recommendation_1_trading": 800,
        "recommendation_1_wanting": 4000,
    }

def boardgamegeek_api_server_bgg_recommender(
    id: Optional[str] = None,
    min_votes: Optional[float] = 30,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get game recommendations based on a specific game using either the BoardGameGeek (BGG) ID or name directly.
    
    Args:
        id (Optional[str]): BoardGameGeek (BGG) ID of the game to base recommendations on (preferred for speed)
        min_votes (Optional[float]): Minimum votes threshold for recommendation quality (default: 30)
        name (Optional[str]): Name of the game to base recommendations on (slower than using ID)
    
    Returns:
        Dict containing a list of recommended board games with detailed information including:
        - recommendations (List[Dict]): list of recommended board games, each containing 'id', 'name', 'description',
          'year', 'complexity', 'players', 'bgg_rating', 'bayes_average', 'play_time', 'min_age', 'designer',
          'publisher', 'type', 'thumbnail', 'image', 'categories', 'mechanics', 'num_ratings', 'owned',
          'wishing', 'trading', 'wanting' fields
    
    Raises:
        ValueError: If neither id nor name is provided
    """
    # Input validation
    if not id and not name:
        raise ValueError("Either 'id' or 'name' must be provided to generate recommendations")
    
    # Validate min_votes
    if min_votes is not None and min_votes < 0:
        raise ValueError("min_votes must be non-negative")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("boardgamegeek-api-server-bgg-recommender", **locals())
    
    # Construct recommendations list from flattened API data
    recommendations: List[Dict[str, Any]] = []
    
    # Process first recommendation
    recommendations.append({
        "id": api_data["recommendation_0_id"],
        "name": api_data["recommendation_0_name"],
        "description": api_data["recommendation_0_description"],
        "year": api_data["recommendation_0_year"],
        "complexity": api_data["recommendation_0_complexity"],
        "players": api_data["recommendation_0_players"],
        "bgg_rating": api_data["recommendation_0_bgg_rating"],
        "bayes_average": api_data["recommendation_0_bayes_average"],
        "play_time": api_data["recommendation_0_play_time"],
        "min_age": api_data["recommendation_0_min_age"],
        "designer": api_data["recommendation_0_designer"],
        "publisher": api_data["recommendation_0_publisher"],
        "type": api_data["recommendation_0_type"],
        "thumbnail": api_data["recommendation_0_thumbnail"],
        "image": api_data["recommendation_0_image"],
        "categories": api_data["recommendation_0_categories"],
        "mechanics": api_data["recommendation_0_mechanics"],
        "num_ratings": api_data["recommendation_0_num_ratings"],
        "owned": api_data["recommendation_0_owned"],
        "wishing": api_data["recommendation_0_wishing"],
        "trading": api_data["recommendation_0_trading"],
        "wanting": api_data["recommendation_0_wanting"],
    })
    
    # Process second recommendation
    recommendations.append({
        "id": api_data["recommendation_1_id"],
        "name": api_data["recommendation_1_name"],
        "description": api_data["recommendation_1_description"],
        "year": api_data["recommendation_1_year"],
        "complexity": api_data["recommendation_1_complexity"],
        "players": api_data["recommendation_1_players"],
        "bgg_rating": api_data["recommendation_1_bgg_rating"],
        "bayes_average": api_data["recommendation_1_bayes_average"],
        "play_time": api_data["recommendation_1_play_time"],
        "min_age": api_data["recommendation_1_min_age"],
        "designer": api_data["recommendation_1_designer"],
        "publisher": api_data["recommendation_1_publisher"],
        "type": api_data["recommendation_1_type"],
        "thumbnail": api_data["recommendation_1_thumbnail"],
        "image": api_data["recommendation_1_image"],
        "categories": api_data["recommendation_1_categories"],
        "mechanics": api_data["recommendation_1_mechanics"],
        "num_ratings": api_data["recommendation_1_num_ratings"],
        "owned": api_data["recommendation_1_owned"],
        "wishing": api_data["recommendation_1_wishing"],
        "trading": api_data["recommendation_1_trading"],
        "wanting": api_data["recommendation_1_wanting"],
    })
    
    return {"recommendations": recommendations}

# Auto-Injected Stateful Wrapper
def call_external_api(tool_name: str, **kwargs) -> Dict[str, Any]:
    # 1. Execute original mock to get schema-compliant result
    result = _original_call_external_api(tool_name)
    
    # 2. Stateful Side-Effects (Heuristic)
    try:
        cmd = kwargs.get("command", "") or tool_name

        if "inventory" in tool_name:
            inv = sys_state.get_inventory()
            result["inventory"] = inv
            result["content"] = str(inv)
            
        if "add" in tool_name or "buy" in tool_name:
             item = kwargs.get("item")
             if item:
                 sys_state.add_item(item)
    except Exception:
        pass
    return result
