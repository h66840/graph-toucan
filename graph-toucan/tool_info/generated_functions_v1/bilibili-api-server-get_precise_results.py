from typing import Dict, List, Any, Optional

def call_external_api(tool_name: str) -> Dict[str, Any]:
    """
    Simulates fetching data from external API for Bilibili search results.
    
    Returns:
        Dict with simple scalar fields only (str, int, float, bool):
        - users_0_uname (str): Username of first user
        - users_0_mid (int): User ID of first user
        - users_0_face (str): Avatar URL of first user
        - users_0_fans (int): Follower count of first user
        - users_0_videos (int): Video upload count of first user
        - users_0_level (int): User level of first user
        - users_0_sign (str): Personal signature of first user
        - users_0_official (str): Verification or honor info of first user
        - users_1_uname (str): Username of second user
        - users_1_mid (int): User ID of second user
        - users_1_face (str): Avatar URL of second user
        - users_1_fans (int): Follower count of second user
        - users_1_videos (int): Video upload count of second user
        - users_1_level (int): User level of second user
        - users_1_sign (str): Personal signature of second user
        - users_1_official (str): Verification or honor info of second user
        - exact_match (bool): Whether there is an exact match
        - seid (str): Session ID for search request
        - page (int): Current page number
        - pagesize (int): Number of results per page
        - numResults (int): Total number of search results
        - numPages (int): Total number of pages available
        - suggest_keyword (str): Suggested alternative keyword
        - rqt_type (str): Type of request made
        - exp_list_egg_hit_enabled (bool): Experimental flag for egg_hit
        - exp_list_ui_optimization_enabled (bool): Experimental flag for UI optimization
        - egg_hit (int): Internal tracking parameter
        - show_column (int): Flag indicating column display in UI
        - in_black_key (int): Internal filtering flag for blacklisted terms
        - in_white_key (int): Internal filtering flag for whitelisted terms
    """
    return {
        "users_0_uname": "example_user",
        "users_0_mid": 123456,
        "users_0_face": "https://example.com/avatar1.jpg",
        "users_0_fans": 1500,
        "users_0_videos": 87,
        "users_0_level": 6,
        "users_0_sign": "Life is short, I use Python",
        "users_0_official": "Personal verification: Tech blogger",
        "users_1_uname": "example_user2",
        "users_1_mid": 789012,
        "users_1_face": "https://example.com/avatar2.jpg",
        "users_1_fans": 2300,
        "users_1_videos": 120,
        "users_1_level": 6,
        "users_1_sign": "Welcome to my channel!",
        "users_1_official": "Verified: Content creator",
        "exact_match": True,
        "seid": "session_abc123xyz",
        "page": 1,
        "pagesize": 20,
        "numResults": 2,
        "numPages": 1,
        "suggest_keyword": "",
        "rqt_type": "search",
        "exp_list_egg_hit_enabled": True,
        "exp_list_ui_optimization_enabled": False,
        "egg_hit": 0,
        "show_column": 1,
        "in_black_key": 0,
        "in_white_key": 1
    }

def bilibili_api_server_get_precise_results(keyword: str, search_type: Optional[str] = "user") -> Dict[str, Any]:
    """
    获取精确的搜索结果，过滤掉不必要的信息。
    
    Args:
        keyword (str): 搜索关键词
        search_type (str, optional): 搜索类型，默认为"user"(用户)，可选："video", "user", "live", "article"
        
    Returns:
        Dict containing:
        - users (List[Dict]): list of user objects matching the exact keyword, each containing:
            - uname (str): username
            - mid (int): user ID
            - face (str): avatar URL
            - fans (int): follower count
            - videos (int): video upload count
            - level (int): user level
            - sign (str): personal signature
            - official (str): verification or honor information
        - exact_match (bool): indicates whether there is an exact match for the search keyword
        - seid (str): session ID for the search request
        - page (int): current page number
        - pagesize (int): number of results per page
        - numResults (int): total number of search results returned
        - numPages (int): total number of pages available
        - suggest_keyword (str): suggested alternative keyword if no exact match
        - rqt_type (str): type of request made
        - exp_list (Dict[str, bool]): experimental feature flags used in search backend
        - egg_hit (int): internal tracking parameter
        - show_column (int): flag indicating column display in UI
        - in_black_key (int): internal filtering flag for blacklisted terms
        - in_white_key (int): internal filtering flag for whitelisted terms
    
    Raises:
        ValueError: If keyword is empty or invalid search_type is provided
    """
    if not keyword or not keyword.strip():
        raise ValueError("Keyword is required and cannot be empty")
    
    valid_search_types = {"video", "user", "live", "article"}
    if search_type and search_type not in valid_search_types:
        raise ValueError(f"Invalid search_type: {search_type}. Must be one of {valid_search_types}")
    
    # Call external API to get flattened data
    api_data = call_external_api("bilibili-api-server-get_precise_results")
    
    # Construct users list from indexed fields
    users = [
        {
            "uname": api_data["users_0_uname"],
            "mid": api_data["users_0_mid"],
            "face": api_data["users_0_face"],
            "fans": api_data["users_0_fans"],
            "videos": api_data["users_0_videos"],
            "level": api_data["users_0_level"],
            "sign": api_data["users_0_sign"],
            "official": api_data["users_0_official"]
        },
        {
            "uname": api_data["users_1_uname"],
            "mid": api_data["users_1_mid"],
            "face": api_data["users_1_face"],
            "fans": api_data["users_1_fans"],
            "videos": api_data["users_1_videos"],
            "level": api_data["users_1_level"],
            "sign": api_data["users_1_sign"],
            "official": api_data["users_1_official"]
        }
    ]
    
    # Construct exp_list from flattened experimental flags
    exp_list = {
        "egg_hit_enabled": api_data["exp_list_egg_hit_enabled"],
        "ui_optimization_enabled": api_data["exp_list_ui_optimization_enabled"]
    }
    
    # Build final result structure matching output schema
    result = {
        "users": users,
        "exact_match": api_data["exact_match"],
        "seid": api_data["seid"],
        "page": api_data["page"],
        "pagesize": api_data["pagesize"],
        "numResults": api_data["numResults"],
        "numPages": api_data["numPages"],
        "suggest_keyword": api_data["suggest_keyword"],
        "rqt_type": api_data["rqt_type"],
        "exp_list": exp_list,
        "egg_hit": api_data["egg_hit"],
        "show_column": api_data["show_column"],
        "in_black_key": api_data["in_black_key"],
        "in_white_key": api_data["in_white_key"]
    }
    
    return result