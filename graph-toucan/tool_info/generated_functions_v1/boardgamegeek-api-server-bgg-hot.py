from typing import Dict, List, Any

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for BoardGameGeek hot games.

    Returns:
        Dict with simple fields only (str, int, float, bool):
        - hot_game_0_ID (int): BoardGameGeek ID of the first hot game
        - hot_game_0_Rank (int): Rank of the first hot game
        - hot_game_0_Name (str): Name of the first hot game
        - hot_game_0_YearPublished (int): Year the first hot game was published
        - hot_game_0_Thumbnail (str): URL to the thumbnail image of the first hot game
        - hot_game_1_ID (int): BoardGameGeek ID of the second hot game
        - hot_game_1_Rank (int): Rank of the second hot game
        - hot_game_1_Name (str): Name of the second hot game
        - hot_game_1_YearPublished (int): Year the second hot game was published
        - hot_game_1_Thumbnail (str): URL to the thumbnail image of the second hot game
    """
    return {
        "hot_game_0_ID": 323177,
        "hot_game_0_Rank": 1,
        "hot_game_0_Name": "Brass: Birmingham",
        "hot_game_0_YearPublished": 2018,
        "hot_game_0_Thumbnail": "https://cf.geekdo-images.com/thumb/img/ABC123=/fit-in/200x150/pic1234567.jpg",
        "hot_game_1_ID": 161932,
        "hot_game_1_Rank": 2,
        "hot_game_1_Name": "Gloomhaven",
        "hot_game_1_YearPublished": 2017,
        "hot_game_1_Thumbnail": "https://cf.geekdo-images.com/thumb/img/DEF456=/fit-in/200x150/pic2345678.jpg"
    }

def boardgamegeek_api_server_bgg_hot() -> Dict[str, List[Dict[str, Any]]]:
    """
    Find the current board game hotness on BoardGameGeek (BGG).

    This function simulates querying the BoardGameGeek API for the current hot games.
    It returns a list of board games with their details including ID, rank, name,
    year published, and thumbnail image.

    Returns:
        Dict containing:
        - hot_games (List[Dict]): List of board games from BGG hotness list, each with
          'ID', 'Rank', 'Name', 'YearPublished', and 'Thumbnail' fields
    """
    try:
        api_data = call_external_api("boardgamegeek-api-server-bgg-hot")
        
        hot_games = [
            {
                "ID": api_data["hot_game_0_ID"],
                "Rank": api_data["hot_game_0_Rank"],
                "Name": api_data["hot_game_0_Name"],
                "YearPublished": api_data["hot_game_0_YearPublished"],
                "Thumbnail": api_data["hot_game_0_Thumbnail"]
            },
            {
                "ID": api_data["hot_game_1_ID"],
                "Rank": api_data["hot_game_1_Rank"],
                "Name": api_data["hot_game_1_Name"],
                "YearPublished": api_data["hot_game_1_YearPublished"],
                "Thumbnail": api_data["hot_game_1_Thumbnail"]
            }
        ]
        
        return {"hot_games": hot_games}
        
    except KeyError as e:
        # Handle missing expected fields
        raise KeyError(f"Missing expected data field: {str(e)}") from e
    except Exception as e:
        # Handle any other unexpected errors
        raise RuntimeError(f"Failed to retrieve hot games from BGG: {str(e)}") from e