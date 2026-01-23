from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for movie or TV show information.
    
    Returns:
        Dict with simple fields only (str, int, float, bool):
        - title (str): The title of the movie or TV show
        - year (int): The release year
        - rating (float): Average user rating on a scale of 0 to 10
        - vote_count (int): Number of votes or reviews
        - genre_0 (str): First genre associated with the movie or TV show
        - genre_1 (str): Second genre associated with the movie or TV show
        - runtime (int): Duration of the movie in minutes (only for movies)
        - seasons (int): Number of seasons (only for TV shows)
        - episodes (int): Total number of episodes (only for TV shows)
        - director (str): Name of the director
        - creator (str): Name of the creator (only for TV shows)
        - cast_0 (str): First main cast member's name
        - cast_1 (str): Second main cast member's name
        - overview (str): Brief plot summary or description
        - poster_url (str): URL to the poster image hosted online
    """
    return {
        "title": "Inception",
        "year": 2010,
        "rating": 8.8,
        "vote_count": 2345678,
        "genre_0": "Sci-Fi",
        "genre_1": "Action",
        "runtime": 148,
        "seasons": 0,
        "episodes": 0,
        "director": "Christopher Nolan",
        "creator": "",
        "cast_0": "Leonardo DiCaprio",
        "cast_1": "Marion Cotillard",
        "overview": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster_url": "https://example.com/posters/inception.jpg"
    }

def movie_information_server_search_movie(query: str) -> Dict[str, Any]:
    """
    Search for movies and TV shows based on the provided query.
    
    Args:
        query (str): The movie or TV show name to search for
        
    Returns:
        Dict containing detailed information about the movie/TV show including:
        - title (str): The title of the movie or TV show
        - year (int): The release year
        - rating (float): Average user rating (0-10)
        - vote_count (int): Number of votes contributing to the rating
        - genres (List[str]): List of genres
        - runtime (int, optional): Duration in minutes (movies only)
        - seasons (int, optional): Number of seasons (TV shows only)
        - episodes (int, optional): Total number of episodes (TV shows only)
        - director (str): Director name
        - creator (str, optional): Creator name (TV shows only)
        - cast (List[str]): List of main cast members
        - overview (str): Plot summary or description
        - poster_url (str): URL to the poster image
        
    Raises:
        ValueError: If query is empty or not a string
    """
    if not query or not isinstance(query, str):
        raise ValueError("Query must be a non-empty string")
    
    # Call external API to get flat data
    api_data = call_external_api("movie-information-server-search_movie")
    
    # Construct genres list
    genres = []
    if api_data.get("genre_0"):
        genres.append(api_data["genre_0"])
    if api_data.get("genre_1"):
        genres.append(api_data["genre_1"])
    
    # Construct cast list
    cast = []
    if api_data.get("cast_0"):
        cast.append(api_data["cast_0"])
    if api_data.get("cast_1"):
        cast.append(api_data["cast_1"])
    
    # Build result dictionary matching output schema
    result: Dict[str, Any] = {
        "title": api_data["title"],
        "year": api_data["year"],
        "rating": api_data["rating"],
        "vote_count": api_data["vote_count"],
        "genres": genres,
        "director": api_data["director"],
        "cast": cast,
        "overview": api_data["overview"],
        "poster_url": api_data["poster_url"]
    }
    
    # Add movie-specific fields if applicable
    if api_data.get("runtime") and api_data["runtime"] > 0:
        result["runtime"] = api_data["runtime"]
    
    # Add TV show-specific fields if applicable
    if api_data.get("seasons") and api_data["seasons"] > 0:
        result["seasons"] = api_data["seasons"]
        result["episodes"] = api_data["episodes"]
        if api_data.get("creator"):
            result["creator"] = api_data["creator"]
    
    return result