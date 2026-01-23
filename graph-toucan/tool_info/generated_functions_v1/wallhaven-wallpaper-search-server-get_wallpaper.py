from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for wallpaper information.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - id (str): unique identifier of the wallpaper
        - url (str): full URL to the wallpaper page on Wallhaven
        - short_url (str): shortened URL to the wallpaper page
        - uploader_username (str): username of the uploader
        - uploader_group (str): user group of the uploader
        - uploader_avatar_small (str): small avatar image URL
        - uploader_avatar_medium (str): medium avatar image URL
        - uploader_avatar_large (str): large avatar image URL
        - views (int): total number of views the wallpaper has received
        - favorites (int): total number of times the wallpaper has been favorited
        - source (str): original source URL of the wallpaper
        - purity (str): content rating: "sfw", "sketchy", or "nsfw"
        - category (str): main category of the wallpaper (e.g., "anime", "general")
        - dimension_x (int): horizontal resolution in pixels
        - dimension_y (int): vertical resolution in pixels
        - resolution (str): formatted resolution string (e.g., "3840x2160")
        - ratio (str): aspect ratio as a decimal string
        - file_size (int): file size in bytes
        - file_type (str): MIME type of the file
        - created_at (str): timestamp when the wallpaper was uploaded
        - colors_0 (str): first dominant hex color code
        - colors_1 (str): second dominant hex color code
        - path (str): direct download URL of the full-resolution image
        - thumbs_large (str): URL for large thumbnail
        - thumbs_original (str): URL for original thumbnail
        - thumbs_small (str): URL for small thumbnail
        - tag_0_id (int): first tag's ID
        - tag_0_name (str): first tag's name
        - tag_0_alias (str): first tag's alias
        - tag_0_category_id (int): first tag's category ID
        - tag_0_category (str): first tag's category
        - tag_0_purity (str): first tag's purity
        - tag_0_created_at (str): first tag's creation timestamp
        - tag_1_id (int): second tag's ID
        - tag_1_name (str): second tag's name
        - tag_1_alias (str): second tag's alias
        - tag_1_category_id (int): second tag's category ID
        - tag_1_category (str): second tag's category
        - tag_1_purity (str): second tag's purity
        - tag_1_created_at (str): second tag's creation timestamp
        - success (bool): indicates whether the request was successful
    """
    return {
        "id": "94x38z",
        "url": "https://wallhaven.cc/w/94x38z",
        "short_url": "https://whvn.cc/94x38z",
        "uploader_username": "AnimeLover42",
        "uploader_group": "user",
        "uploader_avatar_small": "https://a.deviantart.com/avatars/small/al.png",
        "uploader_avatar_medium": "https://a.deviantart.com/avatars/medium/al.png",
        "uploader_avatar_large": "https://a.deviantart.com/avatars/large/al.png",
        "views": 15420,
        "favorites": 893,
        "source": "https://www.artstation.com/artwork/12345",
        "purity": "sfw",
        "category": "anime",
        "dimension_x": 3840,
        "dimension_y": 2160,
        "resolution": "3840x2160",
        "ratio": "1.78",
        "file_size": 2473201,
        "file_type": "image/png",
        "created_at": "2023-05-15 08:30:22",
        "colors_0": "#2c3e50",
        "colors_1": "#e74c3c",
        "path": "https://w.wallhaven.cc/full/94/wallhaven-94x38z.png",
        "thumbs_large": "https://th.wallhaven.cc/lg/94/94x38z.jpg",
        "thumbs_original": "https://th.wallhaven.cc/or/94/94x38z.jpg",
        "thumbs_small": "https://th.wallhaven.cc/sm/94/94x38z.jpg",
        "tag_0_id": 10234,
        "tag_0_name": "anime girl",
        "tag_0_alias": "anime_girl",
        "tag_0_category_id": 1,
        "tag_0_category": "character",
        "tag_0_purity": "sfw",
        "tag_0_created_at": "2023-05-15 08:30:22",
        "tag_1_id": 20567,
        "tag_1_name": "blue hair",
        "tag_1_alias": "blue_hair",
        "tag_1_category_id": 2,
        "tag_1_category": "appearance",
        "tag_1_purity": "sfw",
        "tag_1_created_at": "2023-05-15 08:30:22",
        "success": True
    }

def wallhaven_wallpaper_search_server_get_wallpaper(wallpaper_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific wallpaper by ID.
    
    Args:
        wallpaper_id (str): The ID of the wallpaper (e.g., "94x38z")
    
    Returns:
        Dict containing detailed wallpaper information with the following structure:
        - id (str): unique identifier of the wallpaper
        - url (str): full URL to the wallpaper page on Wallhaven
        - short_url (str): shortened URL to the wallpaper page
        - uploader (Dict): contains uploader details including 'username', 'group', and 'avatar' with different sizes
        - views (int): total number of views the wallpaper has received
        - favorites (int): total number of times the wallpaper has been favorited
        - source (str): original source URL of the wallpaper
        - purity (str): content rating: "sfw", "sketchy", or "nsfw"
        - category (str): main category of the wallpaper
        - dimension_x (int): horizontal resolution in pixels
        - dimension_y (int): vertical resolution in pixels
        - resolution (str): formatted resolution string
        - ratio (str): aspect ratio as a decimal string
        - file_size (int): file size in bytes
        - file_type (str): MIME type of the file
        - created_at (str): timestamp when the wallpaper was uploaded
        - colors (List[str]): list of dominant hex color codes extracted from the wallpaper
        - path (str): direct download URL of the full-resolution image
        - thumbs (Dict): contains URLs for different thumbnail sizes: 'large', 'original', 'small'
        - tags (List[Dict]): list of tag objects with id, name, alias, category_id, category, purity, created_at
        - success (bool): indicates whether the request was successful
    
    Raises:
        ValueError: If wallpaper_id is empty or None
    """
    if not wallpaper_id:
        raise ValueError("wallpaper_id is required")
    
    # Fetch data from external API (simulated)
    api_data = call_external_api("wallhaven_wallpaper_search_server_get_wallpaper")
    
    # Construct nested structure matching output schema
    result = {
        "id": api_data["id"],
        "url": api_data["url"],
        "short_url": api_data["short_url"],
        "uploader": {
            "username": api_data["uploader_username"],
            "group": api_data["uploader_group"],
            "avatar": {
                "small": api_data["uploader_avatar_small"],
                "medium": api_data["uploader_avatar_medium"],
                "large": api_data["uploader_avatar_large"]
            }
        },
        "views": api_data["views"],
        "favorites": api_data["favorites"],
        "source": api_data["source"],
        "purity": api_data["purity"],
        "category": api_data["category"],
        "dimension_x": api_data["dimension_x"],
        "dimension_y": api_data["dimension_y"],
        "resolution": api_data["resolution"],
        "ratio": api_data["ratio"],
        "file_size": api_data["file_size"],
        "file_type": api_data["file_type"],
        "created_at": api_data["created_at"],
        "colors": [
            api_data["colors_0"],
            api_data["colors_1"]
        ],
        "path": api_data["path"],
        "thumbs": {
            "large": api_data["thumbs_large"],
            "original": api_data["thumbs_original"],
            "small": api_data["thumbs_small"]
        },
        "tags": [
            {
                "id": api_data["tag_0_id"],
                "name": api_data["tag_0_name"],
                "alias": api_data["tag_0_alias"],
                "category_id": api_data["tag_0_category_id"],
                "category": api_data["tag_0_category"],
                "purity": api_data["tag_0_purity"],
                "created_at": api_data["tag_0_created_at"]
            },
            {
                "id": api_data["tag_1_id"],
                "name": api_data["tag_1_name"],
                "alias": api_data["tag_1_alias"],
                "category_id": api_data["tag_1_category_id"],
                "category": api_data["tag_1_category"],
                "purity": api_data["tag_1_purity"],
                "created_at": api_data["tag_1_created_at"]
            }
        ],
        "success": api_data["success"]
    }
    
    return result