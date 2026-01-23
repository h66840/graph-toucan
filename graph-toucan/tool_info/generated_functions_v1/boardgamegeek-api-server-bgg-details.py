from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for boardgame details.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - id (int): unique BoardGameGeek ID of the board game
        - name (str): official name of the board game
        - description (str): detailed description of the game mechanics, theme, and gameplay
        - year (int): year the game was first published
        - complexity (float): average complexity rating on a scale from 1 (light) to 5 (heavy)
        - players (str): recommended player count range, e.g. "2-4" or "1-6"
        - bgg_rating (float): average rating from BoardGameGeek users on a scale of 1–10
        - bayes_average (float): Bayesian average of the game's rating, used by BGG for rankings
        - play_time (str): typical duration of a game session, e.g. "30 min" or "60-120 min"
        - min_age (int): minimum recommended age for players
        - designer (str): primary game designer(s), comma-separated if multiple
        - publisher (str): list of publishers who have released the game, comma-separated
        - type (str): type of game, typically "boardgame"
        - thumbnail (str): URL to a small thumbnail image of the game
        - image (str): URL to a full-size image of the game
        - categories_0 (str): first category associated with the game
        - categories_1 (str): second category associated with the game
        - mechanics_0 (str): first game mechanic used in the design
        - mechanics_1 (str): second game mechanic used in the design
        - num_ratings (int): total number of user ratings the game has received on BGG
        - owned (int): number of users who own the game in their BGG collection
        - wishing (int): number of users who have the game on their BGG wishlist
        - trading (int): number of users who have the game listed for trade on BGG
        - wanting (int): number of users who want the game but are not currently trading for it
    """
    return {
        "id": 123456,
        "name": "Wingspan",
        "description": "Wingspan is a competitive, medium-weight, card-driven, engine-building board game from Stonemaier Games.",
        "year": 2019,
        "complexity": 2.3,
        "players": "1-5",
        "bgg_rating": 8.1,
        "bayes_average": 7.9,
        "play_time": "40-70 min",
        "min_age": 10,
        "designer": "Elizabeth Hargrave",
        "publisher": "Stonemaier Games, Eggertspiele",
        "type": "boardgame",
        "thumbnail": "https://example.com/wingspan_thumb.jpg",
        "image": "https://example.com/wingspan_full.jpg",
        "categories_0": "Animals",
        "categories_1": "Card Game",
        "mechanics_0": "Card Drafting",
        "mechanics_1": "Set Collection",
        "num_ratings": 45000,
        "owned": 120000,
        "wishing": 30000,
        "trading": 1500,
        "wanting": 8000
    }

def boardgamegeek_api_server_bgg_details(
    full_details: Optional[bool] = False,
    id: Optional[int] = None,
    name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find the details about a specific board game on BoardGameGeek (BGG).
    
    Args:
        full_details (bool, optional): Return the complete BGG API response instead of essential info.
            WARNING: This returns significantly more data and can overload AI context windows.
            ONLY set this to true if the user explicitly requests 'full details', 'complete data', or similar.
            Default behavior returns essential info which is sufficient for most use cases.
        id (int, optional): The BoardGameGeek ID of the board game
        name (str, optional): The name of the board game
    
    Returns:
        Dict containing board game details with the following structure:
        - id (int): unique BoardGameGeek ID of the board game
        - name (str): official name of the board game
        - description (str): detailed description of the game mechanics, theme, and gameplay
        - year (int): year the game was first published
        - complexity (float): average complexity rating on a scale from 1 (light) to 5 (heavy)
        - players (str): recommended player count range, e.g. "2-4" or "1-6"
        - bgg_rating (float): average rating from BoardGameGeek users on a scale of 1–10
        - bayes_average (float): Bayesian average of the game's rating, used by BGG for rankings
        - play_time (str): typical duration of a game session, e.g. "30 min" or "60-120 min"
        - min_age (int): minimum recommended age for players
        - designer (str): primary game designer(s), comma-separated if multiple
        - publisher (str): list of publishers who have released the game, comma-separated
        - type (str): type of game, typically "boardgame"
        - thumbnail (str): URL to a small thumbnail image of the game
        - image (str): URL to a full-size image of the game
        - categories (List[str]): thematic or genre categories associated with the game
        - mechanics (List[str]): game mechanics used in the design, such as drafting or set collection
        - num_ratings (int): total number of user ratings the game has received on BGG
        - owned (int): number of users who own the game in their BGG collection
        - wishing (int): number of users who have the game on their BGG wishlist
        - trading (int): number of users who have the game listed for trade on BGG
        - wanting (int): number of users who want the game but are not currently trading for it
    """
    # Input validation
    if id is not None and id <= 0:
        raise ValueError("ID must be a positive integer")
    if name is not None and not name.strip():
        raise ValueError("Name cannot be empty or whitespace")
    
    # Call external API to get flat data
    api_data = call_external_api("boardgamegeek-api-server-bgg-details")
    
    # Construct categories list
    categories = []
    if "categories_0" in api_data and api_data["categories_0"]:
        categories.append(api_data["categories_0"])
    if "categories_1" in api_data and api_data["categories_1"]:
        categories.append(api_data["categories_1"])
    
    # Construct mechanics list
    mechanics = []
    if "mechanics_0" in api_data and api_data["mechanics_0"]:
        mechanics.append(api_data["mechanics_0"])
    if "mechanics_1" in api_data and api_data["mechanics_1"]:
        mechanics.append(api_data["mechanics_1"])
    
    # Build result dictionary matching output schema
    result = {
        "id": api_data["id"],
        "name": api_data["name"],
        "description": api_data["description"],
        "year": api_data["year"],
        "complexity": api_data["complexity"],
        "players": api_data["players"],
        "bgg_rating": api_data["bgg_rating"],
        "bayes_average": api_data["bayes_average"],
        "play_time": api_data["play_time"],
        "min_age": api_data["min_age"],
        "designer": api_data["designer"],
        "publisher": api_data["publisher"],
        "type": api_data["type"],
        "thumbnail": api_data["thumbnail"],
        "image": api_data["image"],
        "categories": categories,
        "mechanics": mechanics,
        "num_ratings": api_data["num_ratings"],
        "owned": api_data["owned"],
        "wishing": api_data["wishing"],
        "trading": api_data["trading"],
        "wanting": api_data["wanting"]
    }
    
    # If full_details is requested, we could include more fields or nested structures,
    # but per instructions we're only simulating with the data we have
    if full_details:
        # In a real implementation, this would include additional data
        # For simulation, we just return the same structure
        pass
    
    return result