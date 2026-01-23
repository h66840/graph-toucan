from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching wallpaper search data from external Wallhaven API.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - success (bool): Whether the search was successful
        - meta_current_page (int): Current page number
        - meta_last_page (int): Last available page
        - meta_per_page (int): Number of results per page
        - meta_total (int): Total number of results
        - meta_query (str): Query string used
        - meta_seed (str or None): Seed used for random sorting
        - data_0_id (str): First wallpaper ID
        - data_0_url (str): First wallpaper full URL
        - data_0_short_url (str): First wallpaper short URL
        - data_0_views (int): First wallpaper view count
        - data_0_favorites (int): First wallpaper favorite count
        - data_0_source (str): First wallpaper source URL
        - data_0_purity (str): First wallpaper purity (e.g., 'sfw')
        - data_0_category (str): First wallpaper category (e.g., 'general')
        - data_0_dimension_x (int): First wallpaper width in pixels
        - data_0_dimension_y (int): First wallpaper height in pixels
        - data_0_file_size (int): First wallpaper file size in bytes
        - data_0_file_type (str): First wallpaper MIME type
        - data_0_created_at (str): First wallpaper creation timestamp (ISO format)
        - data_0_path (str): First wallpaper image path
        - data_0_thumbs_large (str): First wallpaper large thumbnail URL
        - data_0_thumbs_original (str): First wallpaper original thumbnail URL
        - data_0_thumbs_small (str): First wallpaper small thumbnail URL
        - data_0_colors_0 (str): First color hex code for first wallpaper
        - data_0_colors_1 (str): Second color hex code for first wallpaper
        - data_1_id (str): Second wallpaper ID
        - data_1_url (str): Second wallpaper full URL
        - data_1_short_url (str): Second wallpaper short URL
        - data_1_views (int): Second wallpaper view count
        - data_1_favorites (int): Second wallpaper favorite count
        - data_1_source (str): Second wallpaper source URL
        - data_1_purity (str): Second wallpaper purity (e.g., 'sfw')
        - data_1_category (str): Second wallpaper category (e.g., 'anime')
        - data_1_dimension_x (int): Second wallpaper width in pixels
        - data_1_dimension_y (int): Second wallpaper height in pixels
        - data_1_file_size (int): Second wallpaper file size in bytes
        - data_1_file_type (str): Second wallpaper MIME type
        - data_1_created_at (str): Second wallpaper creation timestamp (ISO format)
        - data_1_path (str): Second wallpaper image path
        - data_1_thumbs_large (str): Second wallpaper large thumbnail URL
        - data_1_thumbs_original (str): Second wallpaper original thumbnail URL
        - data_1_thumbs_small (str): Second wallpaper small thumbnail URL
        - data_1_colors_0 (str): First color hex code for second wallpaper
        - data_1_colors_1 (str): Second color hex code for second wallpaper
    """
    return {
        "success": True,
        "meta_current_page": 1,
        "meta_last_page": 5,
        "meta_per_page": 2,
        "meta_total": 10,
        "meta_query": "nature",
        "meta_seed": "abc123",
        "data_0_id": "wallhaven-abc123",
        "data_0_url": "https://wallhaven.cc/w/abc123",
        "data_0_short_url": "https://whvn.cc/abc123",
        "data_0_views": 1500,
        "data_0_favorites": 200,
        "data_0_source": "https://example.com/original",
        "data_0_purity": "sfw",
        "data_0_category": "general",
        "data_0_dimension_x": 1920,
        "data_0_dimension_y": 1080,
        "data_0_file_size": 856789,
        "data_0_file_type": "image/jpeg",
        "data_0_created_at": "2023-10-15T08:30:00Z",
        "data_0_path": "https://w.wallhaven.cc/full/ab/wallhaven-abc123.jpg",
        "data_0_thumbs_large": "https://th.wallhaven.cc/lg/ab/abc123.jpg",
        "data_0_thumbs_original": "https://th.wallhaven.cc/orig/ab/abc123.jpg",
        "data_0_thumbs_small": "https://th.wallhaven.cc/sm/ab/abc123.jpg",
        "data_0_colors_0": "1a2b3c",
        "data_0_colors_1": "4d5e6f",
        "data_1_id": "wallhaven-def456",
        "data_1_url": "https://wallhaven.cc/w/def456",
        "data_1_short_url": "https://whvn.cc/def456",
        "data_1_views": 2300,
        "data_1_favorites": 350,
        "data_1_source": "https://example.com/original2",
        "data_1_purity": "sfw",
        "data_1_category": "anime",
        "data_1_dimension_x": 2560,
        "data_1_dimension_y": 1440,
        "data_1_file_size": 1234567,
        "data_1_file_type": "image/png",
        "data_1_created_at": "2023-10-14T12:45:00Z",
        "data_1_path": "https://w.wallhaven.cc/full/de/wallhaven-def456.png",
        "data_1_thumbs_large": "https://th.wallhaven.cc/lg/de/def456.png",
        "data_1_thumbs_original": "https://th.wallhaven.cc/orig/de/def456.png",
        "data_1_thumbs_small": "https://th.wallhaven.cc/sm/de/def456.png",
        "data_1_colors_0": "7a8b9c",
        "data_1_colors_1": "aabbcc"
    }

def wallhaven_wallpaper_search_server_search_wallpapers(
    query: Optional[str] = None,
    categories: Optional[str] = None,
    purity: Optional[str] = None,
    sorting: Optional[str] = None,
    order: Optional[str] = None,
    top_range: Optional[str] = None,
    atleast: Optional[str] = None,
    resolutions: Optional[str] = None,
    ratios: Optional[str] = None,
    colors: Optional[str] = None,
    page: Optional[int] = None,
    seed: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for wallpapers on Wallhaven based on various criteria.
    
    Args:
        query: Search query (tags, keywords, etc.)
        categories: Categories to include (e.g., "100" for general only, "110" for general+anime)
        purity: Purity filter (e.g., "100" for SFW only, "110" for SFW+sketchy)
        sorting: How to sort results (date_added, relevance, random, views, favorites, toplist)
        order: Sort order (desc, asc)
        top_range: Time range for toplist (1d, 3d, 1w, 1M, 3M, 6M, 1y)
        atleast: Minimum resolution (e.g., "1920x1080")
        resolutions: Exact resolutions (e.g., "1920x1080,2560x1440")
        ratios: Aspect ratios (e.g., "16x9,16x10")
        colors: Color hex code (e.g., "0066cc")
        page: Page number
        seed: Seed for random results
    
    Returns:
        Dict containing:
        - data (List[Dict]): list of wallpaper objects with detailed information
        - meta (Dict): pagination and query metadata
        - success (bool): whether the search was successful
    """
    # Call external API to get flattened data
    api_data = call_external_api("wallhaven_wallpaper_search_server_search_wallpapers")
    
    # Construct the first wallpaper object
    wallpaper_0 = {
        "id": api_data["data_0_id"],
        "url": api_data["data_0_url"],
        "short_url": api_data["data_0_short_url"],
        "views": api_data["data_0_views"],
        "favorites": api_data["data_0_favorites"],
        "source": api_data["data_0_source"],
        "purity": api_data["data_0_purity"],
        "category": api_data["data_0_category"],
        "dimension_x": api_data["data_0_dimension_x"],
        "dimension_y": api_data["data_0_dimension_y"],
        "file_size": api_data["data_0_file_size"],
        "file_type": api_data["data_0_file_type"],
        "created_at": api_data["data_0_created_at"],
        "path": api_data["data_0_path"],
        "thumbs": {
            "large": api_data["data_0_thumbs_large"],
            "original": api_data["data_0_thumbs_original"],
            "small": api_data["data_0_thumbs_small"]
        },
        "colors": [
            api_data["data_0_colors_0"],
            api_data["data_0_colors_1"]
        ]
    }
    
    # Construct the second wallpaper object
    wallpaper_1 = {
        "id": api_data["data_1_id"],
        "url": api_data["data_1_url"],
        "short_url": api_data["data_1_short_url"],
        "views": api_data["data_1_views"],
        "favorites": api_data["data_1_favorites"],
        "source": api_data["data_1_source"],
        "purity": api_data["data_1_purity"],
        "category": api_data["data_1_category"],
        "dimension_x": api_data["data_1_dimension_x"],
        "dimension_y": api_data["data_1_dimension_y"],
        "file_size": api_data["data_1_file_size"],
        "file_type": api_data["data_1_file_type"],
        "created_at": api_data["data_1_created_at"],
        "path": api_data["data_1_path"],
        "thumbs": {
            "large": api_data["data_1_thumbs_large"],
            "original": api_data["data_1_thumbs_original"],
            "small": api_data["data_1_thumbs_small"]
        },
        "colors": [
            api_data["data_1_colors_0"],
            api_data["data_1_colors_1"]
        ]
    }
    
    # Construct the final result
    result = {
        "success": api_data["success"],
        "meta": {
            "current_page": api_data["meta_current_page"],
            "last_page": api_data["meta_last_page"],
            "per_page": api_data["meta_per_page"],
            "total": api_data["meta_total"],
            "query": api_data["meta_query"],
            "seed": api_data["meta_seed"]
        },
        "data": [wallpaper_0, wallpaper_1]
    }
    
    return result